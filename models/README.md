# Introduction

In support of the Forest Data Partnership, we created 10-meter resolution raster datasets mapping key commodity crops: palm, rubber, cocoa, coffee, natural forest, and other land cover. Our approach involved pooling community reference data from both open and proprietary sources, which were combined with terrain (slope) data and annual composites of Sentinel-1, Sentinel-2, and Palsar imagery to generate training data. These training datasets were then input to a machine learning model, which was subsequently applied to generate semi-global maps of commodity probability for the years 2017-2023. The resulting datasets provide a valuable resource for assessing and monitoring supply chain sustainability, particularly in regions where existing data is limited or inconsistent.

# Methods

## Land Cover Categories

Here we focus on a subset of commodities specifically named in the EUDR.  These are:

- Palm
- Rubber
- Cocoa
- Coffee
- Natural/Primary Forest
- Other Land Cover (anything not in the previous categories)

We make no effort to precisely define these classes other than to note that our goal is to predict the conditional probability (given the inputs described below) of the presence of these categories in any given pixel.  Logically, these need not sum to one, as agroecological systems can be composed of multiple canopy layers (e.g. sub-canopy grown coffee) and/or intercropping horizontally, resulting in vertically mixed pixels at the 10 meter scale.  "Forest" and "other" categories are present for completeness and are based on pseudo-training data (derived from other products).  We describe the accuracy of such products elsewhere, for example Forest Data Partnership (2024a) and Brown et al. (2022).

## Inputs

The predictors are annual composites built from publicly available satellite imagery provided by Sentinel-1, Sentinel-2, and ALOS-2, with terrain data from Copernicus (GLO-30). Specifically, the following Sentinel-2 Top-of-atmosphere (TOA) reflectance bands were used: B1, B2, B3, B4, B5, B6, B7, B8, B8A, B9, B10, B11, B12. TOA reflectance data were used due to the increased availability of TOA data compared to data products with a higher level of processing, surface reflectance for example. We built annual composites by taking the cloud-masked mean for all bands for all available imagery in a calendar year, deduplicating redundant imagery by Sentinel-2 datatake. The Cloud Score+ dataset (Pasquarella et al. 2023) was used for the cloud mask, with a 0.5 threshold on the ’cs_cdf’ band. The means were scaled to reflectance in approximately [0, 1] and no further normalization was performed. Sentinel-1 data were selected from interferometric wide-swath scenes that included both VV (vertical-vertical) and VH (vertical-horizontal) polarizations in both ascending and descending orbital paths. Radiometric compensation for terrain using the volume scattering model described by Vollrath et al. (2020) was used to preprocess backscattering coefficients. For a calendar year, minimum, maximum, mean, and standard deviation of backscatter were computed at each polarization and subsequently stretched to decibels. Palsar-2 annual composites, containing HH and HV polarizations at 25 meters resolution (Shimada et al., 2014), were bilinearly resampled, gap filled with the rolling 3-year mean of annual composites, and converted to scaled decibels. Slope was derived from the Copernicus GLO-30 DEM. Slopes were scaled to [0, 1] with no further normalization. In a given calendar year, the eight Sentinel-1 statistics (min, max, mean, and SD for both VV and VH) were stacked with the 13 Sentinel-2 band means, the two Palsar-2 bands (HH and HV) and slope to create the annual input composites.

## Training and Validation data

Data sources include: 

| Data Type  | Description | Reference |
| ------------- | ------------- | ------------- |
| foo | foo | foo |


Data from all sources were pooled (n=8,081,825) and overlaid on annual composites according to the year in which the reference data were generated, resulting in the following distribution by label:

| Commodity  | N |
| ------------- | ------------- |
| cocoa | 1254287 |
| coffee | 1680058 |
| forest | 1376774 |
| other | 1046046 |
| palm | 1280226 |
| rubber | 1444434 |

The geographic distribution of the data is uneven, with some areas well represented in the training data, others at intermediate levels and others not at all.  This is illustrated in the following heat map of data density by degree.

![training data heatmap](/assets/images/training_data_heatmap.png)

A 1/10 degree grid (n=373,700) was created over the one degree cells in which pooled data were present.  For each point in the grid, the closest pooled data point less than 1/20 of a degree from the grid point was selected, regardless of label.  If no point was closer than 1/20 of a degree to the grid point, the grid point was discarded.  This resulted in a geographically representative sample (n=210,768) from the pooled dataset with the following distribution by label:

| Commodity  | N |
| ------------- | ------------- |
| cocoa | 1291 |
| coffee | 195 |
| forest | 41010 |
| other | 165476 |
| palm | 1201 |
| rubber | 1595 |

This sample was treated as a test set, and set aside for the remainder of the analysis.  In addition, Descals et al. (2024) and Sheil et al. (2024) datasets were used as validation for the palm and rubber classes, respectively.  The sampled training data were combined with Descals and Sheil data to create a pooled test/validation dataset.  To minimize spatial autocorrelation between training and the test/validation sets, points in the pooled dataset within one kilometer of any point in the pooled test/validation dataset were discarded.  This resulted in a training dataset (n=7,454,512) with the following label distribution:

| Commodity  | N |
| ------------- | ------------- |
| cocoa | 1199279 |
| coffee | 1556099 |
| forest | 1304617 |
| other | 857207 |
| palm | 1206076 |
| rubber | 1331234 |

The following illustrates the 1/10 degree grid, the test sample and the training data.

![grid, test and training data](/assets/images/grid_test_training.png)

## Models

We trained single class models for palm, rubber, cocoa and coffee. We used the training dataset described above with the target variable re-coded for a binary classification problem (e.g. palm and not-palm).  The test dataset was also re-coded for accuracy assessment.  Accuracies of cocoa and coffee models were assessed relative to the test set sampled from the training data.  Palm model accuracy was assessed relative to the test set and the Descals et al. (2024) dataset.  Rubber accuracy was assessed relative to the test set and the Sheil et al. (2024) dataset.

During model selection, the training dataset was randomly partitioned to 80% training, 19% hyperparameter tuning and model selection.  Although 1% data were used as a test set to evaluate the selected model accuracy, that was only because we could not specify 0% for random test data.  The test/validation data were not observed during this process.

The model type is a deep neural network which exports a vector of estimated class probabilities, in the multi-class case, and a binary output for single class models. It is a per-pixel model in which the input is 1x1xC (for C bands) vector and the output is the estimated conditional class probability given the vector of covariates (xt) at time t. The architecture, activation function, optimization function, learning rate, batch size, training iterations and other parameters of the models and training configurations were chosen automatically using a hyperparameter search performed on infrastructure similar to [Google Cloud AutoML](https://cloud.google.com/automl).  The models were allowed to spend up to 24 hours each on hyperparameter tuning and training.

## Mapping Methodology
The trained models were hosted on Google Vertex AI using 5-10 compute nodes of n1-standard-32 CPU machines and no accelerators.  Input imagery (pre-computed to minimize latency during inference) was forwarded from Google Earth Engine to the models on Vertex AI in serialized TensorFlow Example format over gRPC in [1,1] tiles. 

# Results
The results are viewable using [this Earth Engine link](https://code.earthengine.google.com/05c8429a558ae59ae698d260b2168ecb) in the following collections:

| Commodity  | Earth Engine collection |
| ------------- | ------------- |
| cocoa | `ee.ImageCollection("projects/forestdatapartnership/assets/cocoa/model_2025a")` |
| coffee | `ee.ImageCollection("projects/forestdatapartnership/assets/coffee/model_2025a")` |
| palm | `ee.ImageCollection("projects/forestdatapartnership/assets/palm/model_2025a")` |
| rubber | `ee.ImageCollection("projects/forestdatapartnership/assets/rubber/model_2025a")` |

## Accuracy assessment

We assess accuracy of single class models as curves of accuracy, precision, recall and F1 score by threshold on probability output.  The intersection of precision and recall, the maximum of the F1 score, and its corresponding threshold we present as global accuracy, but note that these statistics vary both with choice of threshold and geographically.

### Palm accuracy on test set
Precision and recall ~78% at 0.88 threshold.
![palm test accuracy](/assets/images/palm_test_accuracy.png)

### Palm accuracy on Descals et al. (2024) validation set
Precision and recall ~82% at 0.89 threshold.
![palm descals accuracy](/assets/images/palm_descals_accuracy.png)

### Rubber accuracy on test set
Precision and recall ~80% 0.59 threshold.
![rubber test accuracy](/assets/images/rubber_test_accuracy.png)

### Rubber accuracy on Sheil et al. (2024) validation set
Precision and recall ~76% 0.23 threshold.
![rubber sheil accuracy](/assets/images/rubber_sheil_accuracy.png)

### Cocoa accuracy on test set
Precision and recall ~87% 0.96 threshold.
![cocoa test accuracy](/assets/images/cocoa_test_accuracy.png)

### Coffee accuracy on test set*
Precision and recall ~54% 0.99 threshold.  (*Small sample size.)
![coffee test accuracy](/assets/images/coffee_test_accuracy.png)

# Limitations

Model output is limited to selected countries as calendar year composites for 2020 and 2023. Not all regions of the output are well represented by training data. Accuracy is reported in aggregate, and will vary geographically and with user chosen thresholds. Sensor artifacts based on data availability, cross-track nonuniformity, or cloudiness may be visually apparent in output probabilities and result in classification errors at some thresholds.

# References

