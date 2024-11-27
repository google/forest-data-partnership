# Methods summary

We used the mean of an ensemble of publicly available datasets chosen to represent the persistence of forest cover over the observation period, defined as 1984-2020. We used LandTrendr to examine pixels for disturbance over the observation period. Persistent forest, with no evidence of disturbance (anthropogenic or otherwise), is assumed to represent forest where "ecological processes are not significantly disturbed." (European Commission 2023).

## Input datasets

Hansen et al. (2013) global forest change data at 30 meters resolution were used to create an indicator variable (oldForest), defined as one if pixels that were labeled as forest (according to Hansen et al.) in 2000 had not shown any deforestation events. Illogical scenarios (e.g. forest that was not forest in 2000,not identified as forest again, but showed loss) were identified and used to set the oldForest indicator to zero.

Palsar annual forest/non-forest composites (Shimada et al. 2013) at approximately 25 meters resolution between 2017-2020 were used to create a score variable (palsarForest) defined as the fraction of years the pixel was labeled either sparse or dense forest. The score is one if the pixel is consistently either sparse or dense (it can not switch between densities) over the observation period.

The WorldCover v100 product, a 2020 land cover map at 10 meters resolution (Zanaga et al. 2020) was used to create an indicator variable (wcTrees) defined as one if the pixel is labeled as "trees" in the WorldCover dataset and zero otherwise. There must be trees in the forest for it to be forest.

The European Commission Joint Research Center (JRC) forest/non-forest map of 2020 (Bourgoin et al. 2024), at 10 meters resolution, was used to create a single indicator variable (jrcForest) which is one if the pixel is labeled as forest by the JRC dataset, zero otherwise.

The LandTrendr temporal break-point algorithm (Kennedy et al. 2010) was applied to the Google TimeLapse dataset (https://earthengine.google.com/timelapse/) at 30 meters resolution in years 1984-2020. Since TimeLapse was designed as a visualization in RGB, the exG vegetation index (Woebbecke et al. 1995) was used as a single band input to LandTrendr. The results of LandTrendr include data indicating whether a disturbance was detected. An indicator variable (noChange) summarizing the output is one if no-disturbance was detected in a given pixel, and zero otherwise.

Several datasets represent "primary," "mature," or "undisturbed" forest in geographic regions. For example, the JRC produces a Tropical Moist Forest dataset (Vancutsem et al. 2021) at 10 meter resolution with classes that include "Undisturbed Tropical Moist Forest (TMF)," "deforestation" starting in 2021, 2022, and 2023 and "degradation" starting in 2023. From this dataset we created a single indicator variable (tmfForest) defined as one if the pixel was labeled "Undisturbed Tropical Moist Forest (TMF)" or if the deforestation or degradation occurred in 2021, 2022, 2023 (i.e. it was undisturbed in 2020). Turubanova et al. (2018) produced a map of "primary humid tropical forests" for 2001 at approximately 30 meters resolution. An indicator variable was defined from the Turubanova et al. map (humPrim) which is one if the pixel is labeled as humid primary tropical forest and there was no recorded forest loss in the Hansen et al. dataset at the same location. Because tmfForest and humPrim both characterize the same geographic area (the tropics), they were combined into a single variable (tropicsScore) which is the mean of the two indicator variables.

Other regions with estimated forest age datasets include The United States (US), Canada and the European Union (EU). For the US, DellaSala et al. (2022) produced a map of estimated forest "maturity" levels for the conterminous US, at 30 meters resolution. Although the published data do not reference a year, we assume the data are a fair representation of forest maturity level in 2020. These data were converted to a continuous score (usYim) by dividing the ordinal scale of the data by its maximum (9, for the most "mature" forests) and clamping to [0, 1]. For Canada, Maltman et al. (2023) produced a 2019 map of estimated forest age classes at 30 meter resolution. Through comparison to the DellaSalla et al. (2022) US map in areas of overlap, we determined empirically that the Maltman et al. (2022) map could be converted to a continuous score that approximately matched the US data by dividing the estimated forest age in Canada by 90 (years) and clamping to [0, 1]. That is, forest areas estimated to be over 90 years old and older in the Canada dataset receive a score of 1. In the EU, Sabatini et al. (2022) produced a vector database of "primary" forests corresponding approximately to year 2017. The database contains points and polygons, which we rasterized at 10 meters resolution and converted to an indicator variable, one if the pixel is in the database, zero otherwise.
The geographically distinct datasets representing the tropics, US, Canada, and the EU were mosaicked to produce a single layer of input to the ensemble. This is to keep the number of datasets approximately equal at global scale, since all other input datasets are already global.

## Combination rule

A simple, non-trainable combination rule was applied: the arithmetic mean of the variables described above. Although simple, the mean combiner may be optimal for some problem spaces or in the absence of other information (Kuncheva 2014).

## Accuracy

Due to the absence of a contemporaneous independent global validation dataset for 2020, we assessed the accuracy of  the mean combiner output using the training data in Lesiv et al. (2022). With a goal of assessing separability of mature forest from other classes, including tree crops.  Specifically, classes "Naturally regenerating forest without any signs of human activities, e.g., primary forests" and "Naturally regenerating forest with signs of human activities, e.g., logging, clear cuts etc." were set to 1 as proxies for persistent and minimally disturbed forest and all other classes (other kinds of forest or other land cover categories) were set to zero as proxies for disturbed forest and non-forest . Although the Lesiv et al. (2022) data are nominally for 2015 and at 100m resolution, resulting in a temporal and spatial mismatch, the comparison is relevant if change at the reference points is considered negligible. The reclassification of Lesiv et al. (2022) was compared to the continuous ForestPersistence mean combiner output to generate precision, recall F1 score and overall accuracy (n=216,323). At threshold 0.75 on the persistence scores, precision, recall and accuracy are all ~74%.

## Limitations

Geographic scope is limited to +/- 80 degrees latitude and to calendar year 2020. Not all geographic regions are equally represented. For example, China, Russia, Australia, New Zealand and other countries lack regionally specific datasets in the ensemble. Boreal forest may not be well represented. This dataset is built from existing datasets, and any limitations and errors associated with those datasets may be present. Landsat TimeLapse is a Google developed product that has not been used with LandTrendr previously. A probability sample of these types of forest cover coincident with the year 2020 is not available, making accuracy difficult to assess.

## References

Kuncheva, L.I., 2014. Combining pattern classifiers: methods and algorithms. https://doi.org/10.1002/0471660264

European Commission. 2023. Regulation of the european parliament and of the council on the making available on the union market and the export from the union of certain commodities and products associated with deforestation and forest degradation and repealing regulation (eu) no 995/2010. data.consilium.europa.eu/doc/document/PE-82-2022-INIT/en/pdf 

M. C. Hansen et al., 2013, High-Resolution Global Maps of 21st-Century Forest Cover Change. Science342,850-853. https://doi.org/10.1126/science.1244693 

Masanobu Shimada, Takuya Itoh, Takeshi Motooka, Manabu Watanabe, Tomohiro Shiraishi, Rajesh Thapa, Richard Lucas. 2014. New global forest/non-forest maps from ALOS PALSAR data (2007–2010), Remote Sensing of Environment, Volume 155, Pages 13-31, ISSN 0034-4257, https://doi.org/10.1016/j.rse.2014.04.014 

Zanaga, D. 2021. “ESA WorldCover 10 m 2020 v100”. Zenodo. https://doi.org/10.5281/zenodo.5571936 

Bourgoin, C., Ameztoy, I., Verhegghen, A. et al. 2024. Mapping global forest cover of the year 2020 to support the EU regulation on deforestation-free supply chains. Publications Office of the European Union. https://data.europa.eu/doi/10.2760/262532 

Kennedy, Robert E., Zhiqiang Yang, Warren B. Cohen. 2010. Detecting trends in forest disturbance and recovery using yearly Landsat time series: 1. LandTrendr — Temporal segmentation algorithms. Remote Sensing of Environment. Volume 114, Issue 12, Pages 2897-2910, https://doi.org/10.1016/j.rse.2010.07.008 

D. M. Woebbecke, G. E. Meyer, K. Von Bargen, D. A. Mortensen.  1995.  Color Indices for Weed Identification Under Various Soil, Residue, and Lighting Conditions.  Transactions of the ASAE. 38(1): 259-269. https://doi.org/10.13031/2013.27838

C. Vancutsem et al. 2021.  Long-term (1990–2019) monitoring of forest cover changes in the humid tropics. Sci. Adv. https://doi.org/10.1126/sciadv.abe1603 

Svetlana Turubanova, Peter V Potapov, Alexandra Tyukavina and Matthew C Hansen.  2018. Ongoing primary forest loss in Brazil, Democratic Republic of the Congo, and Indonesia.  Environ. Res. Lett. 13. https://doi.org/10.1088/1748-9326/aacd1c 

DellaSala, D.A., Mackey, B., Norman, P., Campbell, C., Comer, P.J., Kormos, C.F., Keith, H. and Rogers, B. 2022. Mature and old-growth forests contribute to large-scale conservation targets in the conterminous United States. Frontiers in Forests and Global Change, 5, p.979528. https://doi.org/10.3389/ffgc.2022.979528

Sabatini, F.M., Bluhm, H., Kun, Z. et al. 2021. European primary forest database v2.0. Scientific Data. 8, 220. https://doi.org/10.1038/s41597-021-00988-7 

Lesiv, M., Schepaschenko, D., Buchhorn, M. et al. Global forest management data for 2015 at a 100 m resolution. 2022. Scientific Data. 9, 199. https://doi.org/10.1038/s41597-022-01332-3

## Suggested citation

Forest Data Partnership. 2024.  ForestPersistence.  https://github.com/google/forest-data-partnership/edit/main/models/forests
