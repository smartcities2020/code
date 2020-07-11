from prometheus_client import Gauge, start_http_server, Summary
import mh_z19

import time, threading
import Adafruit_DHT
from pub import expose_metrics


g_co2 = Gauge('co2_concentration', 'CO2 in ppm')
g_hum= Gauge('dht_hum', 'Humidity in pct')
g_tmp= Gauge('dht_tmp', 'tmp in celsius')

dht_pin = '17'

def read_co2():
    print(time.ctime())
    val = mh_z19.read()['co2']
    print("co2: " + str(val))
    return val
    #threading.Timer(10, read_co2).start()

def read_dht(dht):
    humidity, temperature = Adafruit_DHT.read_retry(dht, dht_pin)
    print("hum:" + str(humidity) + ",tmp: " + str(temperature))
    return humidity, temperature
CO2_TOPIC = '/sensors/co2'
HUM_TOPIC = '/sensors/humidity'
TEMP_TOPIC = '/sensors/temp'

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print("Starting up on port 8000")
    start_http_server(8000)
    print("starting loop")
    dht = Adafruit_DHT.DHT11
    while True:
        print("looping")
        co2_val = read_co2()
        g_co2.set(co2_val)
        expose_metrics(CO2_TOPIC, co2_val)
        humidity, temperature = read_dht(dht)
        g_hum.set(humidity)
        g_tmp.set(temperature)
        expose_metrics(HUM_TOPIC, humidity)
        expose_metrics(TEMP_TOPIC, temperature)
        time.sleep(30)
