# test_connect.py
import paho.mqtt.client as mqtt
import time

# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", rc)


def on_publish(client, userdata, result):
        print('data published - {}'.format(result))


client = mqtt.Client('weatherpi')
client.on_connect = on_connect
client.on_publish = on_publish
client.connect("192.168.1.148", 1883, 60)
for i in range(5):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    ret = client.publish('weatherpi/weather', payload=i, qos=0, retain=False)
    print("send {} to raspberry/topic, result {}".format(i, ret))
    time.sleep(1)

client.loop_forever()
