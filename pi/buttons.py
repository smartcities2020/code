import RPi.GPIO as GPIO  
from time import sleep     

from pub import expose_metrics
 


WND_TOPIC = '/sensors/wnd'
SHD_TOPIC = '/sensors/shd'


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  
try:  
  while True:
    expose_metrics(WND_TOPIC,GPIO.input(23))
    expose_metrics(SHD_TOPIC,GPIO.input(24))
    sleep(2) 
  
finally:                   
  GPIO.cleanup()        
