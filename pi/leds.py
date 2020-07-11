import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep

WND_TOPIC = '/sensors/wnd'
SHD_TOPIC = '/sensors/shd'
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/commands/htr")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if int(msg.payload) == 1 :
        print("led on")
        GPIO.output(25,1)
    else:
        print("led off")
        GPIO.output(25,0)


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.OUT)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("XXX","XXX")
client.connect("XXX.XXX.XXX", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
