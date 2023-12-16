import paho.mqtt.client as mqtt
import topics

class MQTTSubscriber:
    def __init__(self, broker, port, client_id, topics, on_message_callback=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.topics = topics
        self.on_message_callback = on_message_callback
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if(str(rc) == '0'):
            print("Connected Succesfully!")
        # Subscribe to topics here
        for type, tpcs in self.topics.items():
            print(f"Subscribing to all topics in {type}:")
            for desc, topic in tpcs.items():
                self.client.subscribe(topic)
                print(f"subscribing to {desc}: {topic}")

    def on_message(self, client, userdata, msg):
        if self.on_message_callback:
            self.on_message_callback(msg.topic, msg.payload)
    
    def on_disconnect(self, client, userdata, rc):
        print("Disconnected!")

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
            
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic)
        
    def run(self):
        while True:
            user_input = input()
            if user_input.lower() == "q":
                break

            self.publish("topic1", user_input)
        self.client.disconnect()

# def on_message_callback(topic, payload):
#     print("Received message on topic '{}': {}".format(topic, payload))


# BROKER_ADDRESS = "192.168.43.145"
# BROKER_PORT = 1883
# client = MQTTSubscriber(BROKER_ADDRESS, BROKER_PORT, "sub", topics.sensors, on_message_callback)
# client.connect()
# client.run()