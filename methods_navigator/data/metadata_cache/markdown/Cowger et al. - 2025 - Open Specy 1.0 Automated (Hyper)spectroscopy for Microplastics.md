pubs.acs.org/ac 

Article 

**==> picture [177 x 69] intentionally omitted <==**

## **Open Specy 1.0: Automated (Hyper)spectroscopy for Microplastics** 

Win Cowger,* Aleksandra Karapetrova, Clarissa Lincoln, Ali Chamas, Hannah Sherrod, Nicholas Leong, Katherine S. Lasdin, Christine Knauss, Vesna Teofilovic, Monica M. Arienzo, Zacharias Steinmetz, Sebastian Primpke, Lindsay Darjany, Clare Murphy-Hagan, Shelly Moore, Charles Moore, Gwen Lattin, Andrew Gray, Rachel Kozloski, Jeremiah Bryksa, and Benjamin Maurer 

**Cite This:** _Anal. Chem._ 2025, 97, 17345−17356 **Read Online** 

ACCESS Metrics & More Article Recommendations * **sı** Supporting Information 

ABSTRACT: Microplastic spectral analysis is one of the most timeconsuming processes in studying microplastic pollution, often requiring days per sample. Researchers are transitioning to automated batch and hyperspectral image analysis techniques to enhance efficiency. Open Specy, initially aimed at manual single-spectrum analysis, has now integrated automated methods. This updated version, Open Specy 1.0, introduces several new features, including two algorithms for automated processing (smoothing and particle compression), an extensive library containing over 40,000 open-source Raman and FTIR spectra, and two machine learning classifiers (logistic regression and k medoids) developed from this library. Furthermore, it includes a revamped user interface, an R package, and a 

**==> picture [201 x 109] intentionally omitted <==**

benchmark data set for testing future advancements in automated techniques. Researchers evaluated various configurations for hyperspectral smoothing, particle identification, compression, and splitting, to achieve combined recovery rates between 50 and 150% particle counts, identities, and sizes with a coefficient of variation (CV) of less than 40% (the accredited standard). Mean absorbance times the standard deviation provided a consistent particle identification. Hyperspectral smoothing led to a 96% combined recovery rate and reduced variability (CV = 38%) compared to the 86% recovery (CV = 83%) of nonsmoothed controls. Additionally, compressing spectra for particles was significantly faster (>3×) and showed similar accuracy but with reduced variability than processing each pixel individually. Key challenges persist in automating spectral analysis, particularly in refining particle splitting algorithms, and improving identification routines to minimize false positives and negatives. New methods in sample preparation for better stabilization and dispersion of particles could overcome some of these issues. 

## ■ **[INTRODUCTION]** 

Microplastics, tiny plastic fragments less than 5 mm in size,[1] are pervasive in oceans,[2] rivers,[3] soil,[4] and even the air we breathe.[5] They threaten marine life, ecosystems, and potentially human health.[6][,][7] Microplastic’s persistence, slow degradation, and the high rate of plastic production and pollution make them accumulate in the environment.[8] To adequately address microplastic pollution, the world needs accurate automated techniques for microplastic analysis. 

Traditional methods of detecting and analyzing microplastics are resource-intensive, time-consuming, and prone to human error.[9] At the time of writing, most laboratories use manual approaches combining visual microscopy (accurate for particles >200 _μ_ m)[10] for preliminary identification, followed by manual particle-by-particle spectroscopic (typically Raman or FTIR) analysis of a subsample of particles (∼100),[11] which requires days of effort per sample.[12] Collecting more spectral data using this approach is not feasible for most studies; however, some groups are overcoming this barrier using plate readers.[9] Automated spectroscopy offers a robust solution by providing accurate and reproducible analysis,[9][,][13][,][14] ultimately 

contributing to more effective environmental protection and public health measures. 

Hyperspectral imaging is an automated spectroscopy technique often used to assess particles smaller than 500 _μ_ m in size.[15] Midinfrared (FTIR) (covered here) and Raman hyperspectral imaging are common hyperspectral imaging modes for microplastics, while SWIR, NIR, visible, and fluorescence imaging have also been explored to a lesser extent.[16][−][19] This approach collects many (typically >10,000) spatially referenced spectra of samples at small spatial scales (<50 _μ_ m) through “imaging” a predefined area.[20] Collection of the hyperspectral image is faster (∼30 min total) for the instrument operator than manual particle-by-particle spectroscopic analysis. Even though an image could take many hours 

**==> picture [39 x 59] intentionally omitted <==**

Received: February 13, 2025 Revised: July 29, 2025 Accepted: August 5, 2025 Published: August 11, 2025 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

© 2025 American Chemical Society 

**17345** 

**Analytical Chemistry** 

Article 

**==> picture [56 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
pubs.acs.org/ac<br>**----- End of picture text -----**<br>


**==> picture [349 x 307] intentionally omitted <==**

Figure 1. Workflow diagram of automated analysis components and variables. Batch analysis deals with more than one spectrum at a time. Domain alignment involves converting collected spectra into the same transformation as the reference library. Spectral identification involves comparing reference and unknown spectra to identify them and typically involves correlation between paired absorbance values shown here. Thresholds of the identification match values can be used to differentiate confident from unconfident identifications; shown here is the use of a 0.7 threshold to relabel spectra <0.7 as unknown. Top matches can be pooled to determine an identification. Shown here is a simple pooling where the percent of the class labels in the top 3 matches is used to identify the spectra instead of the top correlation threshold alone. Hyperspectral analysis is a type of batch analysis where the spectra also have a spatial coordinate system. During hyperspectral smoothing, spectra from nearby cells are averaged to reduce noise. Particle locations can be identified using a thresholding of basic spectral statistics. All spectra for individual particles can be compressed to one to get a single representative spectrum for each particle. Merged particles can be split based on their classes. Particle regions can be measured by their shape and size. 

to collect, the instrument operator only needs to set up the sample and the machine automates the rest. However, once hyperspectral data are collected, traditional spectral analysis would involve manual preprocessing and spectral library similarity search at a rate of one spectrum or particle at a time. This is unattainable for hyperspectral images and timeconsuming, up to several days, for typical particle-by-particle analysis with 100 spectra per sample. Hyperspectral image analysis is very data-intensive (>1 GB per sample) and often requires several hours of computation and high-performance computers to run.[14] No manual or automated analysis procedure is perfect, and all will have biases in identification, particle counts, or sizes.[21][,][22] There is a need to create benchmarks for testing automated analysis methods to inform quantitative (accuracy and speed) improvements in this field. 

Open Specy is an extensively documented[23] open-source platform designed to facilitate microplastics’ identification and spectroscopic analysis. Open Specy v0.8.2 was first released in 2021 and primarily focused on manual spectral analysis for individual Raman and FTIR spectra. It provides researchers and scientists with comprehensive tools for managing, sharing, and interpreting spectroscopic data through an R package[24] and a Web interface (www.openspecy.org). Open Specy enables users to differentiate natural and synthetic materials 

with high accuracy and efficiency using cutting-edge analysis approaches. Since 2021, its user base has grown substantially and is one of the most widely used spectroscopy software products in the microplastic research field. While the first version of Open Specy provided a large advance, it did not have automated spectroscopy models for batch or hyperspectral image analysis. In 2023, Open Specy v1.0.0 was released with this support, and the underlying scientific advancements are presented here. 

Open Specy is currently used by one of the few Environmental Lab Accreditation Program accredited microplastics laboratories in the world (Moore Institute for Plastic Pollution Research) and is part of their accredited workflow. An automated method is necessary for accredited laboratories to scale and decrease costs while providing data to meet the increasing demand from clients to analyze microplastic samples. The Environmental Lab Accreditation Program has recovery limits (50−150% and CV <40%) that all methods must meet to be accredited.[25] These limits apply to the count recovery from spiked samples, where a known number of microplastic particles are added to samples. Furthering this objective, the authors aimed to develop an automated method that could reach the recovery limits for particle count, material type, and particle size simultaneously. 

**17346** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

In this work, we advance automated spectral analysis for microplastic research, milestones of which have already been published in field research.[26][−][28] We describe the major updates in Open Specy v1.0, the theories behind them, knowledge gaps, and known limitations. We create a new benchmark hyperspectral image data set and use it to validate the Open Specy v1.0 automated analysis procedure within accredited recovery limits. Hyperspectral smoothing, particle identification, and particle compression techniques have not been previously explored for microplastic research nor have the medoid or multinomial logistic regression models. Lastly, we compare these updates to other automated analysis software and discuss future work needed to advance automated spectroscopy. 

## ■ **[METHODS]** 

**Theory.** Since varying spectral measurement or automation parameters can result in different conclusions, the microplastic research field is cautiously optimistic about automated methods.[29] For example, Moses et al.[21] and Corradini et al.[30] separately found that automated analysis models could result in orders of magnitude of differences in particle counts and polymer distributions depending on the automation parameters. However, automated methods are highly reproducible (5% CV) across devices when sample preparation and automation parameters have been standardized.[31] 

Automated analysis begins by aligning unknown spectra to the known reference model that will be used to identify it by material type (e.g., polymeric, organic, inorganic/mineral)[20][,][32] (Table S1). For example, if using a first derivative transformed spectral library for spectral identification, then collected spectra must undergo the same transformation before being assessed for similarity. If the spectral ranges of the unknown and known spectra do not match, one should insert the mean intensity values to replace the missing data. This artificial lengthening of the spectra is necessary to assess confidence in identifications because the mean value will weigh down the scaled and centered confidence metrics (e.g., correlation coefficient), giving preference to identifications with greater amounts of observed information. Traditional spectral library search is a “machine learning” algorithm, typically using a _k_ -nearest neighbors algorithm with a Pearson correlation coefficient as the similarity metric. The number ( _k_ ) of top similar matches to assess for identification is a critical parameter, often set to 1 (the most similar match). If _k_ exceeds 1, the top matches and/ or their weights must be compiled to determine the identity (Table S3: _K_ Weighting). A match threshold is used (or set to the minimum) to differentiate known from unknown identifications and reduce false positives. Match thresholds should be empirically decided.[27] Any identifications below the match threshold must be relabeled (commonly as “unknown”)[33] (Table S3: Label Unknown), or removed (Table S3: Remove Unknown), which indicates that they need additional lines of evidence (e.g., Visual, Raman, PyGCMS) to determine the material identity. 

Batch analysis allows for simultaneous analysis of many spectra and can be applied to hyperspectral images or compilations of point-and-shoot measurements. When hyperspectral images are the subject of batch analysis, researchers typically want to derive information about the particles’ count, size, morphology, and polymer types (Figure 1). A series of spatial analysis techniques, such as smoothing, identification, particle compression, splitting, and sizing, can be used to 

generate this information. Smoothing averages spectra in each pixel using spectra in adjacent pixels. Identification uses spectral statistics (e.g., mean intensity or standard deviation) to infer which pixels belong to the background and which belong to the particles (Figures 1 and S1) and can either precede[13] or follow spectral identification.[14] The benefit of identifying particle locations before spectral identification is that it reduces the number of spectra requiring identification (the most computationally demanding step) to only pixels within particle boundaries.[13] Additionally, particle spectra can be compressed to one spectrum per particle by averaging intensity values for each particle’s spectra, reducing the computational burden required to identify and process to just the number of particles instead of the number of spectra. There is an inherent assumption with hyperspectral analysis that adjoining pixels of the same particle-classified regions are of the same particle (Figure S1). In many cases, regions identified as particles are several particles that are touching each other (particle 4 in Figure S1). These regions can be split by identifying each pixel in the particle and reattributing particle identities to isolated regions with unique material types unless the material type of the particles is identical.[14] Lastly, identified particles can be given a unique identifier and characterized by shape and size using standard image analysis techniques, such as calculations made from the convex hull (points at the edge of the particle) (Figure 1). 

**Open Specy Development.** _Database Development._ Open Specy v1.0 includes an expanded open-access library from the previously published version (11 databases and 5,416 spectra). The updated library now contains 34 databases and over 40,000 spectra (∼20,000 for FTIR and Raman). In this round of database development, we collated a spectral data set by extracting data from a diverse array of plastic, nonplastic, virgin, and environmental spectra from peer-reviewed studies, online open data repositories, and personal communication from Open Specy community members (including Horiba, Thermo Fisher Scientific, Jennifer Lynch, Dora Mehn, Claudia Cella, Aline Carvalho, and National Renewable Energy Laboratory).[9][,][27][,][33][−][52] Data were combined into a single format by conducting intensity unit conversions to make all spectra in absorbance units and linear interpolation to ensure the same 6 wavenumber resolution, which was shown to be ideal for FTIR identification.[53] Metadata from all libraries were extracted and normalized, resulting in 140 unique metadata fields. This data set will be referred to as the “raw” data set and serves as the basis for all subsequent classes and transformed data sets. 

_Harmonizing Microplastic-Relevant Classes._ Researchers often have unique naming conventions for material classes. Unstandardized categories can cause classification errors in machine learning and should be set to what spectroscopy can confidently differentiate[54] which may not be identical to standard material classifications like CAS numbers. We merged all 11,000 unique unstandardized material descriptors to a standardized system of 34 unique classes, similar to Primpke et al.[37] (Table S1). A significant distinction between this classification system and Primpke et al.[37] is that we lumped all organic and mineral material types. This is convenient because the presence of organics and minerals can be reduced by digestion[55] or density separation,[56] respectively. Therefore, quickly identifying their abundances in extracted samples can be useful. 

_Derivative Data Set._ Next, we processed the raw data set to develop an identification and modeling ready data set. The 

**17347** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

derivative library was created by taking the first derivative using the Savitzky and Golay[57] filter (90 wavenumber window) and its absolute value. This approach amplifies the importance of sharp peaks (likely signal) and minimizes the importance of small peaks (likely baseline). It also performs a moderate smoothing to the spectra (which reduces noise) and makes spectra appear similar to absorbance spectra with peaks pointing upward to aid in visual inspection. The CO2 region from 2200 to 2420 cm[−][1] was removed from further analysis because it was inconsistent and can confound identification due to its strong signal. Automated reclassification of any vague descriptors (e.g., other plastic or nonplastic material) was done by running a correlation-based _k_ -nearest neighbors to find the most similar nonvague spectrum and reassigning the class to that. Outliers and poor quality spectra were identified using _k_ - nearest neighbors to determine the most similar other spectrum in the data set. If the material class of the nearest neighbor disagreed about the class of the material, the spectrum was removed from the data set. This library was used as the basis for the training data in developing the K medoid and Logistic Regression models described below. _K Medoid._ The derivative data set is quite large (>40,000 spectra) and it is likely that some of the spectra are redundant, do not provide additional information, and slow down the computation time of the analysis without improving accuracy. Spectrum representatives for each class of spectra within the derivative data set were identified using a spectral implementation of K medoid cluster analysis.[58] The algorithm identified data points (spectra) that reduce the average distance from other data points in the same category to identify reliable representatives for each group. The distance metric in the K medoids algorithm can be any metric; here, we used the inverse of Pearson correlation, i.e., 1-correlation. For each material-class-organization-spectrum type (e.g., MineralRUFF-Raman, Polyolefins-Thermo-FTIR) combination, we created a distance matrix by correlating all spectra in the group. Next, the PAM K medoid algorithm in the cluster library[59] was used to identify up to 50 spectra that best represented the group. The end result removed redundant spectra and outliers and reduced the size of very large data sets but maintained any classes smaller than 50 spectra. The result reduced the full derivative data set by 90% to just the spectra identified by the K medoids search to 4,000 spectra (2,000 for FTIR and Raman each). Since correlation based search operates on generating arrays of the size of the reference library times size of the experimental data set, this reduction could theoretically lead to exponential increases in speed and memory efficiency. Using the medoid library to identify the original derivative data set resulted in 96% identification accuracy, demonstrating high goodness of fit to the full data set. We tested this in the benchmark analysis as Medoid (Table S3). 

_Logistic Regression._ We created a multinomial logistic regression for material identification using the glmnet package.[60] The K medoid library was used to train the regression because it more evenly weighted the material classes than the derivative library. Each wavenumber was attributed to a variable in the model. We fitted the multinomial without a _y_ - intercept (for easy interpretation of model weights), standardized the variables, weighed the classes based on their frequency in the training data set, and allowed for variable deletion through ridge regression. An alpha weight of 0.1 was used for the ridge regression because spectral intensities are 

highly correlated, and it ensured fewer variables would be removed. Models were trained for the full FTIR and Raman data set and individual models on Raman and FTIR separately, which performed better. The FTIR model fitness to the classes in the full FTIR derivative data set was 96%. We tested this in the benchmark analysis as Model (Table S3). 

_Hyperspectral Smoothing._ Hyperspectral smoothing can confer a truer signal at each location by incorporating spectra from nearby locations.[61] Any unevenness of a sample surface will generate noise due to differences in the focus on the particles and the reflective surface,[62] which we theorized could be corrected with hyperspectral smoothing. We used a Gaussian smoothing algorithm from the mmand package,[61] where the smoothing parameter (sigma) was the standard deviation of the smoothing window to weigh the neighboring cell spectra on the result. We tested variation in the impact of the sigma parameter by varying it to 0.5, 1, and 2 (Table S3). 

_Particle Identification._ We predicted that we could identify the particle locations in hyperspectral images using thresholding of spectral statistics. The ideal absorption law states that particle thickness will correlate to the absorbance intensity of the particle spectra, with larger particles having higher absorbance intensity in general.[62] Hyperspectral pixels of particles should have a larger mean absorbance intensity than the background reflective material. Although deviations from the ideal absorption are significant for real signals and high absorbance can happen without particles during hyperspectral imaging,[62] these high-absorbance signals typically produce flat lines with a low standard deviation because they are flat. However, high noise signals can also have a high standard deviation with a lower absorbance than particle spectra. We expected that the absorbance standard deviation, mean, or a combination of the two would produce a reliable metric that could be used to differentiate particles from the background. To combine the mean and standard deviation metrics, we multiplied them by each other, which has the effect of squaring the influence of the mean and adding the influence of variability, as the mean is also used to calculate the standard deviation (Figure S2). We tested the impact of the metric and threshold values on quantified particle recoveries. 

_Compressing._ After identifying particle locations, each particle can have many spectra attributed to it (e.g., particle 2 in Figure S1 would have >6 spectra). This presents an important question: which spectrum should one choose to identify the particle material type? If every spectrum is identified for the particle, false material identification can happen, especially near the edges of particles, where mixtures of background and particle spectra are present, creating severe distortions. Absorbance saturation may occur near the center of the particle, which causes poor identification accuracy, especially for very large particles. Even points between the center and the edge may not be in good focus due to their surface geometry (e.g., they are angled facing away from the detector). We hypothesized that averaging all the spectra for each particle to a single spectrum (Figure 1) could produce a representative spectrum that was accurately identifiable for that particle. Additionally, we hypothesized that this would improve computational time by reducing the number of correlations to check (the most computationally expensive step) to the number of particles instead of the number of spectra and increase accuracy by avoiding spurious false pixel identifications due to poor signal. We tested the Mean, Median, and Geometric Mean for their ability to compress particle spectra 

**17348** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

accurately (Table S3). Alternatively, all spectra could be identified individually, and their identities could be pooled to determine a single identity (Table S3: Particle Cell Vote). 

_Splitting._ Particle compression has a side effect in that any touching particles are merged into a single particle (e.g., particle 4 in Figure S1). To remedy this issue, Primpke et al.[14] developed a strategy to differentiate touching particles by material type, identifying all pixels, and then used a 4-by-4 closing to fill in gaps. We tested this strategy by incorporating it into the new Open Specy algorithm and compared it to other techniques (Table S3: All Cell Particle ID). 

_R Package and Web GUI Development._ We integrated the new functionality described in this manuscript into the Open Specy R package and the Web application hosted at www. openspecy.org (Figure S3). The application is fully documented with video and text tutorials on the About page and a reference manual.[63] The Web application can batch-process thousands of spectra (individual or hyperspectral images) but will run at a slower rate than the R package because it has the overhead of producing user interface elements. Individual spectra are projected onto a heatmap by generating _x_ − _y_ coordinates for each spectrum. This allows the user to interpret the outcome of many spectra quickly, even when they are not spatially referenced. On the Web application, preprocessing and identification settings are applied to all uploaded spectra simultaneously, allowing for consistent analysis workflows that are highly interpretable and reproducible. The site has been recoded with a Web Assembly framework so that it can scale serverlessly, providing near-native speed for Web site users but keeping costs low for hosting the Web application, and it can work better in low Internet settings, improving accessibility. 

_Benchmark Testing._ Speed and accuracy benchmarking are critical steps in assessing the validity and usability of any automated spectral analysis approach. Microplastic researchers are known for sharing their spectral reference data,[64] which have been used to develop spectral identification models.[65] We add to this growing resource by sharing new benchmark data sets of heavily curated hyperspectral FTIR images of microplastics and natural microparticles. We use these benchmarks to validate and calibrate Open Specy v1.0.0 for microplastic identification and quantification. 

The benchmark data set was created by spreading a homogeneous mixture of particles from one material at a time on a 316L stainless filter screen 5 _μ_ m rating with a reverse Dutch weave from ARTESIAN SYSTEMS L.L.C. The stainless steel filters provide a cheaper alternative to gold-coated polycarbonate or silicone filters at less than $1 per filter compared to >$10 per filter and have a higher flow rate.[66] The Dutch weave was chosen because it traps particles at the surface instead of in the filter matrix and has a relatively flat surface compared with other weaves. Other background surfaces have been tested with this algorithm (results not reported), and they perform similarly or better because they have higher contrast due to less noise from the surface roughness of the steel mesh. The steel mesh filter was flattened and attached to a glass microscope slide by applying doublesided sticky tape to the slide. Then, the back of the steel mesh was pressed against the tape with tweezers and gentle pressure was applied across the filter to ensure a secure attachment. Hyperspectral images were created with a Thermo Fisher iN10 MX using an MCT 8 × 2 array detector (liquid-nitrogencooled) with a 25 _μ_ m step size in reflection mode, a spectral resolution of 16 cm[−][1] (from 4000 to 715 cm[−][1] ), and one scan 

every 0.113 s. The data was exported to ENVI format in OMNIC Picta for processing in Open Specy. 

Both plastic and nonplastic materials were used to test the possibility of false positives and negatives (Table S2). None of the spectra used in the benchmark data set were used in developing the Open Specy database, as that would result in biased overly high accuracy values. Particle counts, median projected area, and median length were manually measured in FIJI[67] using corresponding visual images taken immediately before the FTIR hyperspectral image on the iN10 MX. Particle classes were attributed to two groups: “Specific ID”, which denoted the most specific material type we could attribute to the material, and “Plastic/Not ID”, which was used to differentiate plastic materials from nonplastic materials. We incorporated particle properties at the edge of theoretical capabilities to put this algorithm to rigorous test. Median particle lengths ranged from 77 to 1542 _μ_ m, the smaller of which is near the theoretical limits of the iN10s hyperspectral imager, as particles with 50 _μ_ m are the smallest that the 25 _μ_ m pixel size can accurately interpret because they are approaching the size of the pixel and thus have poor signal (e.g., particles 1 and 3 in Figure S1). Additionally, particles thicker than 1 mm exhibit very high absorption, making identification challenging in reflectance mode.[9] We were unable to calculate the particle size or counts of two hyperspectral images (Red PET Fibers and Cotton Polyester Blend) because the particles were fibers and were too thin to see in the visual images. As a result, we only used material identifications to calculate recoveries. Fine fibers often have a diameter close to 25 _μ_ m, are difficult to focus due to their irregular geometry, and are not wellcharacterized by this approach. We replicated hyperspectral images of 5 materials (BlueSphere 600−710 _μ_ m, Loofah Sponge, Silky Terrier Hair, Soil, and Roto-Mold Dust) to assess replication variability on the same material. A plastic material for which we have not yet determined an identification (Unknown Plastic) was also added. 

We tested the effect of the smoothing parameter and thresholding techniques on particle characterization by count, area, and length. We varied the thresholding cutoff for mean intensity, standard deviation, and mean intensity times the standard deviation from 0.0001 to 10, which we found to be the typical value limits in the benchmark data sets. We tested using a hyperspectral smoothing standard deviation parameter set to 1 and compared it to that of no smoothing. 

Fifteen automated spectroscopy models were tested in the Open Specy R package to assess the impact of hyperspectral smoothing, particle identification, particle compressing, particle splitting, and spectral identification (Table S3). All analyses included preprocessing of spectra using the absolute first derivative transformation with a 90 wavenumber window, min−max normalization, and a wavenumber resolution of 6 cm[−][1] (identical to the training data). A minimum area threshold of >1 pixel (i.e., >50 × 25 _μ_ m particle) was used for all tests so that no single-pixel particles would be identified (e.g., particle 3 in Figure S1). All models included the mean intensity times standard deviation as the particle identification metric (Figure S2). 

Five metrics were tested to assess the accuracy of the models. Particle Count accuracy was calculated as the ratio between the visual particle count in the sample and the particle count determined by the model. Plastic/Not ID and Specific ID accuracy were determined by the percentage of correct identifications from the sample. Particle Length and Particle 

**17349** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

Article 

**==> picture [56 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
pubs.acs.org/ac<br>**----- End of picture text -----**<br>


**==> picture [309 x 193] intentionally omitted <==**

Figure 2. Identifying ideal thresholds and metrics to use for particle identification in hyperspectral images. The _x_ axis is the threshold used in log base 10 units. The _y_ axis denotes if all recovery rates and bootstrapped confidence intervals fell between the accredited standard 50−150% (TRUE). The top axis shows the thresholding metric used and the right axis indicates whether smoothing with a sigma of 1 was used or not. Only metrics with smoothing were able to produce accredited levels of recovery and the mean times standard deviation had the widest region of values with acceptable recoveries. A more detailed version of this analysis is in Figure S4. 

Figure 3. This spiderweb plot shows the deviation between the model and the observations in absolute log 2 relativized space. Models that perform well are clustered toward the center and not labeled, while outliers of poorly performing models are clearly visible and labeled with their names. 

Area accuracy were determined as the ratio between the median particle projected area or length and the visually derived median from FIJI. To derive metrics for the accuracies and variance of the model, we calculated the mean of each accuracy metric across all 22 hyperspectral images (2,880 particles in total) and their 95% confidence intervals using bootstrapping ( _n_ = 1,000, resampling with replacement). The best-fit model was assessed by combining all 5 accuracy values for each model and comparing their means and confidence intervals and determining whether the aggregate recovery fell within the accredited limits (50−150% and CV <40%). Benchmarks were tested using an operating system (Windows 11 Home 64-bit) on a computer with 16 cores (AMD), 64 GB RAM, 4095MB GPU (NVIDIA GeForce RTX 3070 Laptop Dell), 2TB SSD (Western Digital WD Green SN350), and a motherboard (Alienware 06W7NY FP6). This computer ran 

the data analysis but did not control the instrument that collected the data. 

## ■ **[RESULTS][AND][DISCUSSION]** 

**Hyperspectral Smoothing and Thresholding.** The results from the test images (Table S2) were assessed to determine the role of hyperspectral smoothing and thresholding on recovery. We tested the threshold metrics, including mean absorbance, standard deviation, and the mean times of the standard deviation, while comparing smoothing (sigma = 1) and no smoothing to identify reasonable parameters to use for particle identification (Figure 2). Outcomes for particle length and area accuracy had similar trends because the two were correlated (Figure S4). The standard deviation and mean had narrower ranges of values than mean times standard deviation that could be used to identify particles in the sample within accredited limits (Figure 2). In all cases, no smoothing 

**17350** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

**==> picture [370 x 78] intentionally omitted <==**

Figure 4. Result of the Base model for predicting the 75−90 _μ_ m polyethylene red beads (red beads 75−90 _μ_ m) hyperspectral image illustrating − each process (A E) involved in the automated pipeline for analyzing hyperspectral images. (A) shows the visual image that is collected before the hyperspectral image. Red spherical beads are seen atop a stainless steel mesh filter. (B) shows the hyperspectral heatmap for the signal times noise values calculated from the hyperspectral image; particles are the bright regions. (C) shows the regions identified as particles by thresholding the signal times noise heatmap. Particle regions are in black and background regions are in white. (D) Individual particles are shown with unique IDs; their color corresponds to their material identity. A few particles are not identified as the same material (blue and purple) even though all particles are the same. (E) An overlay of A and D shows generally good correspondence between the visual image and the regions identified as particles. The thresholding routine did not identify a few particles on the right-hand side, which can be seen as light pink. 

was unable to produce recoveries within the accredited limits. A threshold of around 0.1 would be ideal if mean intensity or standard deviation were used. A smoothing value of 1 and a threshold of 0.01 for mean times standard deviation were determined to have the best recovery. The trend was flatter, had lower variability, and stayed near 100% recovery for longer than the other metrics. Ideal thresholds are likely to vary by instrument, settings, sample preparation, and data preprocessing, and we anticipate that each lab will need to calibrate the threshold to get the highest accuracy for their analysis. Calibration can be performed using a similar batch recovery experiment or approximated in 20 min by using a single hyperspectral image with a diversity of particle sizes and types, comparing a visual image to the threshold hyperspectral image (Figure S3). We used this test as the rationale for the Base model (Table S3), which used 0.01 with mean times standard deviation for the particle identification threshold and a smoothing parameter of 1 and tested factor 2 shifts (Smoothing 0.5, Smoothing 2, Threshold 0.005, and Threshold 0.02) and removed smoothing (No Smoothing) from these proposed parameters. 

**Benchmark Results.** _Accuracy._ Eight of 15 models performed within the accredited recovery limits (50−150% recovery and CV <40%) based on aggregation of all recovery values. While all models had aggregate recoveries between 85 and 100%, the other models were unable to make the CV <40% limit, underscoring the importance of variability assessment in modeling studies. Strong outliers were produced by the All Cell Particle ID, No Smoothing, Smoothing 0.5, and Smoothing 2 algorithms (Figures 3 and S5). The All Cell ID algorithm segregated particles based on the material IDs of the pixels within each particle and was the least accurate for these benchmark tests. When the materials of particles are all the same and the particles are relatively well dispersed (as was the case here), this algorithm can produce artifacts that increase particle counts and decrease particle sizes. The logistic Model (91%, CI95 82−96) and Medoid (89%, CI95 78−96) algorithms performed statistically similar to the full derivative library (91%, CI95 81−97) in identifying the specific material type suggesting using the full library search, which is slower, is not required for accurate identification. Removing the smoothing parameter (No Smoothing) resulted in poor outcomes for particle counts (189% compared to 89% with smoothing), area (33% compared to 109%), and specific identification (77% compared to 91%). Increasing the smoothing parameter resulted in an overestimation of the 

particle area, while decreasing it led to an underestimation. The Particle Cell Vote algorithm performed similarly in Specific ID recovery (92%, CI95 82−98) to the compressed particle identification (Base) (91%, CI95 81−97), suggesting that aggregating individual identities of pixels for the particles does not outperform the identification of just the average spectrum from all pixels. The _K_ Weighting algorithm with _k_ = 10 also did not improve the Specific ID (89%, CI95 80−96) from the Base, suggesting that a _K_ nearest neighbors with _k_ = 1 algorithm is appropriate for automated analysis. Labeling unknown particles decreased the Specific ID identification − accuracies (76%, CI95 63 88) because particles were relabeled as unknown instead of a possible match, which was counted against them in the accuracy metric. Removing unknown − particles decreased Particle Count accuracy (69%, CI95 54 88) because particles were removed from the data set but had a similar Specific ID accuracy (93%, CI95 83−98) to the Base model. No matter what match threshold is used, practitioners should report the counts and identities of all known and unknown particles in their samples and the threshold used so that readers can assess the study result. As expected, increasing the threshold value by a factor of 2 (Threshold 0.02) underestimated the particle count by a small amount and decreasing the threshold (Threshold 0.005) had the opposite effect. Mean, geometric mean, and median compressing algorithms all had statistically similar recoveries, so any of those options are viable. Specific ID accuracy was typically ∼1−2% lower than Plastic/Not ID accuracy. Future developments should reclassify those spectra. Accuracy was not dependent on the material type or median particle size in the samples (Figures S6 and S7). An example of the Base model is represented in Figure 4, showcasing its performance and the outputs from Open Specy for exemplary hyperspectral images. 

The models that met the accredited criteria (50−150% recovery and CV < 40%) were Base, Particle Cell Vote, Mean, Geometric Mean, Medoid, Model, Threshold 0.02, and _K_ Weighting. The best-fit model with the lowest CV was the Threshold 0.02 analysis routine reaching those limits for length (recovery: 94% CV: 33%), area (recovery: 91% CV: 47%), specific ID (recovery: 90% CV: 24%), plastic/not ID (recovery: 92% CV: 23%), and count (recovery: 86% CV: 34%). When applying these models and parameters to new studies, all parameters should be carefully tuned for best results, especially if using different instruments, sample preparation, and imaging parameters than described here. Of the accurate models tested here, we recommend that future 

**17351** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

work use the computationally cheaper options (i.e., not Particle Cell Vote) (Figure S8). 

_Speed._ The speed of data processing is an important aspect for laboratory users because early implementations of these algorithms required many hours per sample for the computer to process.[14] The speed of the data analysis was primarily controlled by whether the particle spectra were compressed. When compression was used, hyperspectral images took less than a third of the time (3 min) to analyze compared to the spectra analyzed without compression (17 min) (Figure S8). We anticipated the All Cell ID and Particle Cell Vote algorithms to be more computationally expensive because they identify every pixel related to each particle. The computer used in this test was a high-performance system (described in the methods), but we have also observed similar (∼2×) run times on standard-performance personal computers for the same data set size. The Model and Medoid approaches did not significantly improve speed, even though they are theoretically more efficient for the material identification step than using the full library. A slow part of the analysis that persists is reading the large data sets into memory (several minutes). Future efforts should aim to find quicker solutions for reading ENVI files (the common file format for hyperspectral images) into memory.[30] Compared to manually exploring a hyperspectral image or doing manual particle-by-particle spectral collection, the time savings of employing automated analysis are on the order of days to weeks per sample (assuming accuracy >90%, and QA/QC and correction time <10 min). 

_Comparison to Existing Software._ We assessed other commonly used spectral identification software for features comparable to those of these updates: hyperspectral smoothing, particle identification, particle spectra compressing, particle sizing, and open source. We assessed siMPle,[68] Microplastics Finder,[13] Particle Finder,[69] KnowitAll,[70] OMNIC,[71] and OPUS.[72] Outside of Open Specy, none of the other software had open-source code, limiting their extensibility and interpretability for the user and their longterm scalability. Particle Finder, KnowItAll, OMNIC, and OPUS had onboard spectral averaging algorithms that could do particle spectra compressing manually, but none had the automated process presented here. No other software had the hyperspectral smoothing procedure as presented here. Microplastics Finder has a technique similar to particle identification, using an undescribed “statistical technique” to identify where particles are in the hyperspectral image and reduce image processing time. siMPle and Microplastics Finder have processes for characterizing the size and shape of particles, but to the best of our knowledge, these have not yet been tested against an independently evaluated benchmark. Particle Finder and OMNIC can characterize particle shapes and sizes from visual images and use those locations to collect single spectra for each particle but cannot do so from the hyperspectral image information alone. 

_Limitations._ Not all materials colloquially classified as distinct can be easily differentiated in FTIR spectroscopy due to the similarity of their true signals and artifacts from instrumentation and sample preparation. For example, polyacrylates and organic matter are often confounded due to their similarity in signals,[73] mineral-doped plastic can generate false negatives because the mineral signal[74] has very strong peaks, and tire wear particles have high FTIR absorbance from carbon black, which results in poor signalto-noise.[75] Polymer composites can challenge identification 

systems because they are currently poorly supported in reference libraries and will have unique signatures. Instruments used and the spectral collection mode can yield drastically different signals for the same materials. To be as accurate as possible, reference libraries must be made to represent the range of expected spectra for the instrument being used.[9] Environmental chemistry is complex; false positives or negatives can occur due to natural chemistries similar to plastic, like plant cuticles, biofilms, surface oxidation, or fatty acid residues.[27][,][73] The best practices to overcome these issues are to constantly review match outputs, improve reference libraries, and use a hit quality threshold to reduce false positives by relabeling identities below a certain threshold as unknown without setting it too high where false negatives are amplified.[27] 

Sample preparation is challenging for high-quality hyperspectral images. While the ideal scenario for hyperspectral image processing is for particles not to touch, this is difficult to achieve in practice (Figure 5). There is no way to perfectly 

**==> picture [239 x 240] intentionally omitted <==**

Figure 5. Image shows several issues simultaneously. Touching particles are being merged into a single particle. Particles have moved between the time the visual image was taken and the hyperspectral image appearing as an offset. False particles are being produced at the edge of particles because this hyperspectral image was not smoothed. 

separate all touching particles before data collection automatically, but keeping the particle total area low relative to the filter area makes particle touching less likely.[76] Complex environmental media can create bio, chemical, and mineral films that are extremely difficult to remove from the sample and will impact the identification results of the spectra.[27] Spurious particles may be identified as artifacts near the fringes of real particles (Figure 5). In general, the edges of particles typically have lower-quality spectra because they may not take up the full pixel, are not oriented flat facing the detector, or are too thin to provide enough signal to interpret. Future work should improve edge detection and spectral processing strategies. Smoothing can sometimes correct this issue. Large (>500 _μ_ m) spherical particles can shift between visual and FTIR imaging, making their positions difficult to relate (Figure 5). Particle 

**17352** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

size should be constrained to a range where automated analysis results in high-accuracy output. Particles too small (<50 _μ_ m in this study) will produce a weak signal, and particles too large (>500 _μ_ m in this study) are too strongly absorbing. Other instruments and settings may have different optimal particle sizes. Tape can be used to secure filters onto slides for reflectance hyperspectral imaging. If the tape is present in the hyperspectral image (e.g., the image area expands beyond the filter onto a taped edge), it could be falsely identified as a plastic particle and must be removed in post-data processing. Frequently reviewing the output of hyperspectral images for these common artifacts is a critical step for quality control. Future work should standardize sample preparation strategies. 

Background material and form can impact the quality of the hyperspectral image. When using any porous background surface, the size of the holes must be much smaller than the step size of the hyperspectral image or the holes in the mesh will create much noise and other signal artifacts depending on their shape and what is below them. For example, Figure S9 has repeating units being identified as particles due to a 20 _μ_ m mesh size and a 25 _μ_ m step size. In contrast, we found that a step size of 25 _μ_ m on a steel mesh with 5 _μ_ m holes produced acceptable results. Hyperspectral images need to be in focus to collect spectra accurately. For infrared hyperspectral imaging, the practitioner should focus on the surface of the reflective (transreflectance signal) or transparent (transmission signal) background, not the top of the largest particles, because that would lead to smaller particles being out of focus. In Figure S9, regions near the top and in the bottom right corner are blank, while this image should have repeating grid lines across it; these blank spots could be due to incorrect focus from the mesh not being completely flat. If a visible image corresponds to the hyperspectral image, issues with the focus can typically be seen in the visual image and correspond to the signal−noise heatmap of the hyperspectral image and the extracted particle image. No matter what filter or background surface is chosen, care should be taken to optimize the parameters proposed here for any deviations from the instrument and sample preparation described here. 

Even after sample extraction, sometimes a sample cannot fit within a single hyperspectral image because there are countless particles and filters should not be overcrowded. One option is to aliquot the samples, but recent research has shown this strategy to increase uncertainty.[77] In these cases, the ability to accurately extract microplastics from samples must be improved, but until then, these samples must be qualified as extrapolated. We recommend performing at least 3 aliquots per sample so that statistical variability can be assessed for any extrapolated values.[78] As long as more than 100 plastic particles are present within the total aliquot, it will be statistically representative of material types and particle abundances in the sample.[11] 

## ■ **[CONCLUSION]** 

Automated spectroscopy has the potential to become a standard procedure, as accredited microplastic laboratories already utilize it. We have presented major advancements in the speed and accuracy of automated hyperspectral analysis, which function effectively on a benchmark data set of diverse particle sizes, shapes, and materials. However, there is a risk that automated spectroscopy is used as a black box. Automated analysis settings are critical to accuracy but complex to finetune for new instruments or samples. Therefore, ensuring that 

users are adept in the art of automated spectroscopy techniques is non-negotiable for producing high-quality research and advancing the field. Incorrect thresholding, spectral processing, particle splitting, and sample prep can result in highly inaccurate particle identification using automated spectroscopy. We implore the microplastics research and spectroscopy community to frequently verify automated spectroscopy models, critique their output, and improve upon them. This study presents an automated method that meets the accredited standard of 50−150% recovery with <40% coefficient of variation for the benchmark data set tested and demonstrates this can be achieved with a variety of model settings. Continued exploration on automated spectroscopy is needed to ensure the accuracy, reproducibility, and generalizability of these techniques to other sample preparations, spectral processing, and instrumentation. 

## ■ **[ASSOCIATED][CONTENT]** 

## **Data Availability Statement** 

Data and code for reproducing the analysis and techniques presented are available at 10.5281/zenodo.15686092. Open Specy is an R package hosted on CRAN: https://cran.rproject.org/web/packages/OpenSpecy/index.html. Open Specy also has a public Web site where a graphic user interface can be used to drive the code: www.openspecy.org. 

## * **sı Supporting Information** 

The Supporting Information is available free of charge at https://pubs.acs.org/doi/10.1021/acs.analchem.5c00962. 

Figures including conceptual visualization of hyperspectral imaging of particles, mean intensity and standard deviation values of all pixels from a hyperspectral image, Open Specy Web application screenshot showing a hyperspectral image and the selected spectrum below, recoveries for particle count, area, length, and sample count based on combinations of smoothing parameters and thresholding metrics, accuracy metrics for each type of processing procedure, recovery values and the material type for assessing recovery bias by material type for plastic and nonplastic materials, median particle size and recovery values for each recovery metric, mean time in minutes to complete the analysis procedure on each hyperspectral image, and thresholded hyperspectral image and tables on harmonized classes used in this study and examples of unstandardized terminology, information about the benchmark test images, and models tested for their ability for automated spectral analysis and parameters (PDF) 

## ■ **[AUTHOR][INFORMATION]** 

## **Corresponding Author** 

- Win Cowger − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States; University of California, Riverside, California 92521, United States;_ 

- orcid.org/0000-0001-9226-3104; Email: wincowger@ 

- gmail.com 

## **Authors** 

- Aleksandra Karapetrova − _University of California, Riverside, California 92521, United States_ 

**17353** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

- Clarissa Lincoln − _Renewable Resources and Enabling Sciences Center, National Renewable Energy Laboratory, Golden, Colorado 81699, United States_ 

- Ali Chamas − _Renewable Resources and Enabling Sciences Center, National Renewable Energy Laboratory, Golden, Colorado 81699, United States_ 

- Hannah Sherrod − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States;_ orcid.org/0009-0001-0497-8693 

- Nicholas Leong − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States_ 

- Katherine S. Lasdin − _University of Washington, Seattle, Washington 98114, United States_ 

- Christine Knauss − _University of Maryland Center for Environmental Science, Cambridge, Maryland 20610, United States;_ orcid.org/0000-0003-4404-8922 

- Vesna Teofilovic − _University of Novi Sad, Faculty of Technology, Novi Sad 21000, Serbia_ 

- Monica M. Arienzo − _Desert Research Institute, Reno, Nevada 9503, United States_ , 8 

- Zacharias Steinmetz − _RPTU, Landau 67663, Germany;_ orcid.org/0000-0001-6675-5033 

- Sebastian Primpke − _Division Shelf Sea System Ecology, Biologische Anstalt Helgoland, Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research, Helgoland 27498, Germany;_ orcid.org/0000-0001-7633-8524 

- Lindsay Darjany − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States_ 

- Clare Murphy-Hagan − _University of California, Riverside, California 92521, United States_ 

- Shelly Moore − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States;_ orcid.org/ 0000-0002-3313-4481 

- Charles Moore − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States_ 

- Gwen Lattin − _Moore Institute for Plastic Pollution Research, Long Beach, California 90815, United States_ 

- 

- Andrew Gray _University of California, Riverside, California 92521, United States;_ orcid.org/0000-0003-2252-7367 

- Rachel Kozloski − _Desert Research Institute, Reno, Nevada 9503, United States_ , 8; orcid.org/0000-0003-1211-9351 

- Jeremiah Bryksa − _Northern Alberta Institute of Technology (NAIT), Edmonton, Alberta T5G 2R1, Canada;_ orcid.org/0009-0001-1533-7031 

- Benjamin Maurer − _Renewable Resources and Enabling Sciences Center, National Renewable Energy Laboratory, Golden, Colorado 81699, United States_ 

Complete contact information is available at: https://pubs.acs.org/10.1021/acs.analchem.5c00962 

## **Notes** 

The authors declare no competing financial interest. 

## ■ **[ACKNOWLEDGMENTS]** 

We thank Kris and Florencia from the NREL team for assisting in curating and testing the database. W.C. was funded by the National Renewable Energy Laboratory, Walking Softer, the California Sea Grant, and the McPike Zima Charitable Foundation. This work was authored in part by the National Renewable Energy Laboratory, operated by Alliance for Sustainable Energy, LLC, for the US Department of Energy (DOE) under Contract No. DE-AC36-08GO28308. Funding 

was provided by the US Department of Energy Office of Energy Efficiency and Renewable Energy Water Power Technologies Office. A.G. was funded in part by the USDA NIFA Hatch Program [project CA-R-ENS-5120-H], USDA Multistate Project 4170 [project CA-R-ENS-5189-RR], and the UC ANR AES Mission Funding Program. The views expressed in the article do not necessarily represent the views of the DOE or the US Government. The US Government retains and the publisher, by accepting the article for publication, acknowledges that the US Government retains a nonexclusive, paid-up, irrevocable, worldwide license to publish or reproduce the published form of this work, or allow others to do so, for the US Government purposes. V.T. was funded by Ministry of Science, Technological Development and Innovation of the Republic of Serbia (451-03-66/ 2024-03/200134). 

## ■ **[REFERENCES]** 

(1) Hartmann, N. B.; Huffer, T.; Thompson, R. C.; Hassellöv, M.; Verschoor, A.; Daugaard, A. E.; Rist, S.; Karlsson, T.; Brennholt, N.; Cole, M.; Herrling, M. P.; Hess, M. C.; Ivleva, N. P.; Lusher, A. L.; Wagner, M. _Environ. Sci. Technol._ 2019, _53_ (3), 1039−1047. 

(2) Eriksen, M.; Cowger, W.; Erdle, L. M.; Coffin, S.; VillarrubiaGómez, P.; Moore, C. J.; Carpenter, E. J.; Day, R. H.; Thiel, M.; Wilcox, C. _PLoS One_ 2023, _18_ (3), No. e0281596. 

(3) Murphy-Hagan, C.; Gray, A. B.; Singh, S.; Hapich, H.; Cowger, 

W.; Seeley, M. E.; Waldschläger, K. _Environ. Res._ 2025, _269_ , 120908. 

(4) Buks, F.; Kaupenjohann, M. _Soil_ 2020, _6_ (2), 649−662. 

(5) Leonard, J.; Borthakur, A.; Koutnik, V. S.; Brar, J.; Glasman, J.; Cowger, W.; Dittrich, T. M.; Mohanty, S. K. _Atmos. Pollut. Res._ 2023, _14_ (2), 101651. 

(6) Goswami, S.; Adhikary, S.; Bhattacharya, S.; Agarwal, R.; Ganguly, A.; Nanda, S.; Rajak, P. _Life Sci._ 2024, _355_ , 122937. 

(7) Xu, J.-L.; Wright, S.; Rauert, C.; Thomas, K. V. _Nature_ 2025, _639_ (8054), 300−302. 

(8) Chamas, A.; Moon, H.; Zheng, J.; Qiu, Y.; Tabassum, T.; Jang, J. H.; Abu-Omar, M.; Scott, S. L.; Suh, S. _ACS Sustainable Chem. Eng._ 2020, _8_ (9), 3494−3511. 

(9) Cowger, W.; Roscher, L.; Jebens, H.; Chamas, A.; Maurer, B. D.; Gehrke, L.; Gerdts, G.; Primpke, S. _Anal. Bioanal. Chem._ 2024, _416_ , 1311−1320. 

(10) Kotar, S.; McNeish, R.; Murphy-Hagan, C.; Renick, V.; Lee, C.F. T.; Steele, C.; Lusher, A.; Moore, C.; Minor, E.; Schroeder, J.; et al. _Chemosphere_ 2022, _308_ , 136449. 

(11) Cowger, W.; Markley, L. A. T.; Moore, S.; Gray, A. B.; Upadhyay, K.; Koelmans, A. A. _Ecotoxicol. Environ. Saf._ 2024, _275_ , 116243. 

(12) De Frond, H.; Thornton Hampton, L.; Kotar, S.; Gesulga, K.; Matuch, C.; Lao, W.; Weisberg, S. B.; Wong, C. S.; Rochman, C. M. _Chemosphere_ 2022, _298_ , 134282. 

(13) Hufnagl, B.; Stibi, M.; Martirosyan, H.; Wilczek, U.; Möller, J. N.; Löder, M. G. J.; Laforsch, C.; Lohninger, H. _Environ. Sci. Technol. Lett._ 2022, _9_ (1), 90−95. 

(14) Primpke, S.; Lorenz, C.; Rascher-Friesenhausen, R.; Gerdts, G. _Anal. Methods_ 2017, _9_ (9), 1499−1511. 

(15) Primpke, S.; Godejohann, M.; Gerdts, G. _Environ. Sci. Technol._ 2020, _54_ (24), 15893−15903. 

(16) Wander, L.; Vianello, A.; Vollertsen, J.; Westad, F.; Braun, U.; Paul, A. _Anal. Methods_ 2020, _12_ (6), 781−791. 

(17) Vidal, C.; Pasquini, C. _Environ. Pollut._ 2021, _285_ , 117251. 

(18) Faltynkova, A.; Johnsen, G.; Wagner, M. _Microplast. Nanoplast._ 2021, _1_ (1), 13. 

(19) Meyers, N.; Catarino, A. I.; Declercq, A. M.; Brenan, A.; Devriese, L.; Vandegehuchte, M.; De Witte, B.; Janssen, C.; Everaert, G. _Sci. Total Environ._ 2022, _823_ , 153441. 

(20) Cowger, W.; Gray, A.; Christiansen, S. H.; DeFrond, H.; Deshpande, A. D.; Hemabessiere, L.; Lee, E.; Mill, L.; Munno, K.; 

**17354** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

Ossmann, B. E.; Pittroff, M.; Rochman, C.; Sarau, G.; Tarby, S.; Primpke, S. _Appl. Spectrosc._ 2020, _74_ (9), 989−1010. 

(21) Moses, S. R.; Roscher, L.; Primpke, S.; Hufnagl, B.; Löder, M. G. J.; Gerdts, G.; Laforsch, C. _Anal. Bioanal. Chem._ 2023, _415_ (15), 2975−2987. 

(22) Coates, J. In _Encyclopedia of Analytical Chemistry_ ; Meyers, R. A., Ed.; Wiley, 2000. DOI: . 

(23) Cowger, W.; Steinmetz, Z.; Gray, A.; Munno, K.; Lynch, J.; Hapich, H.; Primpke, S.; De Frond, H.; Rochman, C.; Herodotou, O. _Anal. Chem._ 2021, _93_ (21), 7543−7548. 

(24) Cowger, W.; Steinmetz, Z. _OpenSpecy: Analyze, Process, Identify, and Share, Raman and (FT)IR Spectra_ , 2021. https://github.com/ wincowgerDEV/OpenSpecy. 

(25) Wong, D. C.; Coffin, D. S. _Standard Operating Procedures for Extraction and Measurement by Infrared Spectroscopy of Microplastic Particles in Drinking Water_ , 2022. https://www.waterboards.ca.gov/ drinking_water/certlic/drinkingwater/documents/microplastics/swbmp1-rev1.pdf. 

(26) Karapetrova, A.; Cowger, W.; Michell, A.; Braun, A.; Bair, E.; Gray, A.; Gan, J. _J. Hazard. Mater._ 2024, _480_ , 136126. 

(27) Kozloski, R.; Cowger, W.; Arienzo, M. M. _Microplast. Nanoplast._ 2024, _4_ (1), 27. 

(28) Tiwari, E.; Sistla, S. _PNAS Nexus_ 2024, _3_ (10), pgae433. 

(29) Hufnagl, B.; Steiner, D.; Renner, E.; Löder, M. G. J.; Laforsch, 

C.; Lohninger, H. A. _Anal. Methods_ 2019, _11_ , 2277. 

- (30) Corradini, F.; Beriot, N.; Huerta-Lwanga, E.; Geissen, V. 

- _SoftwareX_ 2021, _16_ , 100857. 

- (31) Lenz, R.; Enders, K.; Vizsolyi, E. C.; Schumacher, M.; Lötsch, 

- J.; Löder, M. G. J.; Eder, G.; Voronko, Y.; Andrade-Garda, J. M.; Muniategui-Lorenzo, S.; Laforsch, C.; Fischer, D.; Labrenz, M. _Environ. Sci. Technol._ 2024, _58_ (50), 22224−22234. 

- (32) Primpke, S.; Cross, R. K.; Mintenig, S. M.; Simon, M.; Vianello, 

- A.; Gerdts, G.; Vollertsen, J. _Appl. Spectrosc._ 2020, _74_ , 1127−1138. 

- (33) Chabuka, B. K.; Kalivas, J. H. _Appl. Spectrosc._ 2020, _74_ (9), 

- 1167−1183. 

- (34) El Mendili, Y.; Vaitkus, A.; Merkys, A.; Grazulis, S.; Chateigner, 

- D.; Mathevet, F.; Gascoin, S.; Petit, S.; Bardeau, J.-F.; Zanatta, M.; Secchi, M.; Mariotto, G.; Kumar, A.; Cassetta, M.; Lutterotti, L.; Borovin, E.; Orberger, B.; Simon, P.; Hehlen, B.; Le Guen, M. _J. Appl. Crystallogr._ 2019, _52_ (3), 618−625. 

(35) Lafuente, B.; Downs, R.; Yang, H.; Stone, N. The Power of Databases: The RRUFF Project. In _Highlights in Mineralogical Crystallography_ ; Armbruster, T., Danisi, R. M., Eds.; De Gruyter: Berlin, Germany, 2015; Vol. _1_ , p 30. 

(36) Munno, K.; De Frond, H.; O’Donnell, B.; Rochman, C. M. _Anal. Chem._ 2020, _92_ , 2443−2451. 

(37) Primpke, S.; Wirth, M.; Lorenz, C.; Gerdts, G. _Anal. Bioanal. Chem._ 2018, _410_ , 5131−5141. 

(38) De Frond, H.; Rubinovitz, R.; Rochman, C. M. _Anal. Chem._ 2021, _93_ (48), 15878−15885. 

(39) Miller, E. A.; Yamahara, K. M.; French, C.; Spingarn, N.; Birch, 

J. M.; Van Houtan, K. S. _Sci. Data_ 2022, _9_ (1), 780. 

(40) Davidson, J.; Arienzo, M. M.; Harrold, Z.; West, C.; Bandala, E. 

R.; Easler, S.; Senft, K. _Appl. Spectrosc._ 2023, _77_ (11), 1240−1252. 

(41) Roscher, L.; Fehres, A.; Reisel, L.; Halbach, M.; ScholzBöttcher, B.; Gerriets, M.; Badewien, T. H.; Shiravani, G.; Wurpts, A.; Primpke, S.; Gerdts, G. _Abundances of Large Microplastics (L-MP, 500_ − _5000_ Μ _m) in Surface Waters of the Weser Estuary and the German North Sea (April 2018)_ , 2021, 414 data points. DOI: . 

- (42) Lenz, R.; Fischer, F.; Arnold, M.; Fernández-González, V.; 

- Moscoso Pérez, C. M.; Andrade-Garda, J. M.; Muniategui-Lorenzo, 

S.; Fischer, D. _Robna/MPX_specDB: Microplastix SpecDB_ , 2023; .. 

- (43) Infrared Spectra Library The Helen and Martin Kimmel 

- Center. https://centers.weizmann.ac.il/kimmel-arch/infrared-spectralibrary (accessed 01 27, 2025). 

(44) Cultural Heritage Science Open Source. Cultural Heritage Science Open Source. https://chsopensource.org/(accessed 01 27, 2025).. 

(45) _Data sets_ . Chemometrics Research. https://ucphchemometrics. com/datasets/(accessed 01 27, 2025). 

(46) Berzins, K.; Sales, R. E.; Barnsley, J. E.; Walker, G.; FraserMiller, S. J.; Gordon, K. C. _Vib. Spectrosc._ 2020, _107_ , 103021. 

(47) Menges, F. Spectragryph - optical spectroscopy software. Spectroscopy. http://spectragryph.com/(accessed 01 27, 2025). 

(48) SWGDRUG Infrared Library. https://swgdrug.org/ir.htm (accessed 01 27, 2025). 

(49) National Informatics Centre (NIC) Informatics Division. NIST Chemistry Web Book. https://webbook.nist.gov/chemistry/(accessed 01 27, 2025). 

(50) _Mid-Infrared Spectroscopy | Natural Resources Conservation Service_ . https://www.nrcs.usda.gov/conservation-basics/naturalresource-concerns/soil/mid-infrared-spectroscopy (accessed 01 27, 2025). 

(51) Goodge, K. E.; Vederman, C. J.; Wentz, C. M.; Landauer, A. K.; Forster, A. L. _Near Infrared Spectra of Origin-Defined and Real-World Textiles (NIR-SORT): A Spectroscopic and Materials Characterization Dataset for Known Provenance and Post-Consumer Fabrics_ . 2066 files, 1.95 GB, 2024.. 

(52) Cabernard, L.; Roscher, L.; Lorenz, C.; Gerdts, G.; Primpke, S. _Environ. Sci. Technol._ 2018, _52_ (22), 13279−13288. 

(53) Forland, B. M.; Hughey, K. D.; Wilhelm, M. J.; Williams, O. N.; Cappello, B. F.; Gaspar, C. L.; Myers, T. L.; Sharpe, S. W.; Johnson, T. J. _Appl. Spectrosc._ 2024, _78_ (5), 486−503. 

(54) Hapich, H.; Cowger, W.; Gray, A. B. _Environ. Sci. Technol._ 2024, _58_ (46), 20502−20512. 

(55) Ge, A.; Zhao, S.; Sun, C.; Yuan, Z.; Liu, L.; Chen, L.; Li, F. _Sci. Total Environ._ 2024, _912_ , 168919. 

(56) Crutchett, T. W.; Bornt, K. R. _MethodsX_ 2024, _12_ , 102638. 

(57) Savitzky, A.; Golay, M. J. E. _Anal. Chem._ 1964, _36_ (8), 1627− 1639. 

(58) Schubert, E.; Rousseeuw, P. J. _Inf. Syst._ 2021, _101_ , 101804. 

(59) Maechler, M.; Rousseeuw, P.; Struyf, A.; Hubert, M.; Hornik, 

K. _Cluster.: Cluster Analysis Basics and Extensions_ ; 2023. (60) Friedman, J.; Hastie, T.; Tibshirani, R. J. _Stat. Soft_ 2010, _33_ (1), 1. 

(61) Clayden, J. _Mmand: Mathematical Morphology in Any Number of Dimensions_ , 2023. 

(62) Mayerhöfer, T. G.; Pahlow, S.; Popp, J. _ChemPhysChem_ 2020, _21_ (18), 2029−2046. 

(63) _Analyze, Process, Identify, and Share Raman and (FT)IR Spectra_ . https://rawcdn.githack.com/wincowgerDEV/OpenSpecy-package/ c253d6c3298c7db56fbfdceee6ff0e654a1431cd/index.html (accessed 01 28, 2025). 

(64) Jenkins, T.; Persaud, B. D.; Cowger, W.; Szigeti, K.; Roche, D. G.; Clary, E.; Slowinski, S.; Lei, B.; Abeynayaka, A.; Nyadjro, E. S.; et al. _Front. Environ. Sci._ 2022, _10_ , 912107. 

(65) Back, H. d. M.; Vargas Junior, E. C.; Alarcon, O. E.; Pottmaier, 

D. _Chemosphere_ 2022, _287_ (Pt 1), 131903. 

(66) Harrold, Z.; Arienzo, M. M.; Collins, M.; Davidson, J. M.; Bai, 

X.; Sukumaran, S.; Umek, J. _ACS ES&T Water_ 2022, _2_ (2), 268−277. 

(67) Schindelin, J.; Arganda-Carreras, I.; Frise, E.; Kaynig, V.; Longair, M.; Pietzsch, T.; Preibisch, S.; Rueden, C.; Saalfeld, S.; Schmid, B.; Tinevez, J.-Y.; White, D. J.; Hartenstein, V.; Eliceiri, K.; Tomancak, P.; Cardona, A. _Nat. Methods_ 2012, _9_ (7), 676−682. 

(68) Primpke, S.; Cross, R. K.; Mintenig, S. M.; Simon, M.; Vianello, 

A.; Gerdts, G.; Vollertsen, J. _Appl. Spectrosc._ 2020, _74_ , 1127. 

(69) _ParticleFinder_ . https://www.horiba.com/int/scientific/ products/detail/action/show/Product/particle-finder-1657/(accessed 01 28, 2025).. 

(70) _KnowItAll Analytical Ed. Software_ . Wiley Science Solutions. https://sciencesolutions.wiley.com/knowitall-analytical-editionsoftware/(accessed 01 28, 2025).. 

(71) _OMNIC[TM] Specta Software_ . https://www.thermofisher.com/ order/catalog/product/833-036200 (accessed 01 28, 2025). 

(72) _OPUS_ � _Spectroscopy Software_ . https://www.bruker.com/en/ products-and-solutions/infrared-and-raman/opus-spectroscopysoftware.html (accessed 01 28, 2025). 

**17355** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

**Analytical Chemistry** 

**pubs.acs.org/ac** 

Article 

(73) Roscher, L.; Halbach, M.; Nguyen, M. T.; Hebeler, M.; Luschtinetz, F.; Scholz-Böttcher, B. M.; Primpke, S.; Gerdts, G. _Sci. Total Environ._ 2022, _817_ , 152619. 

(74) Mhatre, A. M.; Chappa, S.; Ojha, S.; Pandey, A. K. _Sep. Sci. Technol._ 2019, _54_ (9), 1469−1477. 

(75) Román-Zas, C.; Ferreiro, B.; Terán-Baamonde, J.; Estela Del Castillo Busto, M.; Andrade, J. M.; Muniategui, S. _Spectrochim. Acta, Part A_ 2025, _327_ , 125321. 

(76) Hagelskjær, O.; Crézé, A.; Le Roux, G.; Sonke, J. E. _Microplast. Nanoplast._ 2023, _3_ , 22. 

(77) Abel, S. M.; Primpke, S.; Int-Veen, I.; Brandt, A.; Gerdts, G. _Environ. Pollut._ 2021, _269_ , 116095. 

(78) Wagner, J.; Robberson, W.; Allen, H. _Chemosphere_ 2022, _304_ , 135295. 

**==> picture [241 x 324] intentionally omitted <==**

**17356** 

https://doi.org/10.1021/acs.analchem.5c00962 _Anal. Chem._ 2025, 97, 17345−17356 

