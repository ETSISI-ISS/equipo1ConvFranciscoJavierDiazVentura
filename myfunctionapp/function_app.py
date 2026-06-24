import json
import logging
import azure.functions as func
import os
import redis

redis_client = None
app = func.FunctionApp()

@app.function_name(name="StreamAnalyticsFunction")
@app.stream_analytics_input(
    name="input",
    data_type=func.DataType.STRING  # ASA always sends JSON string
)
def stream_analytics_function(input: str):

    global redis_client

    if redis_client is None:
        redis_client = redis.StrictRedis(
            host=os.getenv("RedisHost"),
            port=int(os.getenv("RedisPort")),
            password=os.getenv("RedisKey"),
            ssl=True
        )

    logging.info(f"Received from Stream Analytics: {input}")

    # ASA sends a JSON array string
    data = json.loads(input)[0]

    redis_client.set("asa_latest_message", json.dumps(data))

    logging.info("Saved message to Redis.")
