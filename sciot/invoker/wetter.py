import json
import requests
import time, threading
import paho.mqtt.publish as publish

auth = {'username': 'xxx', 'password': 'xxxxxxx'}

def query_weather():
    global temp_o
    temp_o = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Stuttgart&appid=xxxxxxxxxxx").json()["main"]["temp"] - 273.15
    publish.single('/sensors/wtr', temp_o, auth=auth)
    threading.Timer(120, query_weather).start()

def main():
    query_weather()

if __name__ == '__main__':
    main()
