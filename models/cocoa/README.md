# Methods summary

## Input datasets
The input datasets and model selection process are the same as described in Clinton et al. (2024) for palm mapping: input data are annual composites of Sentinel-1, Sentinel-2, ALOS PALSAR-2, and slope derived from global DEMs.

## Model
The training data are randomly split into three sets and a platform similar to Google AutoML selects an optimal model architecture and parameters.  One set is used for training (80%), one for model/parameter selection (10%) and one for validation (10%).  The model type is per-pixel (i.e. not convolutional), meaning input is a 1-D vector.  Model training and selection is performed as described in Clinton et al. (2024), except folds are random instead of geographic.

## Training data
Training data (n=3,013,826) come from a variety of sources. World Resources Institute (WRI) provided the West Africa Cocoa dataset, an anonymized database of mapped cocoa plot locations compiled from data collected by 19 companies. Positive and negative training points were also sampled from the Cote d'Ivoire BNETD 2020 Land Cover Map, which was produced by the Ivorian Government through a national institution, the Center for Geographic Information and Digital from the National Study Office Techniques and Development (BNETD-CIGN). CIRAD provided publicly available inventory of trees in 223 agroforestry cocoa plantations in Cameroon (Lescuyer 2024). SERVIR Amazonia provided publicly available polygons of cocoa in Peru in 2020 (Becerra et al. 2022). A. Shapiro provided data in Cameroon in the form of a field survey of points from March 2024, and manually annotated non-cocoa regions, through the COCAFORI project. Training data were also cross-referenced with the cocoa farming map by N. Kalishek et al. (2023).

Absences were derived from presence of other crops. Palm presence created by Google (detailed in Clinton et al. 2024) as well as palm data in Peru (Fricker et al. 2022) were used as cocoa absences. Rubber presence data (Forest Data Partnership 2024a) were used as cocoa absences. Pseudoabsences (assumed absence of cocoa) were generated from ancillary datasets on forest and land cover as described in Forest Data Partnership (2024b).

## Accuracy

An independent validation dataset was not available.  Instead, accuracy was assessed on the 10% of the data that were not used in model training or selection.  At 0.5 threshold on the output probabilities, precision is ~90%, recall is ~91% and accuracy is ~97%.  These are likely to be optimistic estimates, overestimating accuracy due to spatial autocorrelation between the training, model selection and validation data.

## Limitations

Model output is limited to selected countries as calendar year composites for 2020 and 2023.  Not all regions of the output are represented by training data.  Accuracy is reported in aggregate, is based on a notional threshold, and will vary geographically and with user chosen thresholds.  Sensor artifacts based on data availability, cross-track nonuniformity, or cloudiness may be visually apparent in output probabilities and result in classification errors at some thresholds.

## References

Lescuyer, Guillaume. 2024. Inventaire des arbres dans 223 cacaoyères agroforestières au Cameroun. CIRAD Dataverse, V1. https://doi.org/10.18167/DVN1/MGDIJU

Becerra, Milagros; Rivera, Ovidio; Pawlak, Camila; Crocker, Alexandra; Pinto, Naiara.  2022.  Base de datos de cobertura de cultivos de cacao en la Amazonia Peruana.  Harvard Dataverse, V3.  https://doi.org/10.7910/DVN/XMQNC2

Kalischek, N., Lang, N., Renier, C. et al. 2023. Cocoa plantations are associated with deforestation in Côte d’Ivoire and Ghana. Nature Food. 4, 384–393. https://doi.org/10.1038/s43016-023-00751-8

Fricker, Geoffrey; Nielsen, Kylee; Clark, Isabella; Davis, Jaxson; Bates, Sarah; Davis, Isabella; Pinto, Naira.  2022.  Palm Oil Polygons for Ucayali Province, Peru (2019-2020). Harvard Dataverse, V3.  https://doi.org/10.7910/DVN/BSC9EI

Clinton et al. 2024.  A community palm model. arXiv. https://arxiv.org/pdf/2405.09530

Forest Data Partnership. 2024a.  Rubber model 2024a.  https://github.com/google/forest-data-partnership/edit/main/models/rubber

Forest Data Partnership. 2024b.  A community forest model.  https://github.com/google/forest-data-partnership/edit/main/models/forests

## Suggested citation

Forest Data Partnership. 2024.  Cocoa model 2024a.  https://github.com/google/forest-data-partnership/edit/main/models/cocoa
