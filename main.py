import boto3,json
from flask import Flask, request, jsonify
from datetime import datetime
import os

#SQS_QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/145023112744/email-processing-queue"

app = Flask(__name__)

def get_token_from_ssm(token_name):
    ssm = boto3.client("ssm", region_name="us-east-2")
    response = ssm.get_parameter(
        Name=token_name,
        WithDecryption=True
    )
    return response["Parameter"]["Value"]

EXPECTED_TOKEN = get_token_from_ssm("email-api-token")
SQS_QUEUE_URL = get_token_from_ssm("sqs_queue_url_parameter")

@app.route("/send", methods=["POST"])
def receive_email():
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "Missing JSON payload"}), 400

    token = payload.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    if token != EXPECTED_TOKEN:
        return jsonify({"error": "Invalid token"}), 401

    data = payload.get("data")
    if not data or "email_timestream" not in data:
        return jsonify({"error": "Missing email_timestream"}), 400

    try:
        timestamp = int(data["email_timestream"])
        datetime.fromtimestamp(timestamp) 
    except (ValueError, OSError):
        return jsonify({"error": "Invalid email_timestream format"}), 400

    sqs = boto3.client("sqs", region_name="us-east-2")

    try:
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(payload["data"])
        )
        return jsonify({"message": "Message sent to SQS"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to send to SQS", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
