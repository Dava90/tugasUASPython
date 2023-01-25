from machine import Pin, Timer
import network
import time
from umqtt.robust import MQTTClient
import sys
import dht

sensor = dht.DHT11(Pin(2))                  

WIFI_SSID     = 'WIN'
WIFI_PASSWORD = '11111111'

mqtt_client_id      = bytes('client_'+'12321', 'utf-8')

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'dav4'
ADAFRUIT_IO_KEY     = 'aio_Vjru96UG6bwkUdak6IxVOgYjc5Wl'

TEMP_FEED_ID      = 'temperature'
HUM_FEED_ID      = 'humidity'

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('connected')
    else:
        print('not connected')
        sys.exit()
        

connect_wifi()


client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

        
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8')
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8')


def sens_data(data):
    sensor.measure()                   
    temperature = sensor.temperature()        
    humidity = sensor.humidity()
    client.publish(temp_feed,    
                  bytes(str(temperature), 'utf-8'),  
                  qos=0)
    
    client.publish(hum_feed,    
                  bytes(str(humidity), 'utf-8'),
                  qos=0)
    print("Temperature - ", str(temperature),"°C")
    print("Humidity - " , str(humidity),"%")
    print('Msg sent')
    
    
    
timer = Timer(0)
timer.init(period=5000, mode=Timer.PERIODIC, callback = sens_data)