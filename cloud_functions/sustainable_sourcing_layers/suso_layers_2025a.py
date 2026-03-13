import os

import ee
import google.auth
from google.api_core import retry

# First, initialize.
credentials, _ = google.auth.default(
    scopes=['https://www.googleapis.com/auth/earthengine']
)
ee.Initialize(
  credentials,
  project=os.environ['GOOGLE_CLOUD_PROJECT'],
  opt_url='https://earthengine-highvolume.googleapis.com'
)

# See https://github.com/google/forest-data-partnership/tree/main/models.
cocoa_2025a = ee.ImageCollection('projects/forestdatapartnership/assets/cocoa/model_2025a')
coffee_2025a = ee.ImageCollection('projects/forestdatapartnership/assets/coffee/model_2025a')
palm_2025a = ee.ImageCollection('projects/forestdatapartnership/assets/palm/model_2025a')
rubber_2025a = ee.ImageCollection('projects/forestdatapartnership/assets/rubber/model_2025a')

filter2020 = ee.Filter.calendarRange(2020, 2020, 'year')
filter2023 = ee.Filter.calendarRange(2023, 2023, 'year')

cocoa2020 = cocoa_2025a.filter(filter2020).mosaic().rename('cocoa_2020')
cocoa2023 = cocoa_2025a.filter(filter2023).mosaic().rename('cocoa_2023')
coffee2020 = coffee_2025a.filter(filter2020).mosaic().rename('coffee_2020')
coffee2023 = coffee_2025a.filter(filter2023).mosaic().rename('coffee_2023')
palm2020 = palm_2025a.filter(filter2020).mosaic().rename('palm_2020')
palm2023 = palm_2025a.filter(filter2023).mosaic().rename('palm_2023')
rubber2020 = rubber_2025a.filter(filter2020).mosaic().rename('rubber_2020')
rubber2023 = rubber_2025a.filter(filter2023).mosaic().rename('rubber_2023')

# See https://eartharxiv.org/repository/view/9085/.
natural_forest2020 = ee.ImageCollection(
    'projects/computing-engine-190414/assets/biosphere_models/public/forest_typology/natural_forest_2020_v1_0'
  ).mosaic().divide(255).selfMask()

# THRESHOLDS FOR DEMONSTRATION ONLY! Tune these to your needs.
thresholds = {
    'forest': 0.5,
    'cocoa': 0.45,
    'coffee': 0.96,
    'palm': 0.89,
    'rubber': 0.5
}

# A mini-ensemble of GDM and fodapa data products.
ensemble = ee.Image.cat(
  natural_forest2020.rename('forest'),
  cocoa2020.rename('cocoa'),
  coffee2020.rename('coffee'),
  palm2020.rename('palm'),
  rubber2020.rename('rubber')
).unmask(0)

# Threshold the probabilities.  THRESHOLDS FOR DEMONSTRATION ONLY!
crop_names = list(thresholds.keys())
threshold_values = list(thresholds.values())
thresholded = ensemble.select(crop_names).gt(ee.Image(threshold_values))

# Unclassified means no predicted presence at the specified thresholds.
unclassified = thresholded.reduce('sum').eq(0).rename('unclassified')

# Confusion means two or more classes predicted presence.
confusion = thresholded.reduce('sum').gt(1).selfMask().rename('confusion')

def get_suso_layers_2025a() -> ee.Image:
    '''Returns the stack of probability images in separate bands.'''
    return ee.Image.cat(
        natural_forest2020.rename('natural_forest_2020'),
        cocoa2020.rename('cocoa_probability_2020'),
        cocoa2023.rename('cocoa_probability_2023'),
        coffee2020.rename('coffee_probability_2020'),
        coffee2023.rename('coffee_probability_2023'),
        palm2020.rename('palm_probability_2020'),
        palm2023.rename('palm_probability_2023'),
        rubber2020.rename('rubber_probability_2020'),
        rubber2023.rename('rubber_probability_2023'),
    )

def get_areas_image() -> ee.Image:
    '''Returns data for area calculations in square meters.'''
    return ee.Image.cat(
      thresholded,
      unclassified.rename('unclassified'),
      confusion.rename('confusion')
    ).multiply(ee.Image.pixelArea())

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