import os
from pydoc_data.topics import topics
import subprocess
import sys

from db.insertData import ResQBotDatabase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','communication', 'mosquitto')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','gui')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','db')))
from dotenv import dotenv_values
import subMQTT as mqtt
from gui import GUI
from radar import RadarGridVisualizer

#to create the db
subprocess.call(['bash', 'src/db/startScript.sh'])
# from db import ResQBotDatabase
display = RadarGridVisualizer()
db = ResQBotDatabase()
def on_message(topic, payload):
    if(topic == topics.sensors['sensors']['radar']):
        tempd = payload.decode()[:5]
        tempa = payload.decode()[5:]
        try:
            a = float(tempa)
        except ValueError:
            a = 0
        try:
            d = float(tempd)
        except ValueError:
            d = -1
        display.draw_line_and_targets(a, d)
        db.add_obstacles(a,d)


env_vars = dotenv_values()
BROKER_ADDRESS = env_vars['BROKER_ADDRESS']
PORT = int(env_vars['PORT'])
client = mqtt.MQTTSubscriber(BROKER_ADDRESS, PORT, "robot-1", topics.sensors, on_message)
client.connect()
CC_GUI=GUI()
CC_GUI.create_window()

client.disconnect()



