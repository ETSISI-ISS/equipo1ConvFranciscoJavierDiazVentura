# send_event.py
import time
from azure.iot.device import IoTHubDeviceClient, Message

# Replace this with your actual connection string
CONNECTION_STRING = "HostName=myiothubAFM.azure-devices.net;DeviceId=esp32test;SharedAccessKey=bIs83ed9mzbYDL5iw3zNfaZFmaMQeaUOFH8eqxmbs+8="

# Example telemetry data
TEMPERATURE = 22.5
HUMIDITY = 60

def main():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("IoT Hub device sending periodic messages... Press Ctrl-C to exit")

    try:
        while True:
            # Create a JSON message
            msg_txt = '{{"temperature": {temp:.2f}, "humidity": {hum:.2f}}}'.format(
                temp=TEMPERATURE, hum=HUMIDITY
            )
            message = Message(msg_txt)
            message.content_type = "application/json"
            message.content_encoding = "utf-8"

            print("Sending message:", msg_txt)
            client.send_message(message)
            print("Message successfully sent\n")
            time.sleep(5)

    except KeyboardInterrupt:
        print("IoT Hub client stopped")

if __name__ == "__main__":
    main()
    