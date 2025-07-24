import json
import ee
from flask import jsonify
import functions_framework
import logging
import os
import requests

import google.auth
import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()

@functions_framework.http
def main(request):
  """Handle requests in a format (geojson) suitable for BigQuery."""
  credentials, _ = google.auth.default(
      scopes=['https://www.googleapis.com/auth/earthengine']
  )
  ee.Initialize(credentials, project=os.environ['PROJECT'])
  try:
    replies = []
    request_json = request.get_json(silent=True)
    calls = request_json['calls']
    for call in calls:
      geo_json = json.loads(call[0])
      try:
        logging.info([geo_json])
        response = get_suso_stats(geo_json)
        logging.info(response)
        replies.append(json.dumps(response))
      except Exception as e:
        logging.error(str(e))
        replies.append(json.dumps( { "errorMessage": str(e) } ))
    return jsonify(replies=replies, status=200, mimetype='application/json')
  except Exception as e:
    error_string = str(e)
    logging.error(error_string)
    return jsonify(error=error_string, status=400, mimetype='application/json')
