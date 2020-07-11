#!/usr/bin/python
import sys
import paho.mqtt.publish as publish

host = 'xxx.xxx.xxx'
auth = {'username': 'xxx', 'password': 'xxx'}

def send_instruction(sensor, command):
    publish.single('/commands/{}'.format(sensor),
                   command, auth=auth)

