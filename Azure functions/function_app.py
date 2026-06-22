import json
import logging
import os
import azure.functions as func
import redis

# Initialize the Azure Function App
app = func.FunctionApp()

# Global Redis Client (Reused across executions for high performance)
redis_client = redis.Redis(
    host=os.environ.get("iotEdge.norwayeast.redis.azure.net:10000"),
    port=6380,                         # Default SSL port for Azure Cache for Redis
    password=os.environ.get("1vwH8A7PJjTgeGhbi92yDudYcQMuAuiIgAZCAAj8vmA="),
    ssl=True,                          # Required for secure cloud connections
    decode_responses=True,             # Automatically decodes data to strings
)

@app.event_hub_trigger(
    arg_name="events",
    event_hub_name="messages/events",  # Default telemetry path for IoT Hubs
    connection="HostName=myiothubjdv123.azure-devices.net;DeviceId=myraspi;SharedAccessKey=4TpIfX8PWF+vm8o0LIqGaQvikfSZJevUe96t87AH1So=",
)
def iot_hub_to_redis_trigger(events: list[func.EventData]):
    """Processes incoming batches of IoT Hub telemetry and caches them in Redis."""
    for event in events:
        try:
            # Decode the raw event body sent by your simulator
            payload = json.loads(event.get_body().decode("utf-8"))
            device_id = payload.get("deviceId")

            if not device_id:
                logging.warning("Skipping event: Missing 'deviceId'")
                continue

            # Store the latest metrics using a Redis Hash structure
            redis_key = f"device:state:{device_id}"
            redis_client.hset(
                redis_key,
                mapping={
                    "temperature": payload.get("temperature"),
                    "humidity": payload.get("humidity"),
                    "timestamp": payload.get("timestamp"),
                },
            )
            
            logging.info(f"Successfully cached state for device: {device_id}")

        except Exception as e:
            logging.error(f"Error processing IoT event: {e}")
