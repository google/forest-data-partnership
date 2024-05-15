"""Source code for a Cloud Function that calculates forest conversion risk for palm."""
import json
import ee
import google.auth


def main(request):
  """HTTP Cloud Function.

  Args:
      request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

  Returns:
      The response text, or any set of values that can be turned into a
      Response object using `make_response`
      <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
  """
  request_json = request.get_json(silent=True)
  region_geojson = request_json['region']

  credentials, _ = google.auth.default(
      scopes=['https://www.googleapis.com/auth/earthengine']
  )
  ee.Initialize(credentials)

  # JRC forest.  Just forest/nonForest.
  jrc_forest = ee.ImageCollection('JRC/GFC2020/V1')
  forest_2020 = jrc_forest.mosaic().unmask(0)

  p20 = ee.ImageCollection(
      'projects/forestdatapartnership/assets/palm/palm_2020_model_20240312'
  ).mosaic()
  p23 = ee.ImageCollection(
      'projects/forestdatapartnership/assets/palm/palm_2023_model_20240312'
  ).mosaic()

  # Assume that the Spearman rank correlation on the probabilities is a fair
  # approximation of the Pearson correlation between the unobserved states.
  # 100 meters is a magic number.
  correlation = (
      p20.addBands(p23)
      .reduceNeighborhood(**{
          'reducer': ee.Reducer.spearmansCorrelation(),
          'kernel': ee.Kernel.square(100, 'meters'),
      })
      .select('correlation')
  )

  one = ee.Image(1).rename('one')
  expectation20 = p20
  variance20 = p20.multiply(one.subtract(p20))
  expectation23 = p23
  variance23 = p23.multiply(one.subtract(p23))
  # P(p20, p23) = p11 = E[p20*p23]
  p11 = correlation.multiply(variance20.multiply(variance23).sqrt()).add(
      expectation20.multiply(expectation23)
  )

  # P(!p20, p23) = p01 = P(p23) - P(p20, p23) = p23 - p11
  to_palm = p23.subtract(p11)
  from_palm = p20.subtract(p11)
  # Pixel area in hectares.
  pixel_area = ee.Image.pixelArea().divide(100).divide(100)
  # Risk is probability times loss.  Here the "loss" is pixel area.
  to_palm_risk = pixel_area.multiply(to_palm)
  from_palm_risk = pixel_area.multiply(from_palm)

  areas = ee.Image.cat([pixel_area, to_palm_risk, from_palm_risk, forest_2020])
  group_index = areas.bandNames().length().subtract(1)
  areas_labels = ['Area (ha)', 'Area to palm (ha)', 'Area from palm (ha)']

  def get_risk_summary_feature(f):
    """Get a summary of risk by forest classes."""
    areas_dict = areas.reduceRegion(**{
        'reducer': (
            ee.Reducer.sum()
            .repeat(group_index)
            .group(**{
                'groupField': group_index,
                'groupName': 'forest',
            })
        ),
        'geometry': f.geometry(),
        'scale': 10,
    })
    groups = ee.List(areas_dict.get('groups'))

    def reformat(obj):
      """Reformat the output of the grouped reduction."""
      obj = ee.Dictionary(obj)
      sums = ee.List(obj.get('sum'))
      return ee.Dictionary.fromLists(areas_labels, sums).set(
          'forest', obj.get('forest')
      )

    return groups.map(reformat)

  input_feature = ee.Feature(region_geojson)
  return json.dumps(get_risk_summary_feature(input_feature).getInfo())
