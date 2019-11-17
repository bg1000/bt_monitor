import time
import os
import yaml
import paho.mqtt.client as mqtt
import json
import queue

from lib.bt_scan import bt_scan
from lib.devices import devices
print("bt_monitor initializing")

# Update the mqtt state topic
def update_state(value, topic):
    print ("State change triggered: %s -> %s" % topic, value)

    client.publish(topic, value, retain=True)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print ("Connected to MQTT broker with result code: %s" % mqtt.connack_string(rc))
    client.subscribe(group_command_topic)
    client.subscribe(node_command_topic)

# The callback for when messages come in
def on_message(client, userdata, message):
 #   print("message received " ,str(message.payload.decode("utf-8")))
 #  print("message received " ,str(message.payload))
 #   print("message topic=",message.topic)
 #   print("message qos=",message.qos)
 #   print("message retain flag=",message.retain)
    client.publish(status_topic, "message received")
    if not RequestQueue.full():
        RequestQueue.put(message)
    else:
        print("The request queue full.  Scan request discarded")


# The callback for log messages
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# The callback for subscription confirmations
def on_subscribe(client, userdata, mid, granted_qos):
    print("Received subscription callback for topic number " + str(mid))


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.full_load(ymlfile)

### SETUP MQTT ###
user = CONFIG['mqtt']['user']
password = CONFIG['mqtt']['password']
host = CONFIG['mqtt']['host']
port = int(CONFIG['mqtt']['port'])
discovery = bool(CONFIG['mqtt'].get('discovery'))
group_command_topic = CONFIG['mqtt']['base_topic'] + "/" + CONFIG['mqtt']['command_topic']
node_command_topic = CONFIG['mqtt']['base_topic'] + "/" + CONFIG['mqtt']['publisher_id'] + "/" + CONFIG['mqtt']['command_topic']
status_topic = CONFIG['mqtt']['base_topic'] + "/" + CONFIG['mqtt']['publisher_id'] + "/" + CONFIG['mqtt']['status_topic']

#print ("group_command_topic = " + group_command_topic)  
#print ("node_command_topic = " + node_command_topic)
#print ("status_topic = " + status_topic)

if 'discovery_prefix' not in CONFIG['mqtt']:
    discovery_prefix = 'homeassistant'
else:
    discovery_prefix = CONFIG['mqtt']['discovery_prefix']

client = mqtt.Client(client_id="bt_monitor_" + CONFIG['mqtt']['publisher_id'], clean_session=True, userdata=None, protocol=4)

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.on_subscribe = on_subscribe

client.username_pw_set(user, password=password)
client.connect(host, port, 60)

ymlfile.close()
client.loop_start()

### setup request queue ###
# MaxQueueSize = int(CONFIG['general']['MaxQueueSize'])
RequestQueue = queue.Queue(maxsize=30)

### Set up dictionary of devices to scan
device_dict = devices()



### SETUP END ###

### MAIN LOOP ###
if __name__ == "__main__":


#
# decide if you want to do something here
#
#        if discovery is True:
#            base_topic = discovery_prefix + "/cover/" + doorCfg['id']
#            config_topic = base_topic + "/config"
#            doorCfg['command_topic'] = base_topic + "/set"
#            doorCfg['state_topic'] = base_topic + "/state"
    # Main loop
    num_loops = 0
    while True:
        while not RequestQueue.empty():
            message = RequestQueue.get()
            device_dict.update(message)
            msg_json = json.loads(str(message.payload.decode("utf-8")))

            # need to verify message.topic
#            print("cmd = " + msg_json["cmd"])
#            print("DeviceName = " + msg_json["DeviceName"])
#            print("Address = " + msg_json["Address"])

            # Create bt_scan object and request a scan
#           scanner = bt_scan("hci0", msg_json["DeviceName"], msg_json["Address"], msg_json["ScansForAway"])
            address = msg_json["Address"]
            scanner = device_dict.bt_scans[address]
            scanner.scan()
            if not scanner.ErrorOnScan:
                client.publish(status_topic, scanner.results)
 
 
        num_loops += 1
        print("Loop number " + str(num_loops))
        time.sleep(5)



