# Introduction

Here we introduce the most current, pan-tropical, high resolution (10-meter) dataset of major commodity tree crops: cocoa, coffee, rubber, and palm. For this work, we assembled a large, community-sourced reference database of over 16 million points, integrating field observations and expert interpretation of high-resolution (less than one meter) imagery. We combined these samples with the AlphaEarth Foundation (AEF) model satellite embeddings dataset ([Brown et al. 2025](https://arxiv.org/abs/2507.22291)) in a deep learning framework that generates both classification labels and per-pixel class probability layers. Unlike existing, static map products, our models are deployable on-demand in Google Earth Engine ([Gorelick et al., 2017](https://www.sciencedirect.com/science/article/pii/S0034425717302900?via%3Dihub)), allowing map generation for any year and region of interest. As continuous per-pixel probability layers, the dataset offers global consistency, local customization and per-pixel entropy as a spatial measure of model confusion. We illustrate the utility of our maps by showcasing global outputs for several years and demonstrating how the dataset can be adapted to improve local performance and track change dynamics.

# Methods

## AlphaEarth Foundation model satellite embeddings inputs

As predictive inputs to the model, we used the AEF annual satellite embeddings ([Earth Engine catalog link](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL)). These embeddings constitute a 64-dimensional feature space, at 10 meters spatial resolution, encoding one calendar year of inputs in each output image.  The feature space contains condensed information from a variety of sensors, spectral regions, and derivative products such as climate and topography and was designed to facilitate predictive modeling of land surface characteristics in "data scarce regimes."  We use these data as predictive features on a per-pixel basis.  Because information from a 1280x1280 meter patch and a year's worth of data is encoded in the 64-D vectors, additional spatiotemporal convolutions are unnecessary in the model when considering only annual phenology.  We used these data directly as predictive features and also as a change detector, during temporal augmentation.

## Commodity reference database

We compiled a large land use database by pooling millions of reference geometries (points or polygons) from diverse sources, including field observations, expert-labeled visual interpretations of very high-resolution imagery, and training/validation datasets from existing land change studies.  Contributors include the Food and Agriculture Organization of the United Nations (UN FAO), MapBiomas, CIAT, the World Resources Institute (WRI), the SERVIR global collaborative, IIASA, Boston University, Google, and commercial providers such as agribusiness companies OFI and Meridia who provided data through commercial licensing agreements. External collaborators ("trusted testers")  examined previous releases of the datasets and provided actionable and specific feedback which enabled us to augment the reference database in problematic areas.  We generated a substantial portion of the reference data through manual digitization of polygons over mature tree crop cultivation areas identifiable in high-resolution imagery (Google 2025).  The presence of each specific tree crop was corroborated using evidence such as public records, commercial farm websites, mapped facility information, Google StreetView imagery, or trusted tester feedback. We excluded fallow areas, very immature crops, bands of natural trees, roads, or buildings in the digitized polygons. Table 1 lists the full set of individual data sources in the reference database.

**Table 1**. Reference Database
| Year | Commodity | Region | N | Description | Citation |
| ----- | :---- | :---- | ----- | :---- | :---- |
| 2024 | Coffee | Colombia | 83401 | CIAT provided plot data in Colombia | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2024 | Other | Colombia | 12111 | CIAT provided plot data in Colombia | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2021 | Cocoa | Ghana | 1511 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2021 | Forest | Ghana | 616 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2021 | Negatives | Ghana | 6843 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2021 | Palm | Ghana | 894 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2021 | Cocoa | Vietnam | 4 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2021 | Coffee | Vietnam | 13742 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2021 | Coffee | Vietnam | 171 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2021 | Forest | Vietnam | 3628 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2021 | Negatives | Vietnam | 9448 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2021 | Palm | Vietnam | 4 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2021 | Rubber | Vietnam | 7917 | CIAT Sample Earth data. Licensed by Google to train Forest Data Partnership models. | CIAT (2025) |
| 2023 | Cocoa | Cameroon | 223 | CIRAD provided publicly available inventory of trees in 223 agroforestry cocoa plantations in Cameroon | [Lescuyer (2024)](https://dataverse.cirad.fr/dataset.xhtml?persistentId=doi:10.18167/DVN1/MGDIJU) |
| 2023 | Cocoa | Cameroon | 58 | Cocoa field data in Cameroon collected through the COCAFORI project, collected in March 2024 | Shapiro (2024) |
| 2023 | Coffee | Colombia | 84720 | Internal Google polygon annotations | Google (2025) |
| 2017 | Palm | Global | 5345 | Point data from Olga Danylo / IIASA of oil palm across three countries in Southeast Asia | [Danylo (2021)](https://www.nature.com/articles/s41597-021-00867-1) |
| 2023 | Rubber | Guatemala | 797823 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Brazil | 62630 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Brazil | 255910 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Colombia | 75835 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Jamaica | 8974 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Tanzania | 32556 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Mexico | 18861 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Ecuador | 18677 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Hawaii | 44385 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Kenya | 38187 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Rubber | DRC | 48273 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Coffee | Indonesia | 9025 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Honduras | 8864 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Rubber | Sri Lanka | 57988 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Coffee | Vietnam | 40550 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Ecuador | 97416 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Indonesia | 2595 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Indonesia | 23598 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | Brazil | 106641 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Rubber | Hainan Island | 329032 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Cocoa | West Africa | 13362 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | Tarrio et al. (2026) |
| 2023 | Palm | West Africa | 7456 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | Tarrio et al. (2026) |
| 2023 | Rubber | West Africa | 11751 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | Tarrio et al. (2026) |
| 2023 | Cocoa | Ghana | 18634 | Field collected data for a Lacuna Fund project. | [CERSGIS (2025)](https://zenodo.org/records/16579443) |
| 2023 | Cocoa | Brazil | 324 | Cocoa data from Bahia, Brazil, collected by Mapbiomas. | [MapBiomas (2023)](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/relat_mapbiomas_cacau_83mun_final.pdf%20) |
| 2023 | Coffee | Ethiopia | 200359 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2023 | Coffee | Indonesia | 1526496 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2023 | Coffee | Uganda | 412727 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2023 | Coffee | Vietnam | 528526 | Coffee positive polygons covering 40k hectares across Vietnam, Indonesia, Uganda, and Ethiopia. | Meridia (2025) |
| 2017-2024 | Coffee | Global | 59862 | Olam Food Ingredients Coffee Unit provided data, licensed by Google to train Forest Data Partnership models. | Olam Food Ingredients Coffee Unit (2025) |
| 2020 | Forest | Global | 2482325 | Forest pseudo-presences, generated by Google for the Forest Data Partnership. | This publication. |
| 2020 | Other | Global | 2807835 | Other pseudo-presences, generated by Google for the Forest Data Partnership. | This publication. |
| 2020 | Rubber | Nigeria | 150000 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2021 | Palm | Global | 135462 | Point data generated by Google Crowd Compute | [Clinton et al. (2024)](https://arxiv.org/pdf/2405.09530) |
| 2023 | Rubber | Southeast Asia | 49448 | Ate Poortinga (of SIG / Spatial Informatics Group) used openly accessible rubber maps from NASA SERVIR Mekong to create a sample of 50,000 points for the year 2023 across Southeast Asia | [Poortinga et al. (2019)](https://www.mdpi.com/2072-4292/11/7/831) |
| 2020 | Cocoa | Peru | 70183 | Cocoa polygons in Ucayali Peru, delineated based on the interpretation of satellite imagery from 2020; part of a NASA SERVIR Amazonia project. | [Becerra et al. (2022)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XMQNC2) |
| 2020 | Palm | Peru | 749951 | A team at JPL/California Polytechnic State University used Maxar and Planetscope imagery along with the Descals et al. 2019 model to hand digitize oil palm plantations. The imagery covered 2019 and 2020 for the Ucayali Province in Peru. | [Fricker et al. (2022)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/BSC9EI) |
| 2024 | Cocoa | Sumatra | 5 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2024 | Rubber | Sumatra | 9 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Palm | Global | 75 | Tijs Lips (Bunge) provided some hand-made points (in his personal capacity). | [Clinton et al. (2024)](https://arxiv.org/pdf/2405.09530) |
| 2017 | Palm | Global | 383558 | Reference data points collected for a global oil palm project for 2017, originally presented at the 2019 Living Planet Symposium in Milan | Vollrath (2019) |
| 2021 | Rubber | Global | 2059 | Training samples used in the paper 'High-resolution maps show that rubber causes substantial deforestation' (Wang 2023); classes include rubber, forest, deciduous forest. | [Wang et al. (2023)](https://www.nature.com/articles/s41586-023-06642-z) |
| 2020 | Cocoa | West Africa | 759879 | WRI developed the West Africa Cocoa dataset (WAC) in collaboration with the World Cocoa Foundation and 19 chocolate companies who contributed supply locations. Data consists of 839,242 plots over Ghana and Cote d' Ivoire, originally collected in situ / manually by GPS-tracing plot boundaries. | [Schenider (2023)](https://files.wri.org/d8/s3fs-public/2023-12/mapping-cocoa-assessing-deforestation-risk-ghana.pdf?VersionId=sT0HWefiGZf7UXTKhuZ.Ra644cXOlLl5&_gl=1yutix2_gcl_au*OTQ4NDkyNTIuMTc0NzQxNDcwOC43ODM1NzYzNC4xNzQ3NDE0NzE0LjE3NDc0MTQ3MTM) |
| multiple | Other | Ghana | 21023 | CIAT provided data, licensed by Google to train Forest Data Partnership models. | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| multiple | Cocoa | Ghana | 471892 | CIAT provided data, licensed by Google to train Forest Data Partnership models. | [Vantalon et al. (2025)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/U7HWY1) |
| 2024 | Rubber | Sumatra | 4123 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2017-2023 | Rubber | Sumatra | 206461 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Forest, Other | Hawaii | 317854 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Forest, Other | East Africa | 45229 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Cocoa | Java | 1 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Forest, Other | Java | 2390 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Coffee | East Africa | 369 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2023 | Other | West Africa | 12992 | Manually collected point data across West Africa (Ghana, Cote d'Ivoire, Liberia, Sierra Leone) for research paper | [Stanimirova et al. (2020)](https://www.nature.com/articles/s41597-023-02798-5), Tarrio et al. (2026) |
| 2021 | Cocoa | Southeast Asia | 2143 | Hand-made, fully segmented land-use polygons in Indonesia made for a Lacuna Func project. | [Wafiq et al. (2025)](https://zenodo.org/records/15618532) |
| 2021 | Rubber | Southeast Asia | 4001 | Hand-made, fully segmented land-use polygons in Indonesia made for a Lacuna Func project. | [Wafiq et al. (2025)](https://zenodo.org/records/15618532) |
| 2021 | Forest | Southeast Asia | 671776 | Hand-made, fully segmented land-use polygons in Indonesia made for a Lacuna Func project. | [Wafiq et al. (2025)](https://zenodo.org/records/15618532) |
| 2021 | Other | Southeast Asia | 404117 | Hand-made, fully segmented land-use polygons in Indonesia made for a Lacuna Func project. | [Wafiq et al. (2025)](https://zenodo.org/records/15618532) |
| 2021 | Palm | Southeast Asia | 1333151 | Hand-made, fully segmented land-use polygons in Indonesia made for a Lacuna Func project. | [Wafiq et al. (2025)](https://zenodo.org/records/15618532) |
| multiple | Forest | Global | 41041 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| multiple | Coffee | Global | 764 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| multiple | Palm | Global | 385 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| multiple | Other | Global | 30 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| multiple | Rubber | Global | 269 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Other | Global | 23196 |  | [Stanimirova et al. (2020)](https://www.nature.com/articles/s41597-023-02798-5) |
| 2019 | Other | Global | 43401 |  | [Stanimirova et al. (2020)](https://www.nature.com/articles/s41597-023-02798-5) |
| 2025 | Forest | Ecuador | 8723 | Manually digitized polygons identified from high-resolution Google Earth imagery, StreetView, and corroborating evidence for commodity presence (e.g. websites for commercial-scale farms). | Google (2025) |
| 2020 | Forest, Other | Global | 27097 | Forest pseudo-presences, generated by Google for the Forest Data Partnership. | This publication |

In aggregate, the reference database (N=11,031,010) represents a wide variety of production systems across pantropical regions, including both smallholder and industrial operations, varying levels of shade tree density, monocultures and mixed agroforestry systems, and diverse management types, such as terraced, pivot-irrigated, and mixed-age stands.  The reference data also span multiple years: 2017-2025, and are temporally imbalanced by class, with some years and classes in relatively high proportion in the database. The reference data are also spatially imbalanced, with some geographies well represented and some not at all.

**Figure 1.** Geographic distribution of reference data density, aggregated to a one-degree heatmap grid by commodity. Colors indicate the total number of reference points available per grid cell from the reference dataset. [Code Editor link](https://code.earthengine.google.com/5e339bd356ab1f3761efc169bb830eaf).
![cocoa_heatmap_2026a](/assets/images/cocoa_heatmap_2026a.png)
![coffee_heatmap_2026a](/assets/images/coffee_heatmap_2026a.png)
![palm_heatmap_2026a](/assets/images/palm_heatmap_2026a.png)
![rubber_heatmap_2026a](/assets/images/rubber_heatmap_2026a.png)

## ‘Negative’ sample generation

### Convergence of evidence

We use several ancillary datasets in a convergence of evidence approach ([d'Annunzio et al. 2026](https://openknowledge.fao.org/items/22aa92d2-995d-400f-a5b4-04ee3cc3c515)) to sample reference polygon geometries and generate negatives (i.e. not palm, rubber, cocoa or coffee) data corresponding to the "forest" and "other" classes.  Specifically, we used Dynamic World ([Brown et al. 2022](https://doi.org/10.1038/s41597-022-01307-4)), Worldcover ([Zanaga et al. 2021](https://doi.org/10.5281/zenodo.5571936)), MapBiomas ([Souza et al., 2020](https://www.mdpi.com/2072-4292/12/17/2735)), Forest Persistence ([Forest Data Partnership 2024](https://github.com/google/forest-data-partnership/blob/main/models/forests/README.md)) and Natural forests of the world ([Neumann et al. 2025](https://www.nature.com/articles/s41597-025-06097-z)) to identify areas of trees, shrubs, crops, natural forest, or other land cover.  We used the prior release of the Forest Data Partnership commodity maps ([Forest Data Partnership 2025](https://github.com/google/forest-data-partnership/tree/main/models/model_2025a)) to identify areas of commodity production with high confidence (using probabilities palm \> 0.9, rubber \> 0.7, coffee \> 0.98, and cocoa \> 0.95).

### Reference polygon sampling

Some reference data was non-specific, with geometries containing more than the labeled commodity (e.g. roads, buildings, windbreaks, patches of other vegetation).  To improve sample purity, we masked commodity data with the ancillary datasets to exclude areas of natural forest, bare land, or land cover without the presence of the labeled commodity.  To capture within-field variability arising from different canopy densities, planting ages, and irregular spatial arrangements, we buffered polygons by 10 meters and systematically sampled unmasked pixels with a lattice at 10 to 30 meters spacing.

### Negatives sampling

To create "forest" pseudo-absences, we randomly selected "forest" samples from pixels classified as both natural and persistent forest (natural forest probability greater than 0.9 and forest persistence probability greater than 0.95).  To create "other" pseudo-absences, we randomly selected "other" samples from pixels classified as not trees, shrubs or mangroves in both Dynamic World and Worldcover.  For both "other" and "forest" pseudo-absences, we excluded pixels previously mapped as commodities with high confidence. We sampled one "forest" and one "other" pixel within one degree of each commodity presence point and 20 "forest" and 20 "other" points per square degree in the entire range, if possible given inputs availability. The date of ancillary datasets (2020, except Dynamic World) resulted in a pseudo-absences dataset (N=5,290,160) corresponding to 2020\. 

The pooled reference and pseudo-absence database contains 16,321,170 point samples for the following land use classes: cocoa, coffee, rubber, oil palm, natural forest and other. Table 1 lists the reference sample distribution by land use type. Figure 1 illustrates the geographic distribution of reference data (excluding pseudo-absences) globally, with all classes aggregated into one degree cells. Commodity crop samples are concentrated in key production regions such as West Africa, Indonesia, Brazil, Peru and Colombia, reflecting the opportunistic nature of data collection through collaborator contributions and publicly available sources. Collaborator-provided non-forest samples extend into the Southern Cone of South America and Central Asia, producing heterogeneous geographic representation. We excluded samples outside the tropics.

**Table 2.** Total number of reference samples by commodity, including pseudo-absences.
| Commodity | N |
| :---- | ----- |
| cocoa | 1,662,981 |
| coffee | 3,431,079 |
| forest | 3,398,854 |
| other | 3,542,821 |
| palm | 2,616,281 |
| rubber | 1,669,154 |

**Figure 2.** Training data distribution in an area of Indonesia.
![training_data_indonesia_2026a](/assets/images/training_data_indonesia_2026a.png)

## Spatial partitioning

For training and model selection, we desired (assumed) independent sets. The training set is used to train the model; the model selection set is used to choose the best model over multiple neural network architectures and parameterizations.  We assume that labeled points are independent if they are more than 640 meters apart, or half the 1280 meter receptive field of the AEF satellite embeddings we used for prediction.  Although we tolerate spatial autocorrelation in the training data (i.e. points closer than 640 meters), in the model selection set, points are more than 640 meters apart.

To generate these sets, we systematically sampled the reference database (pooled with pseudo-absences) globally.  Systematic sampling prioritizes geographic representativeness, ensuring that all major production regions, cropping systems, and ecological zones are represented in the sample.  In the square degrees containing any training data, we created a lattice of 0.025 degree (\~2780 meters) resolution (n=9,243,200).  We sampled the reference database with this lattice to get a model selection set. The sample method is: select the closest point in the pooled reference and pseudo-absences database that is within 1280 meters of each lattice point, if such a point existed. We then removed all data from the training set within 640 meters of any point in the model selection set.

Through this process, we created assumed independent sets: a training set and a model selection set.  We used [Descals (2024b](https://zenodo.org/records/13379129), n=18,812) for assessment of the palm model and [Descals (2024c](https://zenodo.org/records/10646349), n=1555) for assessment of the rubber model.  Though neither of the Descals validation sets were used until after model selection, they are not necessarily independent of the training, which could be within the 640 meter radius of assumed autocorrelation.  Figure 3 illustrates the geographic configuration of the resultant sets.  Table 3 shows the class distribution of training and model selection data.

**Table 3.** Training, test and evaluation datasets following geographic partitioning.
| Commodity | Training | Model Selection |
| :---- | ----- | ----- |
| cocoa | 1,273,132 | 15,407 |
| coffee | 2,563,018 | 1397 |
| forest | 2,515,685 | 83,365 |
| other | 2,590,497 | 149,128 |
| palm | 1,936,774 | 4285 |
| rubber | 1,157,503 | 12,464 |

**Figure 3.** Training and validation data partitioning for a sub-region of Indonesia. White lines show a grid at 0.5 degrees; black points are the training data, discarded near the validation data (gray).  White points are the 0.025 degree grid used to sample from the training data.
![grid_training_test_2026a](/assets/images/grid_training_test_2026a.png)

## Spectral thinning

In addition to the convergence of evidence based masking we used to refine reference data, we also employed thinning in AEF feature space to further eliminate non-representative examples from the training set.  Specifically, we assume that classes form compact structures in feature space, with representative examples close to the class centroid.  The class centroids are first computed from the training set.  To ensure geographic representation of each class, which occur in biophysically diverse growth contexts, we computed percentiles by euclidean distance to class centroid in level 5 geohashes (\~4.89 kilometer resolution) across the spatial domain of the training data.  In each geohash, we selected the 40% of the training data closest to the global class centroid.  The resultant class distribution is shown in Table 4.  Note that following spatial partitioning and spectral thinning, roughly 30% of reference data was retained for training.

**Table 4.** Training samples following spectral thinning.
| Tree crop type | Number samples |
| :---- | ----- |
| cocoa | 510,841 |
| coffee | 1,025,543 |
| forest | 1,022,309 |
| other | 1,064,910 |
| palm | 775,978 |
| rubber | 465,446 |

## Temporal Augmentation

To ameliorate unrealistically high interannual variability and to increase the available training samples, we performed temporal augmentation on the training and evaluation datasets.  The training data contain a year attribute, corresponding to the time of data collection *in situ* or the image acquisition date if visually interpreted.  We assume the label of each point to be valid in the entire year in which it was collected as well as any other year for which the spectral angle relative to the reference year is low ([Gong et al. 2019](https://www.sciencedirect.com/science/article/abs/pii/S2095927319301380)).  The spectral angle is computed as the arccos of the dot product of two feature vectors: the reference year vector and prospective year vector.  If the angle is less than 0.3, we assume the pixel to be unchanged and append the prospective year feature vector to the training or test set.  This was done for every year available in 2017-2024 for both the training and test sets.  Table 5 shows the number of examples per class for training and test, after the temporal augmentation.  

**Table 5.** Training and test datasets following temporal augmentation.

| Commodity | Training | Model Selection |
| :---- | ----- | ----- |
| cocoa | 937,376 | 32,792 |
| coffee | 1,306,201 | 1768 |
| forest | 4,247,073 | 315,378 |
| other | 3,795,442 | 529,677 |
| palm | 1,713,033 | 7854 |
| rubber | 856,085 | 21,121 |

## Classification

Prior to training, the spatially partitioned, spectrally filtered, and temporally extended data were converted to four separate one-hot datasets for cocoa, coffee, palm and rubber.  To make the table suitable for binary classification, the target variable was coded as 1 for the class of interest and 0 for all other classes.

Model training and classification were performed using a cloud-based infrastructure similar to Google Cloud AutoML ([Bisong et al., 2019](https://link.springer.com/book/10.1007/978-1-4842-4470-8)). Model architecture, activation functions, optimization routines, learning rates, batch sizes, and training iterations were selected through an automated hyperparameter search, with up to 24 hours allocated for optimization and 24 hours for training.  Model architecture is constrained to deep neural networks (DNNs), or networks with one or more hidden layers and one-dimensional inputs.  We used the model selection sets in the optimization phase, to choose architecture and parameters of models trained by the training set.

The final TensorFlow-based DNNs were hosted on Vertex AI and deployed in Google Earth Engine.  The models output probability of class occurrence as a scalar.

# Technical validation

Here we report calibration results on the model selection set and the Descals (2024b) palm validation dataset and the Descals (2024c) rubber validation set.  Although these sets may be of limited utility for understanding external validity, they offer insight into precision/recall tradeoffs at various probability thresholds.

## Model selection set

For the model selection set, the thresholds (and approximate accuracies) at the intersection of precision and recall curves shown in table 6.  

Table 6. Precision and recall at the specified thresholds on the model selection set.
| Commodity | Threshold | Precision/Recall |
| :---- | :---- | :---- |
| Cocoa | 0.54 | 94% |
| Coffee | 0.33 | 71% |
| Palm | 0.47 | 89% |
| Rubber | 0.35 | 94% |

### Cocoa

![cocoa_test_accuracy_2026a](/assets/images/cocoa_test_accuracy_2026a.png)

### Coffee

![coffee_test_accuracy_2026a](/assets/images/coffee_test_accuracy_2026a.png)

### Palm

![palm_test_accuracy_2026a](/assets/images/palm_test_accuracy_2026a.png)

### Rubber

![rubber_test_accuracy_2026a](/assets/images/rubber_test_accuracy_2026a.png)

## Descals et al. (2024b) palm

On the Descals et al. (2024b) palm dataset, the single class palm model gets approximately 84% accuracy at 0.58 probability threshold, at the intersection of precision and recall.

![descals_palm_accuracy_2026a](/assets/images/descals_palm_accuracy_2026a.png)

## Descals et al. (2024c) rubber

On the Descals et al. (2024c) rubber dataset, the single class rubber model gets approximately 81% accuracy at 0.3 probability threshold, at the intersection of precision and recall.

![descals_rubber_accuracy_2026a](/assets/images/descals_rubber_accuracy_2026a.png)

# Limitations

Known limitations of the 2026a release include the following.

## General

* Accuracies computed from the model selection set are overestimates. It is incumbent upon the consumer of the data to conduct localized accuracy assessments to ensure suitability for any particular purpose.  
* Model outputs experience interannual variation that does not reflect on-the-ground structural changes.  
* Input artifacts may be visually apparent in output probabilities and result in classification errors at some thresholds.  
* Training data is sparse and some geographies are not represented or under-represented.  For example, South Pacific islands (Fiji, Vanuatu, New Caledonia) lack reference data.

## Cocoa

* Commission errors with coffee occur in some areas (e.g., Huila, Colombia).

## Coffee

* Omission errors occur for coffee grown in multi-canopy agroecosystems. This is pronounced in the highland growing regions of Central America (e.g., San Marcos and Huehuetenango in Guatemala; Santa Bárbara and Copán in Honduras; Jinotega and Estelí in Nicaragua), East African forest coffee systems (e.g., Sidama and Yirga Chefe in Ethiopia), and Western India (Karnataka and Kerala).  
* Commission with tea occurs in some areas. These include highland monocultures, notably across Java, Indonesia and Tamil Nadu (Nilgiris), India.  
* Commission with bananas occurs in some areas (e.g., Veracruz, Mexico, Caribbean lowlands of Honduras; smallholder robusta/banana in Eastern Uganda).

## Palm

* Commission errors with natural forest occur in sago forests (e.g. Papua) and secondary forest regrowth (e.g., Maranhão and Roraima, Brazil).

## Rubber

* Commission errors may occur in dry/deciduous forests (Northern Thailand, Yucatan, Central America, West Africa) and outside historical core production provinces in China (e.g. outside Yunnan and Hainan).

# Data availability

**Table 7.** Publicly available 2026a datasets hosted in the Forest Data Partnership publisher catalog in Google Earth Engine.

| Layer | Earth Engine collection |
| ----- | ----- |
| Cocoa | ee.ImageCollection("projects/forestdatapartnership/assets/cocoa/model\_2026a") |
| Coffee | ee.ImageCollection("projects/forestdatapartnership/assets/coffee/model\_2026a") |
| Palm | ee.ImageCollection("projects/forestdatapartnership/assets/palm/model\_2026a") |
| Rubber | ee.ImageCollection("projects/forestdatapartnership/assets/rubber/model\_2026a") |
| Training data heatmap | ee.FeatureCollection("projects/forestdatapartnership/assets/training_data_2026a_one_degree_heatmap") |

# References

1. Becerra, Milagros; Rivera, Ovidio; Pawlak, Camila; Crocker, Alexandra; Pinto, Naiara. 2022\. Base de datos de cobertura de cultivos de cacao en la Amazonia Peruana. Harvard Dataverse, V3. [https://doi.org/10.7910/DVN/XMQNC2](https://doi.org/10.7910/DVN/XMQNC2)

2. Berger, K., Foerster, S., Szantoi, Z., Hostert, P., Foerster, M., Van De Kerchove, R., Vancutsem, C., Schweitzer, C., Masolele, R., Reiche, J., Dowell, M., Enssle, F., Requena Suarez, D., Nepomshina, O., & Herold, M. (2025). Evolving Earth observation capabilities for recent land-related EU policies. Land Use Policy, 158, 107749\. [https://doi.org/10.1016/j.landusepol.2025.107749](https://doi.org/10.1016/j.landusepol.2025.107749).

3. Bisong et al. 2019\. Building Machine Learning and Deep Learning Models on Google Cloud Platform. Springer.  [https://doi.org/10.1007/978-1-4842-4470-8](https://doi.org/10.1007/978-1-4842-4470-8) 

4. Bourgoin, Clement;  Verhegghen, Astrid;  Ameztoy, Iban;  Carboni, Silvia;  Achard, Frederic;  Colditz, Rene (2026): Global map of forest cover 2020 \- version 3\. European Commission, Joint Research Centre
Dataset
doi: 10.2905/JRC.354CG88 PID: [http://data.europa.eu/89h/8c561543-31df-4e1b-9994-e529afecaf54](http://data.europa.eu/89h/8c561543-31df-4e1b-9994-e529afecaf54)

5. Brown, C. F., Brumby, S. P., Guzder-Williams, B., Birch, T., Hyde, S., Mazzariello, J., Radoglou-Grammatikis, P., Rieke, M., Smith, A., Tzachor, A., Yeh, C., Zaitunah, A., Zambrano, F., & Zhang, R. 2022\. Dynamic World: Near real-time global 10 m land use land cover mapping. Scientific Data, 9, 251\. [https://doi.org/10.1038/s41597-022-01307-4](https://doi.org/10.1038/s41597-022-01307-4)

6. Brown, C.F., Kazmierski, M.R., Pasquarella, V.J., Rucklidge, W.J., Samsikova, M., Zhang, C., Shelhamer, E., Lahera, E., Wiles, O., Ilyushchenko, S. and Gorelick, N., 2025\. Alphaearth foundations: An embedding field model for accurate and efficient global mapping from sparse label data. [https://arxiv.org/abs/2507.22291](https://arxiv.org/abs/2507.22291) 

7. Centre for Remote Sensing and Geographic Information Services (CERSGIS). 2025\. Reference Dataset for Land Use Change Mapping in Ghana's Cocoa Landscape (2024–2025) (v2.0)
Dataset
. Zenodo. [https://doi.org/10.5281/zenodo.16579443](https://doi.org/10.5281/zenodo.16579443)

8. CIAT. 2025\. Data licensed by Google to train Forest Data Partnership models. *Unpublished dataset*.

9. Clinton, N., Vollrath, A., D’Annunzio, R., Liu, D., Glick, H. B., Descals, A., Guinan, O., Sullivan, A., Abramowitz, J., Stolle, F., Goodman, C., Birch, T., Quinn, D., Danylo, O., Lips, T., Coelho, D., Bihari, E., Cronkite-Ratcliff, B., Poortinga, A., Haghighattalab, A., Notman, E., DeWitt, M., Yonas, A., Donchyts, G., Shah, D., Saah, D., Tenneson, K., Nguyen, H. Q., Verma, M., & Wilcox, A. 2024\. A community palm model. arXiv. [https://arxiv.org/pdf/2405.09530](https://arxiv.org/pdf/2405.09530).

10. d'Annunzio, R., Abramowitz, J., Bale, F., Clinton, N., Dontenville, A., Dyson, K., Foresta, L., Freitas Beyer, J., Gasperini, L., Houdry, P., Hunka, N., Jonsson, Ö., Lindquist, E., Lippe, M., Monnier, B., Mushtaq, F., Orlowski, K., Poulenas, P., Rambaud, P., Rembold, F., Reymondin, L., Riano, C., Ribeiro, V., Ripplinger, P., Saah, D., Sagarra, L., Sannier, C., Schechtman, S., Shapiro, A., Sullivan, A., Tenneson, K., Valbuena Perez, M.P., Vantalon, T., Vollrath, A. & Wielgosz, B. 2026\. Forest monitoring good practices: mapping tree crop commodities. Rome, FAO. [https://doi.org/10.4060/cd9622en](https://doi.org/10.4060/cd9622en) 

11. Danylo, O., Pirker, J., Lemoine, G., Ceccherini, G., See, L., McCallum, I., Hadi, H., Kraxner, F., Achard, F., & Fritz, S. (2021). A map of the extent and year of detection of oil palm plantations in Indonesia, Malaysia and Thailand. Scientific Data, 8, 96\. [https://doi.org/10.1038/s41597-021-00867-1](https://doi.org/10.1038/s41597-021-00867-1)

12. Descals, A., Gaveau, D. L. A., Wich, S., Szantoi, Z., and Meijaard, E.: Global mapping of oil palm planting year from 1990 to 2021\. 2024a. Earth Syst. Sci. Data, 16, 5111–5129. [https://doi.org/10.5194/essd-16-5111-2024](https://doi.org/10.5194/essd-16-5111-2024) 

13. Descals, Adria. 2024b. Global oil palm extent and planting year from 1990 to 2021 (v1.2)
Dataset
. Zenodo. [https://doi.org/10.5281/zenodo.13379129](https://doi.org/10.5281/zenodo.13379129)

14. Descals, A. 2024c. Validation dataset for the article 'Rubber planting and deforestation' (Version v1.1)
Dataset
. Zenodo. [https://doi.org/10.5281/zenodo.10646349](https://doi.org/10.5281/zenodo.10646349) 

15. European Commission. 2023\. Regulation (EU) 2023/1115 of the European Parliament and of the Council of 31 May 2023 on the making available on the Union market and the export from the Union of certain commodities and products associated with deforestation and forest degradation and repealing Regulation (EU) No 995/2010 (Text with EEA relevance). (European Commission, 2023).

16. Forest Data Partnership. 2024\. A community forest model. [https://github.com/google/forest-data-partnership/edit/main/models/forests](https://github.com/google/forest-data-partnership/edit/main/models/forests)

17. Forest Data Partnership. 2025\. Community models 2025b. [https://github.com/google/forest-data-partnership/edit/main/models/model\_2025b/README.md](https://github.com/google/forest-data-partnership/edit/main/models/model_2025b/README.md) 

18. Freitas Beyer, J., Köthke, M., & Lippe, M. 2025\. Assessing the suitability of available global forest maps as reference tools for EUDR-compliant deforestation monitoring. Remote Sensing, 17(17), 3012\. [https://doi.org/10.3390/rs17173012](https://doi.org/10.3390/rs17173012)

19. Fricker, Geoffrey; Nielsen, Kylee; Clark, Isabella; Davis, Jaxson; Bates, Sarah; Davis, Isabella; Pinto, Naira. 2022\. Palm Oil Polygons for Ucayali Province, Peru (2019-2020). Harvard Dataverse, V3. [https://doi.org/10.7910/DVN/BSC9EI](https://doi.org/10.7910/DVN/BSC9EI)

20. Goldman, E., Weisse, M. J., Harris, N., & Schneider, M. 2020\. Estimating the role of seven commodities in agriculture-linked deforestation: Oil palm, soy, cattle, wood fiber, cocoa, coffee, and rubber (Technical Note). World Resources Institute.

21. Peng Gong, Han Liu, Meinan Zhang, Congcong Li, Jie Wang, Huabing Huang, Nicholas Clinton, Luyan Ji, Wenyu Li, Yuqi Bai, Bin Chen, Bing Xu, Zhiliang Zhu, Cui Yuan, Hoi Ping Suen, Jing Guo, Nan Xu, Weijia Li, Yuanyuan Zhao, Jun Yang, Chaoqing Yu, Xi Wang, Haohuan Fu, Le Yu, Iryna Dronova, Fengming Hui, Xiao Cheng, Xueli Shi, Fengjin Xiao, Qiufeng Liu, Lianchun Song. 2019\. Stable classification with limited sample: transferring a 30-m resolution sample set collected in 2015 to mapping 10-m resolution global land cover in 2017\. *Science Bulletin*. Volume 64, Issue 6\. [https://doi.org/10.1016/j.scib.2019.03.002](https://doi.org/10.1016/j.scib.2019.03.002). 

22. Google LLC. 2025\. Manually digitized commodity production reference dataset. *Unpublished dataset*.

23. Gorelick, Noel, Matt Hancher, Mike Dixon, Simon Ilyushchenko, David Thau, Rebecca Moore.  2017\.  Google Earth Engine: Planetary-scale geospatial analysis for everyone. Remote Sensing of Environment. [https://doi.org/10.1016/j.rse.2017.06.031](https://doi.org/10.1016/j.rse.2017.06.031)

24. Kalischek, N., Lang, N., Renier, C., Caye Daudt, R., Addoah, T., Thompson, W., Blaser-Hart, W. J., Garrett, R., Schindler, K., & Wegner, J. D. (2023). Cocoa plantations are associated with deforestation in Côte d’Ivoire and Ghana. Nature Food, 4(5), 384–393. [https://doi.org/10.1038/s43016-023-00751-8](https://doi.org/10.1038/s43016-023-00751-8)

25. Lescuyer, Guillaume. 2024\. Inventaire des arbres dans 223 cacaoyères agroforestières au Cameroun. CIRAD Dataverse, V1. [https://doi.org/10.18167/DVN1/MGDIJU](https://doi.org/10.18167/DVN1/MGDIJU)

26. MapBiomas. 2023\. Mapeamento do Cultivo de Cacau Sombreado em 83 Municípios do Sul da Bahia. [https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/relat\_mapbiomas\_cacau\_83mun\_final.pdf](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/relat_mapbiomas_cacau_83mun_final.pdf)

27. Meridia. 2025\. Data licensed by Google to train Forest Data Partnership models. *Unpublished dataset*.

28. Neumann, M., Raichuk, A., Jiang, Y. et al. Natural forests of the world – a 2020 baseline for deforestation and degradation monitoring. 2025\. Scientific Data. 12, 1715\. [https://doi.org/10.1038/s41597-025-06097-z](https://doi.org/10.1038/s41597-025-06097-z) 

29. Olam Food Ingredients (OFI) Coffee Unit. 2025\. Data licensed by Google to train Forest Data Partnership models. *Unpublished dataset*.

30. Parente, L., Sloat, L., Mesquita, V., Consoli, D., Stanimirova, R., Hengl, T., Bonannella, C., Teles, N., Wheeler, I., Hunter, M., Ehrmann, S., Ferreira, L., Mattos, A., Oliveira, B., Meyer, C., Şahin, M., Witjes, M., Fritz, S., Malek, Z., & Stolle, F. (2024). Annual 30-m maps of global grassland class and extent (2000-2022) based on spatiotemporal machine learning. Scientific Data, 11, Article 1303\. [https://doi.org/10.1038/s41597-024-04139-6](https://doi.org/10.1038/s41597-024-04139-6)

31. Poortinga, A., Tenneson, K., Shapiro, A., Nquyen, Q., San Aung, K., Chishtie, F. and Saah, D., 2019\. Mapping plantations in Myanmar by fusing Landsat-8, Sentinel-2 and Sentinel-1 data along with systematic error quantification. Remote sensing, 11(7), p.831. [https://doi.org/10.3390/rs11070831](https://doi.org/10.3390/rs11070831) 

32. Wafiq, M. W., Cutter, P., Poortinga, A., dela Torre, D. M. G., Tenneson, K., Teck, V., Bihari, E., Saisaward, C., Suaruang, W., McMahon, A., Andi Vika Faradiba, M., Batiran, K. B., A, C., Nurul, Q., Arya Arismaya, M., Ganz, D., & Saah, D. (2025). Open Land Use Reference Dataset for Palm Oil Landscapes in Indonesia (Version 0.1). RECOFTC. [https://doi.org/10.5281/zenodo.15618532](https://doi.org/10.5281/zenodo.15618532) 

33. Richter, J., Goldman, E., Harris, N. L., Gibbs, D., Rose, M., Peyer, S., Richardson, S. B., & Velappan, H. (2024). Spatial Database of Planted Trees (SDPT version 2.0)
TechnicalNote
. World Resources Institute. [https://doi.org/10.46830/writn.23.00073](https://doi.org/10.46830/writn.23.00073)

34. Schneider, M., C. Winchester, E. Goldman, and Y. Shao. 2023\. “Mapping cocoa and assessing deforestation risk for the cocoa sector in Côte d’Ivoire and Ghana.” Technical Note. Washington, DC: World Resources Institute. Available online at: [doi.org/10.46830/writn.21.00011](http://doi.org/10.46830/writn.21.00011) 

35. Shapiro, Aurelie. 2024\. Cocoa reference data in Cameroon. UN FAO. *Unpublished dataset*.

36. Sheil, D., Descals, A., Meijaard, E. et al. Rubber planting and deforestation. Nature 644, E20–E22 (2025). [https://doi.org/10.1038/s41586-025-08848-9](https://doi.org/10.1038/s41586-025-08848-9) 

37. Song, X.-P., Hansen, M. C., Potapov, P. V., Adusei, B., Pickering, J., & Adami, M. (2021). Massive soybean expansion in South America since 2000 and implications for conservation. Nature Sustainability, 4(9), 784–792. [https://doi.org/10.1038/s41893-021-00729-z](https://doi.org/10.1038/s41893-021-00729-z)

38. Souza, C. M., Jr., Shimbo, J. Z., Rosa, M. R., Parente, L. L., Alencar, A. A., Rudorff, B. F. T., Hasenack, H., Matsumoto, M., Ferreira, L. G., Souza-Filho, P. W. M., de Oliveira, S. W., Rocha, W. F., Fonseca, A. V., Marques, C. B., Diniz, C. G., Costa, D., Monteiro, D., Rosa, E. R., Vélez-Martin, E., Weber, E. J., Lenti, F. E. B., Paternost, F. F., Pareyn, F. G. C., Siqueira, J. V., Viera, J. L., Ferreira Neto, L. C., Saraiva, M. M., Sales, M. H., Salgado, M. P. G., Vasconcelos, R., Galano, S., Mesquita, V. V., & Azevedo, T. 2020\. Reconstructing three decades of land use and land cover changes in Brazilian biomes with Landsat archive and Earth Engine. Remote Sensing, 12(17), 2735\. [https://doi.org/10.3390/rs12172735](https://doi.org/10.3390/rs12172735)

39. Stanimirova, R., Tarrio, K., Turlej, K., McAvoy, K., Stonebrook, S., Hu, K.-T., Arévalo, P., Bullock, E. L., Zhang, Y., Woodcock, C. E., Olofsson, P., Zhu, Z., Barber, C. P., Souza, C. M. Jr., Chen, S., Wang, J. A., Mensah, F., Calderón-Loor, M., Hadjikakou, M., Bryan, B. A., Graesser, J., Beyene, D. L., Mutasha, B., Siame, S., Siampale, A., & Friedl, M. A. (2023). A global land cover training dataset from 1984 to 2020\. Scientific Data, 10, 879\. [https://doi.org/10.1038/s41597-023-02798-5](https://doi.org/10.1038/s41597-023-02798-5)

40. Tarrio, Katelyn. 2026\. Plantation land use drives forest change in West Africa. *In prep*.

41. Vantalon, Thibaud, Phuong Thi Luong, Jorge Andres Perez Escobar, Jhon Jairo Tello Dagua, Trong Van Phan, Hang Nguyen, Hong Nguyen, Hoa Nguyen, and Louis Reymondin. 2025\. “Sample Earth: Machine-Learning\&ndash;Ready Land-Cover Reference Dataset.” Harvard Dataverse. [https://doi.org/10.7910/DVN/U7HWY1](https://doi.org/10.7910/DVN/U7HWY1) 

42. Vollrath, Andreas, Jennifer Adams, Sara Aparicio, and John Mrziglod. A global palm oil map for the year 2017 using multi-sensor sar imagery. 2019\. Living Planet Symposium. ESA/ESRIN, Frascati, Italy.

43. Wang, Y., Hollingsworth, P. M., Zhai, D., West, C. D., Green, J. M. H., Chen, H., Hurni, K., Su, Y, Warren-Thomas, E., Xu, J., & Ahrends, A. 2023\. High-resolution maps show that rubber causes substantial deforestation. Nature, 623, 340–346. [https://doi.org/10.1038/s41586-023-06642-z](https://doi.org/10.1038/s41586-023-06642-z) 

44. Zanaga, D., Van De Kerchove, R., De Keersmaecker, W., Souverijns, N., Brockmann, C., Quast, R., Wevers, J., Grosu, A., Paccini, A., Vergnaud, S., Cartus, O., Santoro, M., Fritz, S., Georgieva, I., Lesiv, M., Carter, S., Herold, M., Li, Linlin, Tsendbazar, N.E., Ramoino, F., Arino, O., 2021\. ESA WorldCover 10 m 2020 v100. [https://doi:10.5281/zenodo.5571936](https://doi:10.5281/zenodo.5571936)

# Suggested citation
Forest Data Partnership. 2026a. Community models 2026a. https://github.com/google/forest-data-partnership/edit/main/models/model_2026a/README.md
