from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'invoker', 'xxxxx', 'sensors')

light    = client.query('SELECT last(value) as value FROM sensors.autogen.light    WHERE time > now() - 2h;').get_points().next()['value']
co2      = client.query('SELECT last(value) as value FROM sensors.autogen.co2      WHERE time > now() - 2h;').get_points().next()['value']
humidity = client.query('SELECT last(value) as value FROM sensors.autogen.humidity WHERE time > now() - 2h;').get_points().next()['value']
shd      = client.query('SELECT last(value) as value FROM sensors.autogen.shd      WHERE time > now() - 2h;').get_points().next()['value']
temp     = client.query('SELECT last(value) as value FROM sensors.autogen.temp     WHERE time > now() - 2h;').get_points().next()['value']
wnd      = client.query('SELECT last(value) as value FROM sensors.autogen.wnd      WHERE time > now() - 2h;').get_points().next()['value']

print('light   :'+str(light    )) 
print('co2     :'+str(co2      )) 
print('humidity:'+str(humidity )) 
print('shd     :'+str(shd      )) 
print('temp    :'+str(temp     )) 
print('wnd     :'+str(wnd      )) 
