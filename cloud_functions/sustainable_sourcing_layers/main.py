import json
import ee
from flask import jsonify
import functions_framework
import logging
import os
import requests

import google.auth
import google.cloud.logging
from google.api_core import retry

from suso_layers_2025a import get_areas_image

client = google.cloud.logging.Client()
client.setup_logging()

@retry.Retry()
def get_suso_stats(geojson):
    """Get area stats for the provided geojson polygon."""
    region = ee.Geometry(geojson)
    feature_area = ee.Number(region.area(10))
    suso_image = get_areas_image()
    # Sum of pixel areas in square meters.
    stats = suso_image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=10
    )
    # Gini index.
    # See https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity.
    crop_names = ['forest', 'cocoa', 'coffee', 'palm', 'rubber']
    gini = ee.Number(1).subtract(ee.List(
        [ee.Number(stats.get(c)).divide(feature_area) for c in crop_names]
    ).reduce(ee.Reducer.sum()))
    # Update the EE dictionary.
    stats = stats.set('gini', gini).set('total_area', feature_area)
    # Request the result to the client and return it.
    return stats.getInfo()


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
