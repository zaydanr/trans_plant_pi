import RPi.GPIO as GPIO
import time
import random 
from paho.mqtt import client as mqtt_client
import Adafruit_BMP.BMP085 as BMP085
import json

RelayPin = 11    # pin11
PumpPin = 12
broker = 'mqtt.things.ph' #INPUT BROKER NAME
port = 1883
topic = "MQTT_Challenge" #INPUT TOPIC NAME
client_id = f'publish-{random.randint(0, 1000)}'
username = '64c14253811ec75105c1948a' #INPUT USERNAME
password = 'QuRHxlbi8RDbkv7Nkq77N3Ps' #INPUT PASSWORD

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if(msg.payload.decode() == 'pump_on'):
            print("Turning Pump ON")
            GPIO.output(PumpPin, GPIO.HIGH)
        elif(msg.payload.decode() == "pump_off"):
            print("Turning Pump OFF")
            GPIO.output(PumpPin, GPIO.LOW)
        elif(msg.payload.decode() == "light_on"): #The light relay is reversed. GPIO LOW is on, GPIO HIGH is off.
            print("Turning Light ON")
            GPIO.output(RelayPin, GPIO.LOW)
        elif(msg.payload.decode() == "light_off"):
             print("Turning Light OFF")
             GPIO.output(RelayPin, GPIO.HIGH)

            
    client.subscribe(topic)
    client.on_message = on_message
    
def setup():
   GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
   GPIO.setup(RelayPin, GPIO.OUT)
   GPIO.setup(PumpPin, GPIO.OUT)
   GPIO.output(RelayPin, GPIO.HIGH)
   GPIO.output(PumpPin, GPIO.LOW)
   
def loop():
   while True:
      #'...relayd on'
      GPIO.output(RelayPin, GPIO.LOW)
      GPIO.output(PumpPin, GPIO.HIGH)
      time.sleep(60)
      #'relay off...'
      GPIO.output(RelayPin, GPIO.HIGH)
      GPIO.output(PumpPin, GPIO.LOW)
      time.sleep(60)
def run():
   client = connect_mqtt()
   subscribe(client)
   client.loop_forever()

def destroy():
   GPIO.output(RelayPin, GPIO.HIGH)
   GPIO.output(PumpPin, GPIO.LOW)
   GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
   setup()
   try:
      run()
   except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
      destroy()
