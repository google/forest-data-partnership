# Methods summary

## Input datasets
The input datasets and model selection process are the same as described in Clinton et al. (2024) for palm mapping: input data are annual composites of Sentinel-1, Sentinel-2, ALOS PALSAR-2, and slope derived from global DEMs.

## Model

The training data are split into three geographic folds and a platform similar to Google AutoML selects an optimal model architecture and parameters.  One fold is used for training, one for model/parameter selection and one for validation.  The model type is per-pixel (i.e. not convolutional), meaning input is a 1-D vector.  Model training and selection is performed as described in Clinton et al. (2024).

## Training data

Training data come from a variety of sources. Wang et al. (2023) provided 4931 publicly available reference samples representing deciduous forest (982), forest (1890) and rubber (2059) as of 2021, which were reclassified as rubber presence (1) or absence (0). K. Tarrio provided 8168 rubber samples over 2019-2023 across West Africa (Ghana, Cote d’Ivoire, Liberia, Guinea) via visual interpretation of very high resolution imagery from Google Earth (Stanimirova et al., 2023). K. Tarrio also generated hand-digitized partial field boundaries over southern Guatemala (320), which were then sampled to produce 30,759 positive rubber samples at 50m resolution; similarly, for Hainan Island, China, K. Tarrio created 128 partial field boundary polygons which were sampled at 10m resolution to produce 330,238 positive rubber samples. A. Poortinga provided 49,368 samples of rubber across Southeast Asia. 

Absences were derived from presence of other crops.  Cocoa (n=77,041, Becerra et al. 2022), palm (n=43,638, Fricker et al. 2022), and degraded forest (n=52,592, Cooley et al. 2021) in Peru were used as rubber absences.  Palm presence (n=137,070) created by Google (detailed in Clinton et al. 2024) and cocoa (n=30,213) from a Cote d' Iviore land cover map (BNETD Land Cover Map 2020) were also used as rubber absence data.  Pseudoabsences (assumed absence of rubber, n=52,609) were generated from ancillary datasets on forest and land cover as described in Clinton et al. (2024).

Validation data come from the Sheil et al. (2024) dataset, which was produced as critique to the Wang et al. (2023) paper.  Sheil et al. (2024) show that the accuracy assessment strategy employed by Wang et al. (2023) was spatially biased.  They generated a publicly available stratified random sample (Descals et al. 2024) using recommended guidelines (Olofsson et al. 2014).

## Accuracy

Accuracy was assessed relative to the Sheil et al. (2024) dataset.  At a threshold of ~0.92 on the probability output, precision, recall and F1 score are all ~78%.  Accuracy is ~93%.  Accuracy will vary according to user selected threshold.

## Limitations

Model output is limited to selected countries as calendar year composites for 2020 and 2023.  Not all regions of the output are represented by training data.  Accuracy is reported in aggregate, is based on a notional threshold, and will vary geographically and with user chosen thresholds.  Sensor artifacts based on data availability, cross-track nonuniformity, or cloudiness may be visually apparent in output probabilities and result in classification errors at some thresholds.

## References

Wang, Y., Hollingsworth, P.M., Zhai, D. et al. High-resolution maps show that rubber causes substantial deforestation.  2023.  Nature 623, 340–346. https://doi.org/10.1038/s41586-023-06642-z

Stanimirova, R., Tarrio, K., Turlej, K. et al. A global land cover training dataset from 1984 to 2020.  2023. Scientific Data 10, 879. https://doi.org/10.1038/s41597-023-02798-5

Becerra, Milagros; Rivera, Ovidio; Pawlak, Camila; Crocker, Alexandra; Pinto, Naiara.  2022.  Base de datos de cobertura de cultivos de cacao en la Amazonia Peruana.  Harvard Dataverse, V3.  https://doi.org/10.7910/DVN/XMQNC2

Fricker, Geoffrey; Nielsen, Kylee; Clark, Isabella; Davis, Jaxson; Bates, Sarah; Davis, Isabella; Pinto, Naira.  2022.  Palm Oil Polygons for Ucayali Province, Peru (2019-2020). Harvard Dataverse, V3.  https://doi.org/10.7910/DVN/BSC9EI

Cooley, S., Pinto, N., Aguilar-Amuchastegui, N., Vela Alvarado, J., & Fahlen, J. 2021. Vegetation typology classification and data set in Ucayali, Peru (4.0). CaltechDATA. https://doi.org/10.22002/D1.2318 

Clinton et al. 2024.  A community palm model. arXiv. https://arxiv.org/pdf/2405.09530

Sheil,  D., Descals,  A., Meijaard,  E., & Gaveau,  D.  2024. Rubber Planting and Deforestation. Preprints. https://doi.org/10.20944/preprints202402.0743.v1

Descals, A. 2024. Validation dataset for the article 'Rubber planting and deforestation' (v1.1). Zenodo. https://doi.org/10.5281/zenodo.10646349

Olofsson, Pontus, Giles M. Foody, Martin Herold, Stephen V. Stehman, Curtis E. Woodcock, Michael A. Wulder.  2014.  Good practices for estimating area and assessing accuracy of land change, Remote Sensing of Environment, Volume 148, Pages 42-57.  https://doi.org/10.1016/j.rse.2014.02.015 

## Suggested citation

Forest Data Partnership. 2024.  Rubber model 2024a.  https://github.com/google/forest-data-partnership/edit/main/models/rubber


