import os
from datetime import datetime

import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    with open("log_file.txt", "a") as log_file:
        log_file.write("Connected with result code " + str(rc) + " " + str(datetime.now()) + '\n')
        log_file.flush()
        os.fsync(log_file.fileno())

    client.subscribe("logs")
    client.subscribe("bet_manager/working")


def on_message(client, userdata, msg):
    message = f"Received MQTT message: topic={msg.topic}, payload={msg.payload.decode()}"
    print(message)

    with open("log_file.txt", "a") as log_file:
        log_file.write(message + '\n')
        log_file.flush()
        os.fsync(log_file.fileno())


client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_start()


def main():
    while True:
        pass


if __name__ == "__main__":
    main()