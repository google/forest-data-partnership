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

Datasets were aggregated from diverse sources as described in the following table.  Where possible, ostensibly pure polygons of commodity presence were cross-referenced with ancillary data products to exclude potential areas of non-trees, or natural forests.  These datasets include the cocoa farming map by N. Kalishek et al. (2023), the Cote d' Iviore land cover map (BNETD Land Cover Map 2020), Dynamic World (Brown et al. 2022), Forest Persistence (Forest Data Partnership 2024), WorldCover (Zanaga et al. 2021) and/or MapBiomas land cover (Souza et al. 2020).

Data sources include: 

|               |               |                                   |                                                                                                                                                                                                                                                                                                           |                                            |
| :-----------: | :-----------: | :-------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------: |
|   **Crop**    |   **Year**    |   **Region**                      |   **Description**                                                                                                                                                                                                                                                                                         |   **Reference**                            |
|   cocoa       |   2024        |   Cameroon                        |   Cocoa field data in Cameroon collected through the COCAFORI project, collected in March 2024                                                                                                                                                                                                            |   Shapiro (2024)                           |
|   cocoa       |   2023        |   Cameroon                        |   CIRAD provided publicly available inventory of trees in 223 agroforestry cocoa plantations in Cameroon                                                                                                                                                                                                  |   Lescuyer (2024)                          |
|   cocoa       |   2023        |   Ghana, Cote d'Ivoire, Liberia   |   Manually digitized points based on Google Earth imagery and other reference data.                                                                                                                                                                                                                       |   Tarrio (2025a)                           |
|   cocoa       |   2023        |   Indonesia                       |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   cocoa       |   2023        |   Indonesia                       |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   cocoa       |   2023        |   Ecuador                         |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   cocoa       |   2023        |   Colombia                        |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   cocoa       |   2023        |   Ecuador                         |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   cocoa       |   2023        |   Brazil                          |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   cocoa       |   2023        |   Ghana                           |   Cocoa ground data (GPS points) collected in the field by researchers of CERSGIS as part of a Lacuna Fund project.                                                                                                                                                                                       |   CERSGIS (2025)                           |
|   cocoa       |   2023        |   Brazil                          |   Validation data for the Map Biomas Cacau project (2023).                                                                                                                                                                                                                                                |   MapBiomas Cacau (2023)                   |
|   cocoa       |   2020        |   Peru                            |   Cacao polygons in Ucayali Peru, delineated based on the interpretation of satellite imagery from 2020; part of a NASA SERVIR Amazonia project.                                                                                                                                                          |   Becerra et al. (2022)                    |
|   cocoa       |   2020        |   Ghana, Cote d'Ivoire            |   WRI developed the West Africa Cocoa dataset (WAC) in collaboration with the World Cocoa Foundation and 19 chocolate companies who contributed supply locations. Data consists of 839,242 plots over Ghana and Cote d' Ivoire, originally collected in situ / manually by GPS-tracing plot boundaries.   |   Schenider (2023)                         |
|   coffee      |   2023        |   Colombia                        |   Internal Google polygon annotations                                                                                                                                                                                                                                                                     |   Google (2024)                            |
|   coffee      |   2023        |   Honduras                        |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Brazil                          |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Brazil                          |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2020        |   Brazil                          |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Hawaii                          |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Jamaica                         |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Tanzania                        |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Mexico                          |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Vietnam                         |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Kenya                           |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                                                 |   Tarrio (2025b)                           |
|   coffee      |   2023        |   Ethiopia                        |   Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia.                                                                                                                                                                                                         |   Meridia (2025)                           |
|   coffee      |   2023        |   Uganda                          |   Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia.                                                                                                                                                                                                         |   Meridia (2025)                           |
|   coffee      |   2023   |   Indonesia                       |   Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia.                                                                                                                                                                                   |   Meridia (2025)                         |
|   coffee      |   2023   |   Vietnam                         |   Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia.                                                                                                                                                                                   |   Meridia (2025)                         |
|   coffee      |   2023   |   Colombia                        |   CIAT provided coffee plot data in Colombia                                                                                                                                                                                                                                        |   CIAT (2025)                            |
|   forest      |   2020   |   Global                          |   Forest pseudo-positives sampled from Forest Persistence Forest Data Partnership 2024) thresholded at 0.95 and ETH Canopy Height map (Lang et al. 2023) thresholded at 30m (both for 2020).                                                                                        |   Tarrio (2025c)                         |
|   negatives   |   2023   |   Colombia                        |   CIAT provided plot data in Colombia                                                                                                                                                                                                                                               |   CIAT (2025)                            |
|   negatives   |   2020   |   Global                          |   Labeled non-tree data (Tarrio 2024a, Stanimirova 2023). Non-tree = urban, water, grassland, herbaceous cropland, etc. No shrubs.                                                                                                                                                  |   Tarrio (2025a), Stanimirova 2023       |
|   negatives   |   2020   |   Global                          |   Ktarrio generated non-tree (i.e. not forest, shrub or mangroves) 'other' / 'negative' samples in the overlap between ESA's WorldCover map for 2020 and Dynamic World's 2020 map                                                                                                   |   Tarrio (2025c)                         |
|   palm        |   2023   |   Malaysia                        |   Tijs Lips (Bunge) provided some hand-made points (in his personal capacity).                                                                                                                                                                                                      |   Clinton et al. (2024)                  |
|   palm        |   2017   |   Global                          |   Reference data points collected for a global oil palm project for 2017, originally presented at the 2019 Living Planet Symposium in Milan                                                                                                                                         |   Vollrath (2019)                        |
|   palm        |   2021   |   Global                          |   Point data generated by Google Crowd Compute                                                                                                                                                                                                                                      |   Clinton et al. (2024)                  |
|   palm        |   2017   |   Indonesia, Malaysia, Thailand   |   Point data from Olga Danylo / IIASA of oil palm across three countries in Southeast Asia                                                                                                                                                                                          |   Danylo (2021)                          |
|   palm        |   2023   |   Ghana, Cote d'Ivoire, Liberia   |   Manually digitized points based on Google Earth imagery and other reference data.                                                                                                                                                                                                 |   Tarrio (2025a)                         |
|   palm        |   2020   |   Peru                            |   A team of faculty and student researchers at JPL/California Polytechnic State University used Maxar and Planetscope imagery along with the Descals et al. 2019 model to hand digitize oil palm plantations. The imagery covered 2019 and 2020 for the Ucayali Province in Peru.   |   Cooley (2021)                          |
|   palm\*      |   2021   |   Global                          |   Publicly available validation data from Descals et al. (2024) as 18,736 10-meter samples of palm (1) or not palm (0) in 2021.                                                                                                                                                     |   Descals (2024a)                        |
|   rubber      |   2023   |   Ghana, Cote d'Ivoire, Liberia   |   Manually digitized points based on Google Earth imagery and other reference data.                                                                                                                                                                                                 |   Tarrio (2025a)                         |
|   rubber      |   2023   |   Guatemala                       |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                           |   Tarrio (2025b)                         |
|   rubber      |   2020   |   China                           |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                           |   Tarrio (2025b)                         |
|   rubber      |   2023   |   Sri Lanka                       |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                           |   Tarrio (2025b)                         |
|   rubber      |   2020   |   Nigeria                         |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                           |   Tarrio (2025b)                         |
|   rubber      |   2023   |   DRC                             |   Manually digitized polygons over commodities using imagery available from Google Earth, StreetView, and corroborating evidence for commodity presence (i.e. websites for commercial-scale farms); polygons converted to lattice at 10 meter resolution.                           |   Tarrio (2025b)                         |
|   rubber      |   2023   |   Southeast Asia                  |   Ate Poortinga (of SIG / Spatial Informatics Group) used openly accessible rubber maps from NASA SERVIR Mekong to create a sample of 50,000 points for the year 2023 across Southeast Asia                                                                                         |   Poortinga et al. (2019)                |
|   rubber      |   2021   |   Southeast Asia                  |   Training samples used in the paper 'High-resolution maps show that rubber causes substantial deforestation' (Wang 2023); classes include rubber, forest, deciduous forest.                                                                                                        |   Wang et al. (2023)                     |
|   rubber\*    |   2021   |   Global                          |   Validation data come from Sheil et al. (2024), which was produced in response to Wang et al. (2023).                                                                                                                                                                              |   Sheil et al. (2024), Descals (2024b)   |

*Validation only, not used in training or model selection.

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
The trained models were hosted on Google Vertex AI using 5-10 compute nodes of `n1-standard-32` CPU machines and no accelerators.  Input imagery (pre-computed to minimize latency during inference) was forwarded from Google Earth Engine to the models on Vertex AI in serialized TensorFlow [Example](https://github.com/tensorflow/tensorflow/blob/v2.16.1/tensorflow/core/example/example.proto) format over [gRPC](https://grpc.io/) in [1,1] tiles. The following demonstrates this connection from the Earth Engine Python client:

```
output_bands_dict = {}
output_bands_dict['your_model_output_name'] = {
    'type': ee.PixelType.float(),
    'dimensions': 1,
}
model = ee.Model.fromVertexAi(
    endpoint='projects/your-project/locations/your-location/endpoints/your-endpoint-id',
    inputTileSize=[1, 1],
    outputTileSize=[1, 1],
    proj=ee.Projection('your_projection').atScale(your_scale),
    payloadFormat='GRPC_SERIALIZED_TF_EXAMPLES',
    fixInputProj=True,
    outputBands=output_bands_dict,
    maxPayloadBytes=5242800,
)
```

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

-   Becerra, Milagros; Rivera, Ovidio; Pawlak, Camila; Crocker, Alexandra; Pinto, Naiara. 2022. Base de datos de cobertura de cultivos de cacao en la Amazonia Peruana. Harvard Dataverse, V3. <https://doi.org/10.7910/DVN/XMQNC2>
-   Brown, C.F., Brumby, S.P., Guzder-Williams, B. et al. Dynamic World, Near real-time global 10 m land use land cover mapping. 2022. Sci Data 9, 251. [https://doi:10.1038/s41597-022-01307-4](about:blank)
-   CERSGIS. 2025. Reference Data Collection for Improving Land Use Change Mapping in Ghana.
-   CIAT. 2025. Coffee polygons annotated by the Alliance of Bioversity International and CIAT.
-   Clinton et al. 2024. A community palm model. arXiv. <https://arxiv.org/pdf/2405.09530>
-   Cooley, S., Pinto, N., Aguilar-Amuchastegui, N., Vela Alvarado, J., & Fahlen, J. 2021. Vegetation typology classification and data set in Ucayali, Peru (4.0). CaltechDATA. <https://doi.org/10.22002/D1.2318>
-   Danylo, O., Pirker, J., Lemoine, G. et al. A map of the extent and year of detection of oil palm plantations in Indonesia, Malaysia and Thailand. Sci Data 8, 96 (2021). <https://doi.org/10.1038/s41597-021-00867-1>
-   Descals, Adria. (2024a). Global oil palm extent and planting year from 1990 to 2021 (v1.2) \[Data set\]. Zenodo. <https://doi.org/10.5281/zenodo.13379129>
-   Descals, Adria. 2024b. Validation dataset for the article 'Rubber planting and deforestation' (v1.1). Zenodo. <https://doi.org/10.5281/zenodo.10646349>
-   Forest Data Partnership. 2024. A community forest model. <https://github.com/google/forest-data-partnership/edit/main/models/forests>
-   Fricker, Geoffrey; Nielsen, Kylee; Clark, Isabella; Davis, Jaxson; Bates, Sarah; Davis, Isabella; Pinto, Naira. 2022. Palm Oil Polygons for Ucayali Province, Peru (2019-2020). Harvard Dataverse, V3. <https://doi.org/10.7910/DVN/BSC9EI>
-   Google LLC. 2024. Manually digitized coffee polygons in Colombia. *Unpublished*.
-   Kalischek, N., Lang, N., Renier, C. et al. 2023. Cocoa plantations are associated with deforestation in Côte d’Ivoire and Ghana. Nature Food. 4, 384–393. <https://doi.org/10.1038/s43016-023-00751-8>
-   Lang, N., Jetz, W., Schindler, K. *et al.* A high-resolution canopy height model of the Earth. *Nature Ecology and Evolution.* 7, 1778–1789 (2023). <https://doi.org/10.1038/s41559-023-02206-6>
-   Lescuyer, Guillaume. 2024. Inventaire des arbres dans 223 cacaoyères agroforestières au Cameroun. CIRAD Dataverse, V1. <https://doi.org/10.18167/DVN1/MGDIJU>
-   MapBiomas Cacau. (2023). Mapeamento do Cultivo de Cacau Sombreado em 83 Municípios do Sul da Bahia. MapBiomas. <https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/relat_mapbiomas_cacau_83mun_final.pdf>
-   Meridia. 2025. Deliverables Report for Google. *Unpublished*.
-   Olofsson, Pontus, Giles M. Foody, Martin Herold, Stephen V. Stehman, Curtis E. Woodcock, Michael A. Wulder. 2014. Good practices for estimating area and assessing accuracy of land change, Remote Sensing of Environment, Volume 148, Pages 42-57. <https://doi.org/10.1016/j.rse.2014.02.015>
-   Pasquarella, Valerie J., Christopher F. Brown, Wanda Czerwinski, and William J. Rucklidge. 2023. Comprehensive quality assessment of optical satellite imagery using weakly supervised video learning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops, pages 2125–2135.
-   Poortinga, A., Tenneson, K., Shapiro, A., Nquyen, Q., San Aung, K., Chishtie, F. and Saah, D., 2019. Mapping plantations in Myanmar by fusing Landsat-8, Sentinel-2 and Sentinel-1 data along with systematic error quantification. Remote sensing, 11(7), p.831.
-   Schneider, Martina, Caroline Winchester, Elizabeth Goldman, and Yang Shao. Mapping cocoa and assessing deforestation risk for the cocoa sector in Côte d’Ivoire and Ghana. WRI Technical Note. 2023. <https://files.wri.org/d8/s3fs-public/2023-12/mapping-cocoa-assessing-deforestation-risk-ghana.pdf?VersionId=sT0HWefiGZf7UXTKhuZ.Ra644cXOlLl5&_gl=1yutix2_gcl_au*OTQ4NDkyNTIuMTc0NzQxNDcwOC43ODM1NzYzNC4xNzQ3NDE0NzE0LjE3NDc0MTQ3MTM>.
-   Shapiro, Aurelie. 2024. Cocoa reference data in Cameroon. *Personal communication*.
-   Sheil, D., Descals, A., Meijaard, E., & Gaveau, D. 2024. Rubber Planting and Deforestation. Preprints. <https://doi.org/10.20944/preprints202402.0743.v1>
-   Shimada, Masanobu, Takuya Itoh, Takeshi Motooka, Manabu Watanabe, Tomohiro Shiraishi, Rajesh Thapa, and Richard Lucas. New global forest/non-forest maps from ALOS PALSAR data (2007–2010). 2014. Remote Sensing of Environment. 155: 13–31. <https://doi.org/10.1016/j.rse.2014.04.014>
-   Souza et al. 2020. Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine – Remote Sensing, Volume 12, Issue 17, <https://doi.org/10.3390/rs12172735>.
-   Stanimirova, R., Tarrio, K., Turlej, K. et al. A global land cover training dataset from 1984 to 2020. 2023. Scientific Data 10, 879. <https://doi.org/10.1038/s41597-023-02798-5>
-   Tarrio, Katelyn 2025a. Plantation land use drives forest change in West Africa. *In prep*.
-   Tarrio, Katelyn 2025b. Google Sustainable Sourcing commodity production reference dataset. *Unpublished*.
-   Tarrio, Katelyn 2025c. Google Sustainable Sourcing forest and non-forest training dataset. *Unpublished*.
-   Vollrath, Andreas, Jennifer Adams, Sara Aparicio, and John Mrziglod. A global palm oil map for the year 2017 using multi-sensor sar imagery. 2019. Living Planet Symposium. ESA/ESRIN, Frascati, Italy.
-   Vollrath, Andreas, Adugna Mullissa, and Johannes Reiche. Angular-based radiometric slope correction for sentinel-1 on google earth engine. Remote Sensing, 12(11):1867, 2020. <https://doi.org/10.3390/rs12111867>
-   Wang, Y., Hollingsworth, P.M., Zhai, D. et al. High-resolution maps show that rubber causes substantial deforestation. 2023. Nature 623, 340–346. <https://doi.org/10.1038/s41586-023-06642-z>
-   Zanaga, D., Van De Kerchove, R., De Keersmaecker, W., Souverijns, N., Brockmann, C., Quast, R., Wevers, J., Grosu, A., Paccini, A., Vergnaud, S., Cartus, O., Santoro, M., Fritz, S., Georgieva, I., Lesiv, M., Carter, S., Herold, M., Li, Linlin, Tsendbazar, N.E., Ramoino, F., Arino, O., 2021. ESA WorldCover 10 m 2020 v100. <https://doi:10.5281/zenodo.5571936>

# Suggested citation

Forest Data Partnership. 2025. Community models 2025a. https://github.com/google/forest-data-partnership/edit/main/models/README.md

