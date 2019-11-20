import time
import os
import yaml
import paho.mqtt.client as mqtt
import json
import queue
import logging

from lib.bt_scan import bt_scan
from lib.devices import devices
print("bt_monitor initializing")

# Update the mqtt state topic
def update_state(value, topic):
    logging.info("State change triggered: %s -> %s" % topic, value)

    client.publish(topic, value, retain=True)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info ("Connected to MQTT broker with result code: %s" % mqtt.connack_string(rc))
    client.subscribe(group_command_topic)
    client.subscribe(node_command_topic)

# The callback for when messages come in
def on_message(client, userdata, message):
    logging.debug("message received " ,str(message.payload.decode("utf-8")))
    logging.debug("message received " ,str(message.payload))
    logging.debug("message topic=",message.topic)
    logging.debug("message qos=",message.qos)
    logging.debug("message retain flag=",message.retain)
    if not RequestQueue.full():
        RequestQueue.put(message)
    else:
        logging.warning("The request queue full.  Scan request discarded")


# The callback for log messages
def on_log(client, userdata, level, buf):
    pass
  # The following line causes errors  
  #  logging.debug("MQTT-log: ",str(buf))

# The callback for subscription confirmations
def on_subscribe(client, userdata, mid, granted_qos):
    logging.info("Received subscription callback for topic number " + str(mid))


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.full_load(ymlfile)
### Set the logging level ###
logging.basicConfig(level=CONFIG['general']['LoggingLevel'])


### SETUP MQTT ###
user = CONFIG['mqtt']['user']
password = CONFIG['mqtt']['password']
host = CONFIG['mqtt']['host']
port = int(CONFIG['mqtt']['port'])
discovery = bool(CONFIG['mqtt'].get('discovery'))
group_command_topic = CONFIG['mqtt']['base_topic'] + "/" + CONFIG['mqtt']['command_topic']
node_command_topic = CONFIG['mqtt']['base_topic'] + "/" + CONFIG['mqtt']['publisher_id'] + "/" + CONFIG['mqtt']['command_topic']
status_topic = CONFIG['mqtt']['base_topic'] + "/" + CONFIG['mqtt']['publisher_id'] + "/" + CONFIG['mqtt']['status_topic']

logging.debug("group_command_topic = " + group_command_topic)  
logging.debug("node_command_topic = " + node_command_topic)
logging.debug("status_topic = " + status_topic)

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

client.loop_start()

### setup request queue ###
RequestQueue = queue.Queue(maxsize = int(CONFIG['general']['MaxQueueSize']))

### Set up dictionary of devices to scan
device_dict = devices()

LoopTime = int(CONFIG['general']['LoopTimer'])
ymlfile.close()

### SETUP END ###

### MAIN LOOP ###
if __name__ == "__main__":


    # Main loop
    num_loops = 0
    while True:
        while not RequestQueue.empty():
            message = RequestQueue.get()
            device_dict.update(message)
            msg_json = json.loads(str(message.payload.decode("utf-8")))

            if msg_json["cmd"] == "scan":
                scanner = device_dict.bt_scans[msg_json["Address"]]
                scanner.scan()
                if not scanner.ErrorOnScan:
                    client.publish(status_topic, scanner.results)
                    # If confidence != 0.0 and != 100.0 this means that the device wasn't seen
                    # but we haven't yet checked ScansForAway times for it.
                    # Enqueue another request for this message so it checks it again
                    if scanner.PreviousConfidence != 0.0 and scanner.PreviousConfidence != 100.0:
                       if not RequestQueue.full(): 
                           RequestQueue.put(message)
                       else:
                           logging.warning("The request queue is full. Discarding request.")
            else:
                # put other command types above this as elif's
                logging.warning("Command type " + msg_json["cmd"] + " is unknown. Ignoring command.")
 
        num_loops += 1
        logging.debug("Loop number " + str(num_loops))
        time.sleep(LoopTime)



