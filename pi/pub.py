#!/usr/bin/python

import sys
import paho.mqtt.publish as publish

#topic=sys.argv[1]
#payload=sys.argv[2]

host = 'xxx.xxx.xxx'

def expose_metrics(topic, payload):
    publish.single(topic, payload, hostname=host, auth = {'username':"xxx", 'password':"xxx"})

print ("Ok")
