import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from collections import namedtuple

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'invoker'
INFLUXDB_PASSWORD = 'xxxxxxxxxxxxx'
INFLUXDB_DATABASE = 'sensors'

MQTT_TOPIC = '/sensors/+'
MQTT_USER = 'xxx'
MQTT_PASSWORD = 'xxxx'
MQTT_ADDRESS = 'localhost'


influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

SensorData = namedtuple('SensorData', ['sensor', 'measurement', 'value'])

def on_connect(client, userdata, flags, rc):
    print('on connect...')
    client.subscribe(MQTT_TOPIC)

def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.sensor
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)

def on_message(client, userdata, msg):
    try:
        topic_parts = [row for row in msg.topic.split('/') if row !='']
        sensor = topic_parts[0]
        measurement = topic_parts[1]
        payload = float(msg.payload.decode('utf-8'))
        print(sensor, measurement, payload)
        print('*' * 100)
        sensor_data = SensorData(sensor, measurement, payload)
        _send_sensor_data_to_influxdb(sensor_data)
    except Exception as e:
        print(e)

    


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def main():
    _init_influxdb_database()
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883, 60)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    print('MQTT to InfluxDB...')
    main()
