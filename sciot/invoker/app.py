import os
import signal
import sys
from jinja2 import Template, FileSystemLoader, Environment
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import json
import requests
import time, threading
import subprocess
import paho.mqtt.publish as publish




host = 'xxx.xxx.xxx'
auth = {'username': 'xxx', 'password': 'xxx'}

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('problem.pddl.j2')

client = InfluxDBClient('localhost', 8086, 'invoker', 'xxxxxx', 'sensors')

#desired_heater_softgoal = False
#desired_window_softgoal = False
#desired_shades_softgoal = False
desired_softgoal = False

MQTT_TOPIC = '/sensors/+'
MQTT_USER = 'xxx'
MQTT_PASSWORD = 'xxx'
MQTT_ADDRESS = 'localhost'

window_topic = "servo0"
shades_topic = "servo1"
heater_topic = "htr"
foo = 0

#temp_o = 20

heater_on_state=False

tick_count  = 0



def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    foo = 4
    #print("got message")

def on_trigger():
    global tick_count

    tick_count +=1

    desired_softgoal = tick_count % 4 == 0

    print("Trying softgoals: " + str(desired_softgoal))
    render_pddl(desired_softgoal)
    invoke_ff(True)
    #apply_updates()  # might change heater on state
    threading.Timer(10, on_trigger).start()




def render_pddl(softgoals):
    light    = client.query('SELECT last(value) as value FROM sensors.autogen.light    WHERE time > now() - 2h;').get_points().next()['value']
    co2      = client.query('SELECT last(value) as value FROM sensors.autogen.co2      WHERE time > now() - 2h;').get_points().next()['value']
    humidity = client.query('SELECT last(value) as value FROM sensors.autogen.humidity WHERE time > now() - 2h;').get_points().next()['value']
    shd      = client.query('SELECT last(value) as value FROM sensors.autogen.shd      WHERE time > now() - 2h;').get_points().next()['value']
    temp     = client.query('SELECT last(value) as value FROM sensors.autogen.temp     WHERE time > now() - 2h;').get_points().next()['value']
    wnd      = client.query('SELECT last(value) as value FROM sensors.autogen.wnd      WHERE time > now() - 2h;').get_points().next()['value']
    htr      = client.query('SELECT last(value) as value FROM sensors.autogen.htr      WHERE time > now() - 2h;').get_points().next()['value']
    temp_o   = client.query('SELECT last(value) as value FROM sensors.autogen.wtr      WHERE time > now() - 2h;').get_points().next()['value']
    
    print('light   :'+str(light    )) 
    print('co2     :'+str(co2      )) 
    print('humidity:'+str(humidity )) 
    print('shd     :'+str(shd      )) 
    print('temp    :'+str(temp     )) 
    print('wnd     :'+str(wnd      )) 
    print('htr     :'+str(htr      )) 
    print('temp_o  :'+str(temp_o   ))
    
    context={}
    
    state={}
    
    
    #---------- if co2 val > 1000 oder so
    state['co2_crit']       = co2  > 1000
    state['temp_high_i']    = temp > 25
    state['temp_low_i']     = temp < 16
    state['temp_high_o']    = temp_o > 30
    state['temp_low_o']     = temp_o < 10
    state['hum_high']       = humidity > 60
    state['hum_low']        = humidity < 30
    state['light_crit']     = light >128
    # ruhezustand (fenster zu rollo oben = alles auf 0)
    state['window_closed']  = wnd == 0 # offenes fenster = schalter auf 1
    state['shades_up']      = shd == 0 # shades oben = schalter auf 0
    state['heater_on']      = htr == 1
    
    #----------
    
    goal={}
    
    goal['user_window_open']=False
    goal['user_window_closed']=False
    goal['user_shades_open']=False
    goal['user_shades_closed']=False
    
    #goal['user_window_closed']=desired_window_softgoal&&!state['co2_crit']
    #goal['user_shades_open']=desired_shades_softgoal&&!state['light_crit']
    #goal['user_heater_off']=desired_heater_softgoal&&!state['temp_low_i']

    goal['softgoals_wnd']=softgoals
    goal['softgoals_shd']=softgoals
    goal['softgoals_htr']= not state['temp_low_o']
    
    context['init_state']=state
    context['goal']=goal
    
    output_from_parsed_template = template.render(context)
    with open("problem.pddl", "w") as fh:
        fh.write(output_from_parsed_template)


def invoke_ff(try_again):
    try:
      result = subprocess.check_output(['/srv/sciot/tools/ff -o /srv/sciot/planning/domain.pddl -f /srv/sciot/invoker/problem.pddl'],shell=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
      # check if plan would be impossible
      # e.output has to contain false
      # render_pddl(False)
      # invoke_ff again (attention recursion)
      # e.cmd, e.returncode, e.output
      if "FALSE" in e.output and try_again:
          print("Will try again")
          render_pddl(False)
          invoke_ff(False)
      elif "TRUE" in e.output:
          print("Already satisfied")
      else:
          print("Won't try again, still not fulfillable")
      return

    print(result)
    parse_instruction(result)

def parse_instruction(text):
    instruction = text[text.find('step')+4: text.find('time spent')]

    instruction_steps = []

    # find the first valid step
    for row in instruction.split('\n'):
        parts = row.strip().split(':')
        if len(parts) == 1:
            continue
        step = int(parts[0])
        rest = ' '.join(parts[1:])
        parts = [part.strip() for part in rest.split(' ') if part !='']
        command = parts[0]
        sensors = parts[1:]
        instruction_steps.append({
            'step': step,
            'command': command,
            'sensors': sensors})

        for sensor in sensors:
            print(sensor + " " + command)
            if sensor == "S01" :
                if command == "A-SHADES-DOWN":
                    send_instruction(shades_topic, '{"pos":128}')
                if command == "A-SHADES-UP":
                    send_instruction(shades_topic, '{"pos":0}')
            if sensor == "W01" :
                if command == "A-WINDOW-OPEN":
                    send_instruction(window_topic, '{"pos":128}')
                if command == "A-WINDOW-CLOSE":
                    send_instruction(window_topic, '{"pos":0}')
            if sensor == "H01" :
                if command == "A-HEATER-ON":
                    send_instruction(heater_topic, '1')
                    send_volatile_state(heater_topic, '1')
                    global heater_on_state
                    heater_on_state = True
                if command == "A-HEATER-OFF":
                    send_instruction(heater_topic, '0')
                    send_volatile_state(heater_topic, '0')
                    heater_on_state = False
         # when we found a valid plan step, return and do not continue processing
        return


def send_instruction(sensor, command):
    publish.single('/commands/{}'.format(sensor), command, auth=auth)

def send_volatile_state(sensor, command):
    publish.single('/sensors/{}'.format(sensor), command, auth=auth)

def signal_handler(sig, frame):
    print('Rcv sigint, exit')
    sys.exit(0)

def main():

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    signal.signal(signal.SIGINT, signal_handler)

    mqtt_client.connect(MQTT_ADDRESS, 1883, 60)
    #query_weather()

    on_trigger()
    mqtt_client.loop_forever()

if __name__ == '__main__':
    main()
