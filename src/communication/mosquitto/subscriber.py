import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker_address, port):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.broker_address = broker_address
        self.port = port
        self.message=None

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("ManualControl")

        
    def on_message(self, client, userdata, message):
        print("Message received: " + message.topic + " : " + str(message.payload.decode()))
        # Here goes the logic for handling the different messages
        self.message=str(message.payload.decode())
   
    def connect(self):
        self.client.connect(self.broker_address, port=self.port)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_messge(self):
        return self.message