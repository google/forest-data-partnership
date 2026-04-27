# Introduction

Here, we introduce the first pan-tropical, high resolution (10-meter) dataset that maps four major commodity tree crops: cocoa, coffee, rubber, and oil palm. For this work, we assembled a large, community-sourced reference database of over eight million points, integrating field observations and expert interpretation of high-resolution (less than one meter) imagery. We combined these samples with the Google Satellite Embeddings dataset in a deep learning framework that generates both classification labels and per-pixel class probability layers. Unlike existing, static map products, our model is deployable on-demand in Google Earth Engine (Gorelick et al., 2017), allowing us to generate maps for any year and region of interest. As continuous per-pixel probability layers, the dataset offers global consistency, local customization and per-pixel entropy as a spatial measure of model confusion. We illustrate the utility of our maps by showcasing representative outputs in key production regions and demonstrating how the dataset can be adapted to improve local performance and track change dynamics.

# Methods

## Geospatial foundation model inputs

As predictive inputs to the model, we used the AlphaEarth geospatial foundation model embeddings (Brown et al. 2025).  These embeddings constitute a 64-dimensional feature space, at 10 meters spatial resolution, produced annually.  The feature space contains condensed information from a variety of sensors, spectral regions, and derivative products such as climate and topography and was designed to facilitate predictive modeling of land surface characteristics in "data scarce regimes."  We use these data as predictive features on a per-pixel basis.  Because information from a 1280x1280 meter patch and a year's worth of data is encoded in the 64-D vectors, spatiotemporal convolutions are unnecessary in the model.  We used these data directly as predictive features and also as a change detector, during temporal augmentation.

## Commodity reference database

We compiled a large land use database by pooling millions of reference geometries (points or polygons) from diverse sources, including field observations, expert-labeled visual interpretations of very high-resolution imagery, and training/validation datasets from existing land change studies.  Contributors include the Food and Agriculture Organization of the United Nations (UN FAO), MapBiomas, CIAT, the World Resources Institute (WRI), NASA SERVIR, IIASA, Boston University, Google, and commercial providers such as agribusiness companies OFI, Meridia and Bunge who provided data through licensing agreements.  We generated a substantial portion of the reference data through manual digitization of polygons over mature tree crop cultivation areas identifiable in high-resolution imagery (Google 2025).  The presence of each specific tree crop was corroborated using evidence such as public records, commercial farm websites, mapped facility information and Google StreetView imagery. We excluded fallow areas, very immature crops, bands of natural trees, roads, or buildings in the digitized polygons (Google 2025).  Table 1 lists the full set of individual data sources in the reference database.

In aggregate, the commodity database contains 12,676,728 points, representing a wide variety of production systems across pantropical regions, including both smallholder and industrial operations, varying levels of shade tree density, monocultures and mixed agroforestry systems, and diverse management types, such as terraced, pivot-irrigated, and mixed-age stands (Figure 2).  The reference data also span multiple years: 2017-2024, and are temporally imbalanced by class, with some years and classes in relatively high proportion in the database.

## Convergence of evidence

We use several ancillary datasets in a convergence of evidence approach (D'Annunzio et al. 2024) to sample reference polygon geometries and generate pseudo-absence (i.e. not palm, rubber, cocoa or coffee) data corresponding to the "forest" and "other" classes.  Specifically, we used Dynamic World (Brown et al. 2022), Worldcover (Zanaga et al. 2021), MapBiomas (Souza et al., 2020), Forest Persistence (Forest Data Partnership 2024) and Natural forests of the world (Neumann et al. 2025) to identify areas of trees, shrubs, crops, or natural forest.  We used the prior release of our commodity models (Forest Data Partnership 2025) to identify areas of commodity production with high confidence (using probabilities palm > 0.9, rubber > 0.7, coffee > 0.98, and cocoa > 0.95).

## Reference polygon sampling

Some reference data was non-specific, with geometries containing more than the labeled commodity (e.g. roads, buildings, windbreaks, patches of other vegetation).  To improve sample purity, we masked commodity data with the ancillary datasets to exclude areas of natural forest, bare land, or land cover without the presence of the labeled commodity.  To capture within-field variability arising from different canopy densities, planting ages, and irregular spatial arrangements, we buffered polygons by 10 meters and systematically sampled unmasked pixels with a lattice at 10 or 20 meters spacing.

## Negatives sampling

To create "forest" pseudo-absences, within one degree of each commodity presence point, we randomly selected one "forest" sample from pixels classified as both natural and persistent forest (natural forest probability greater than 0.9 and forest persistence probability greater than 0.95).  To create "other" pseudo-absences, within one degree of each commodity presence point, we randomly selected one "other" sample from pixels classified as not trees, shrubs or mangroves in both Dynamic World and Worldcover.  For both "other" and "forest" pseudo-absences, we also excluded pixels previously mapped as commodities with high confidence.  The date of ancillary datasets (2020, except Dynamic World) resulted in a pseudo-absences dataset corresponding to 2020.  

The pooled reference and pseudo-absence database contains 12,676,728 point samples for the following land use classes: cocoa, coffee, rubber, oil palm, natural forest and other. Table 1 lists the reference sample distribution by land use type. Figure 1 illustrates the geographic distribution of reference data (excluding pseudo-absences) globally, with all classes aggregated into one degree cells. Commodity crop samples are concentrated in key production regions such as West Africa, Indonesia, Brazil, Peru and Colombia, reflecting the opportunistic nature of data collection through collaborator contributions and publicly available sources. Collaborator-provided non-forest samples extend into the Southern Cone of South America and Central Asia, producing heterogeneous geographic representation. Overall, samples are concentrated within the tropical belt (30°N - 30°S).

**Figure 1. Geographic distribution of reference data density, aggregated to a one-degree heatmap grid across all land use classes. Colors indicate the total number of reference points per grid cell from the pooled dataset of 12,676,728 samples. Higher densities (red) typically correspond to commodity crop data, which were concentrated in key production regions, while lower densities (white) generally represent natural forest or non-forest samples.**
![training data heatmap](/assets/images/training_data_heatmap_2025b.png)

**Table 1. Reference database.**

| Year | Commodity | Region | N | Description | Citation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2021 | Cocoa | Ghana | 1511 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2021 | Cocoa | Vietnam | 4 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2023 | Cocoa | Cameroon | 223 | CIRAD provided publicly available inventory of trees in 223 agroforestry cocoa plantations in Cameroon | Lescuyer (2024) |
| 2023 | Cocoa | Cameroon | 58 | Cocoa field data in Cameroon collected through the COCAFORI project, collected in March 2024 | Shapiro (2024) |
| 2023 | Cocoa | Colombia | 75835 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Ecuador | 18677 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Ecuador | 97416 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Indonesia | 2595 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Indonesia | 23598 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Brazil | 106641 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | West Africa | 13362 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | Tarrio et al. (2026) |
| 2023 | Cocoa | Ghana | 18634 | Field collected data for a Lacuna Fund project. | CERSGIS (2025) |
| 2023 | Cocoa | Brazil | 324 | Cocoa data from Bahia, Brazil, collected by Mapbiomas. | MapBiomas (2023)  |
| 2020 | Cocoa | Peru | 70183 | Cocoa polygons in Ucayali Peru, delineated based on the interpretation of satellite imagery from 2020; part of a NASA SERVIR Amazonia project. | Becerra et al. (2022) |
| 2024 | Cocoa | Sumatra | 5 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Cocoa | West Africa | 759879 | WRI developed the West Africa Cocoa dataset (WAC) in collaboration with the World Cocoa Foundation and 19 chocolate companies who contributed supply locations. Data consists of 839,242 plots over Ghana and Cote d' Ivoire, originally collected in situ / manually by GPS-tracing plot boundaries. | Schneider et al. (2023) |
| 2024 | Coffee | Colombia | 83401 | CIAT provided plot data in Colombia | CIAT (2025) |
| 2021 | Coffee | Vietnam | 13742 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2021 | Coffee | Vietnam | 171 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2023 | Coffee | Colombia | 84720 | Internal Google polygon annotations | Google (2024) |
| 2023 | Coffee | Brazil | 255910 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Brazil | 62630 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Jamaica | 8974 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Tanzania | 32556 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Mexico | 18861 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Hawaii | 44385 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Kenya | 38187 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Coffee | Indonesia | 9025 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Honduras | 8864 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Vietnam | 40550 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Ethiopia | 200359 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2023 | Coffee | Indonesia | 1526496 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2023 | Coffee | Uganda | 412727 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2023 | Coffee | Vietnam | 528526 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2017-2024 | Coffee | Global | 59862 | Olam Food Ingredients Coffee Unit provided data, licensed by Google to train Forest Data Partnership models. | Olam Food Ingredients Coffee Unit (2025) |
| 2021 | Forest | Ghana | 616 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2021 | Forest | Vietnam | 3628 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2021 | Negatives | Ghana | 6843 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2021 | Negatives | Vietnam | 9448 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2024 | Other | Colombia | 12111 | CIAT provided plot data in Colombia | CIAT (2025) |
| 2021 | Palm | Ghana | 894 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2021 | Palm | Vietnam | 4 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2017 | Palm | Global | 5345 | Point data from Olga Danylo / IIASA of oil palm across three countries in Southeast Asia | Danylo (2021) |
| 2023 | Palm | West Africa | 7456 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | Tarrio (2026) |
| 2021 | Palm | Global | 135462 | Point data generated by Google Crowd Compute | Clinton et al. (2024) |
| 2020 | Palm | Peru | 749951 | A team at JPL/California Polytechnic State University used Maxar and Planetscope imagery along with the Descals et al. 2019 model to hand digitize oil palm plantations. The imagery covered 2019 and 2020 for the Ucayali Province in Peru. | Fricker et al. (2022) |
| 2023 | Palm | Global | 75 | Tijs Lips (Bunge) provided some hand-made points (in his personal capacity). | Clinton et al. (2024) |
| 2017 | Palm | Global | 383558 | Reference data points collected for a global oil palm project for 2017, originally presented at the 2019 Living Planet Symposium in Milan | Vollrath (2019) |
| 2021 | Rubber | Vietnam | 7917 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | Vantalon et al. (2025) |
| 2023 | Rubber | Guatemala | 797823 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Rubber | DRC | 48273 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Rubber | Sri Lanka | 57988 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Rubber | Hainan Island | 329032 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Rubber | West Africa | 11751 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | Tarrio (2026) |
| 2020 | Rubber | Nigeria | 150000 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Rubber | Southeast Asia | 49448 | Ate Poortinga (of SIG / Spatial Informatics Group) used openly accessible rubber maps from NASA SERVIR Mekong to create a sample of 50,000 points for the year 2023 across Southeast Asia | Poortinga et al. (2019) |
| 2024 | Rubber | Sumatra | 9 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2021 | Rubber | Global | 45 | Training samples used in the paper 'High-resolution maps show that rubber causes substantial deforestation' (Wang 2023); classes include rubber, forest, deciduous forest. | Wang et al. (2023) |
| 2020 | Forest, Other | Global | 5290160 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |

**Table 2. Total number of reference samples by land use type, including pseudo-absences.**

| Tree crop type | Number samples |
| :--- | :--- |
| Cocoa | 1,188,945 |
| Coffee | 3,429,946 |
| Palm | 1,282,745 |
| Rubber | 1,452,286 |
| Natural forest | 2,486,569 |
| Other | 2,836,237 |

## Spatial partitioning

For training, model selection and accuracy assessment, we required three independent sets: training, test and evaluation respectively. We assume that labeled points are independent if they are more than 640 meters apart, or half the 1280 meter receptive field of the Alpha Earth foundations model we used for prediction. Although we tolerate spatial autocorrelation in the training data (i.e. points closer than 640 meters), in the test and evaluation sets, points are more than 640 meters apart.  

To generate these sets, we systematically sampled the reference database (pooled with pseudo-absences) globally. Systematic sampling prioritizes geographic representativeness, ensuring that all major production regions, cropping systems, and ecological zones are represented in the sample. In the square degrees containing any training data, we created a lattice of 0.025 degree (~2780 meters) resolution (n=1,846,400). We sampled the reference database with this lattice by selecting the closest point in the pooled reference data and pseudo-absences database that is within 1280 meters of each lattice point, if such a point existed. We partitioned this hold-out sample (n=215,140) into two assumed independent sets (test and evaluation) using a checkerboard pattern to minimize inter and infra sample spatial autocorrelation. To minimize spatial autocorrelation between the training data and any set used for accuracy assessment, we pooled the hold-out set locations with locations from Descals (2024a,  2024b), which we use as independent validation sets for palm and rubber, and removed all data from the training set within 640 meters of any point in the test set, evaluation set or the Descals (2024a,  2024b) sets.  

Through this process, we created three assumed independent sets: a training set, a test (model selection) set, and an evaluation set. We used Descals (2024a, n=18,812) for independent validation of the palm model and Descals (2024b, n=1555) for independent validation of the rubber model. Neither the evaluation set nor either of the Descals validation sets were used until after model selection, during the preparation of this manuscript. Table 3 shows the class distribution of training, test and evaluation data.

**Table 3. Training, test and evaluation datasets following geographic partitioning.**

| Commodity | Training | Test | Evaluation |
| :--- | :--- | :--- | :--- |
| Cocoa | 914,680 | 7812 | 7725 |
| Coffee | 2,558,139 | 705 | 676 |
| Palm | 901,525 | 2024 | 2032 |
| Rubber | 1,016,075 | 6114 | 6099 |
| Natural forest | 1,872,039 | 38,279 | 38,649 |
| Other | 2,081,203 | 52,637 | 52,388 |

**Figure 2. Training, test and evaluation data partitioning for a sub-region of West Sumatra, Indonesia.**
![grid_training_test_2025b](/assets/images/grid_training_test_2025b.png)

## Spectral thinning

In addition to the convergence of evidence based masking we used to refine reference data, we also employed thinning in feature space to further eliminate non-representative examples from the training set. Specifically, we assume that classes form compact structures in feature space, with representative examples close to the class centroid. The class centroids are first computed from the training set. To ensure geographic representation of each class, which occur in biophysically diverse growth contexts, we computed percentiles by euclidean distance to class centroid in level 5 geohashes (~4.89 kilometer resolution) across the spatial domain of the training data. In each geohash, we selected the 30% of the training data closest to the global class centroid. The resultant class distribution is shown in Table 4. Note that following spatial partitioning and spectral thinning, roughly 21-23% of reference data was retained for training.

**Table 4. Training samples after spectral thinning.**

| Tree crop type | Number samples |
| :--- | :--- |
| Cocoa | 276,343 |
| Coffee | 767,828 |
| Palm | 271,826 |
| Rubber | 307,680 |
| Natural forest | 580,627 |
| Other | 649,833 |

## Temporal Augmentation

Although we trained models on the spatially partitioned and spectrally thinned training dataset, they were found to exhibit unrealistically high interannual variability. To ameliorate this unexpected effect, we performed temporal augmentation on the training and test datasets. The training data contain a year attribute, corresponding to the time of data collection in situ or the image acquisition date if visually interpreted. We assume the label of each point to be valid in the year in which it was collected as well as any other year for which the spectral angle relative to the reference year is low. The spectral angle is computed as the arccos of the dot product of two feature vectors: the reference year vector and prospective year vector. If the angle is less than 0.2, we assume the pixel to be unchanged and append the prospective year feature vector to the training or test set. This was done for every year available in 2017-2024 for both the training and test sets. Table 5 shows the number of examples per class for training and test, after the temporal augmentation.

**Table 5. Training and test datasets following temporal augmentation.**

| Commodity | Training | Test |
| :--- | :--- | :--- |
| Cocoa | 1,562,897 | 16,178 |
| Coffee | 3,029,306 | 895 |
| Palm | 1,339,568 | 3541 |
| Rubber | 1,789,435 | 10,291 |
| Natural forest | 3,431,857 | 113,542 |
| Other | 3,239,129 | 148,419 |

The training dataset that results from temporal augmentation is still class imbalanced by year. To generate an approximately uniform class distribution by year, we performed another feature space thinning on the temporally augmented dataset, choosing thinning percentiles individually by class and year with a target of 100,000 examples for each class for each year. Following this temporal balancing in feature space, the training data had the class distribution shown in Table 6.

**Table 6. Training samples after spectral thinning, temporal thinning and feature space balancing.**

| Tree crop type | Number samples |
| :--- | :--- |
| Cocoa | 789,463 |
| Coffee | 695,247 |
| Palm | 822,462 |
| Rubber | 783,491 |
| Natural forest | 807,848 |
| Other | 794,881 |

**Figure 3. Label count by year and class after temporal augmentation..**
![balanced_training_data_distribution_2025b](/assets/images/balanced_training_data_distribution_2025b.png)

## Classification

Model training and classification were performed using a cloud-based infrastructure similar to Google Cloud AutoML (Bisong et al., 2019). Model architecture, activation functions, optimization routines, learning rates, batch sizes, and training iterations were selected through an automated hyperparameter search, with up to 24 hours allocated for optimization and 24 hours for training. Model architecture is constrained to deep neural networks (DNNs), or networks with one or more hidden layers and one-dimensional inputs. We used the test set for model selection in the optimization phase, the training set for training and did not use the evaluation set.

The final TensorFlow-based DNN was hosted on Vertex AI and deployed in Google Earth Engine. The model outputs probability of class occurrence, either in a vector, for multiclass training, or as a scalar for single class model training.

## Data Records 

The outputs generated by this study are: 

1. Fully trained tree crop classification models, deployable on-the-fly in Google Earth Engine via VertexAI.
2. Per-pixel probability layers for each class for selected even-numbered years.

These products are designed to flexibly adapt to diverse use cases, for example by tuning per-class thresholds to local conditions and/or independent field data. The probability layers, when stacked with other datasets, form a per-pixel classification. For example, when combined with natural forest (Neumann et al.) and water from WorldCover (Zanaga et al. 2021), a pan-tropical map of commodity production in 2020 is assembled.  

Data Link: [https://goo.gle/fodapa-layers-2025b](https://goo.gle/fodapa-layers-2025b)

## Technical validation

### Model performance

We evaluated single-class model performance on the evaluation set described previously by recoding labels to one-hot vectors. We also evaluated the palm model on the Descals et al. (2024b) validation set and the rubber model on the Sheil et al. (2024) validation set. We present these results as precision-recall curves to illustrate accuracy tradeoffs with choice of threshold. We also report accuracy at the intersection of precision and recall curves, but note that these metrics are synoptic and map accuracy varies temporally and geographically.

*   **Palm (generated evaluation):** 0.92 @ 0.22
![palm_test_accuracy_2025b](/assets/images/palm_test_accuracy_2025b.png)

*   **Palm (Descals):** 0.81 @ 0.66
![palm_descals_accuracy_2025b](/assets/images/palm_descals_accuracy_2025b.png)

*   **Rubber (generated evaluation):** 0.96 @ 0.44
![rubber_test_accuracy_2025b](/assets/images/rubber_test_accuracy_2025b.png)

*   **Rubber (Sheil):** 0.75 @ 0.35
![**rubber_sheil_accuracy_2025b**](/assets/images/rubber_sheil_accuracy_2025b.png)

*   **Cocoa (generated evaluation):** 0.94 @ 0.5
![cocoa_test_accuracy_2025b](/assets/images/cocoa_test_accuracy_2025b.png)

*   **Coffee (generated evaluation):** 0.7 @ 0.28
![coffee_test_accuracy_2025b](/assets/images/coffee_test_accuracy_2025b.png)

## Limitations

*   Comparison of estimates of accuracy from generated evaluation data and independent validation data suggests that accuracies from generated evaluation data are overestimates. It is incumbent upon the consumer of the data to conduct localized accuracy assessments to ensure suitability for any particular purpose.
*   Qualitative inspection of the categorical maps revealed mixed performance across regions. 
    *   Palm is overestimated in dense canopy forest.
    *   Coffee is overestimated in topographically suitable locations.
    *   Rubber is underestimated in South Sumatra.
*   While the tree crops were all overpredicted on average, many areas showed strong correspondence with existing plantation locations and field boundaries. 
*   Our training dataset is largely opportunistic, and does not comprehensively represent every class in every region. Users should exercise extreme caution when using data in areas not represented in our training dataset.
*   Temporal instability between years is present. Determination of change may require statistical comparison of multiple time periods (Clinton et al. 2024), adjustment of thresholds annually, or post processing such as BULC (Cardille and Fortin 2016).
*   Input artifacts may be visually apparent in output probabilities and result in classification errors at some thresholds.

# References

-   Becerra, Milagros; Rivera, Ovidio; Pawlak, Camila; Crocker, Alexandra; Pinto, Naiara. 2022. Base de datos de cobertura de cultivos de cacao en la Amazonia Peruana. Harvard Dataverse, V3. <https://doi.org/10.7910/DVN/XMQNC2>
-   Brown, C.F., Brumby, S.P., Guzder-Williams, B. et al. Dynamic World, Near real-time global 10 m land use land cover mapping. 2022. Sci Data 9, 251. [https://doi:10.1038/s41597-022-01307-4](about:blank)
-   Brown, C.F., Kazmierski, M.R., Pasquarella, V.J., Rucklidge, W.J., Samsikova, M., Zhang, C., Shelhamer, E., Lahera, E., Wiles, O., Ilyushchenko, S. and Gorelick, N., 2025. Alphaearth foundations: An embedding field model for accurate and efficient global mapping from sparse label data. arXiv preprint [arXiv:2507.22291](https://arxiv.org/abs/2507.22291v1).
-   Cardille, J.A. and Fortin, J.A. 2016. Bayesian updating of land-cover estimates in a data-rich environment. Remote Sensing of Environment. 186. pp.234-249. <https://doi.org/10.1016/j.rse.2016.08.021>.
-   CERSGIS. 2025. Reference Data Collection for Improving Land Use Change Mapping in Ghana.
-   CIAT. 2025. Coffee polygons annotated by the Alliance of Bioversity International and CIAT.
-   Clinton et al. 2024. A community palm model. arXiv. <https://arxiv.org/pdf/2405.09530>
-   D’Annunzio, R., O’Brien, V., Arnell, A., Neeff, T., Fontanarosa, R., Valbuena Perez, P., Shapiro, A.C., Sanchez-Paus Díaz, A., Merle, C., Vega, J. & Fox, J. 2024. Towards a digital public infrastructure for deforestation-related trade regulations - What is in that plot? (Whisp) solution to implement convergence of evidence. Rome, FAO. <https://doi.org/10.4060/cd0957en>.
-   Danylo, O., Pirker, J., Lemoine, G. et al. A map of the extent and year of detection of oil palm plantations in Indonesia, Malaysia and Thailand. Sci Data 8, 96 (2021). <https://doi.org/10.1038/s41597-021-00867-1>
-   Descals, Adria. (2024a). Global oil palm extent and planting year from 1990 to 2021 (v1.2) \[Data set\]. Zenodo. <https://doi.org/10.5281/zenodo.13379129>
-   Descals, Adria. 2024b. Validation dataset for the article 'Rubber planting and deforestation' (v1.1). Zenodo. <https://doi.org/10.5281/zenodo.10646349>
-   Forest Data Partnership. 2024. A community forest model. <https://github.com/google/forest-data-partnership/edit/main/models/v2024/forests>
-   Forest Data Partnership. 2025. Community models 2025a. <https://github.com/google/forest-data-partnership/edit/main/models/v2025/README.md>
-   Fricker, Geoffrey; Nielsen, Kylee; Clark, Isabella; Davis, Jaxson; Bates, Sarah; Davis, Isabella; Pinto, Naira. 2022. Palm Oil Polygons for Ucayali Province, Peru (2019-2020).  2022.  Harvard Dataverse, V3. <https://doi.org/10.7910/DVN/BSC9EI>
-   Google LLC. 2024. Manually digitized coffee polygons in Colombia. *Unpublished*.
-   Google LLC. 2025. Google digitized commodity production, forest and non-forest reference dataset. *Unpublished*.
-   Gorelick, Noel, Matt Hancher, Mike Dixon, Simon Ilyushchenko, David Thau, Rebecca Moore.  2017.  Google Earth Engine: Planetary-scale geospatial analysis for everyone. Remote Sensing of Environment. <https://doi.org/10.1016/j.rse.2017.06.031>.
-   Lescuyer, Guillaume. 2024. Inventaire des arbres dans 223 cacaoyères agroforestières au Cameroun. CIRAD Dataverse, V1. <https://doi.org/10.18167/DVN1/MGDIJU>
-   MapBiomas Cacau. 2023. Mapeamento do Cultivo de Cacau Sombreado em 83 Municípios do Sul da Bahia. MapBiomas. [online report](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/relat_mapbiomas_cacau_83mun_final.pdf)
-   Meridia. 2025. Deliverables Report for Google. *Unpublished*.
-   Neumann, M., Raichuk, A., Jiang, Y. et al. Natural forests of the world – a 2020 baseline for deforestation and degradation monitoring. 2025. Scientific Data. 12, 1715. https://doi.org/10.1038/s41597-025-06097-z
-   Olam Food Ingredients Coffee Unit. 2025. Deliverables Report for Google. *Unpublished*.
-   Poortinga, A., Tenneson, K., Shapiro, A., Nquyen, Q., San Aung, K., Chishtie, F. and Saah, D., 2019. Mapping plantations in Myanmar by fusing Landsat-8, Sentinel-2 and Sentinel-1 data along with systematic error quantification. Remote sensing, 11(7), p.831.
-   Schneider, Martina, Caroline Winchester, Elizabeth Goldman, and Yang Shao. Mapping cocoa and assessing deforestation risk for the cocoa sector in Côte d’Ivoire and Ghana. WRI Technical Note. 2023. <https://files.wri.org/d8/s3fs-public/2023-12/mapping-cocoa-assessing-deforestation-risk-ghana.pdf?VersionId=sT0HWefiGZf7UXTKhuZ.Ra644cXOlLl5&_gl=1yutix2_gcl_au*OTQ4NDkyNTIuMTc0NzQxNDcwOC43ODM1NzYzNC4xNzQ3NDE0NzE0LjE3NDc0MTQ3MTM>.
-   Shapiro, Aurelie. 2024. Cocoa reference data in Cameroon. *Personal communication*.
-   Sheil, D., Descals, A., Meijaard, E., & Gaveau, D. 2024. Rubber Planting and Deforestation. Preprints. <https://doi.org/10.20944/preprints202402.0743.v1>
-   Souza et al. 2020. Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine – Remote Sensing, Volume 12, Issue 17, <https://doi.org/10.3390/rs12172735>.
-   Tarrio, Katelyn, 2026. Plantation land use drives forest change in West Africa. *In prep*.
-   Vantalon, Thibaud, Phuong Thi Luong, Jorge Andres Perez Escobar, Jhon Jairo Tello Dagua, Trong Van Phan, Hang Nguyen, Hong Nguyen, Hoa Nguyen, and Louis Reymondin. 2025. “Sample Earth: Machine-Learning&ndash;Ready Land-Cover Reference Dataset.” Harvard Dataverse. <https://doi.org/10.7910/DVN/U7HWY1>.
-   Vollrath, Andreas, Jennifer Adams, Sara Aparicio, and John Mrziglod. A global palm oil map for the year 2017 using multi-sensor sar imagery. 2019. Living Planet Symposium. ESA/ESRIN, Frascati, Italy.
-   Wang, Y., Hollingsworth, P.M., Zhai, D. et al. High-resolution maps show that rubber causes substantial deforestation. 2023. Nature 623, 340–346. <https://doi.org/10.1038/s41586-023-06642-z>
-   Zanaga, D., Van De Kerchove, R., De Keersmaecker, W., Souverijns, N., Brockmann, C., Quast, R., Wevers, J., Grosu, A., Paccini, A., Vergnaud, S., Cartus, O., Santoro, M., Fritz, S., Georgieva, I., Lesiv, M., Carter, S., Herold, M., Li, Linlin, Tsendbazar, N.E., Ramoino, F., Arino, O., 2021. ESA WorldCover 10 m 2020 v100. <https://doi:10.5281/zenodo.5571936>

# Suggested citation

Forest Data Partnership. 2026. Community models 2025b. https://github.com/google/forest-data-partnership/edit/main/models/v2025/README.md
