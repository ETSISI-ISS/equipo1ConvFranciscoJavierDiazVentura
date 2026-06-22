import random
import json
import time
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=myiothubjdv123.azure-devices.net;DeviceId=myraspi;SharedAccessKey=4TpIfX8PWF+vm8o0LIqGaQvikfSZJevUe96t87AH1So="

client = IoTHubDeviceClient.create_from_connection_string(
    CONNECTION_STRING
)

client.connect()

print("Dispositivo conectado")
devices = ["device-01", "device-02", "device-03", "device-04", "device-05"]

while True:
    for device_id in devices:
        temperatura = round(random.uniform(17, 35), 2)
        humedad = round(random.uniform(30, 90), 2)

        payload = {
            "deviceId": device_id,
            "temperature": temperatura,
            "humidity": humedad,
            "timestamp": int(time.time() * 1000)
        }

        mensaje = Message(json.dumps(payload))
        client.send_message(mensaje)

        print(f"Enviado [{device_id}]: {payload}")

    time.sleep(100)
