pubs.acs.org/ac 

Technical Note 

**==> picture [177 x 69] intentionally omitted <==**

## Microplastic Spectral Classification Needs an Open Source Community: Open Specy to the Rescue! 

Win Cowger,* Zacharias Steinmetz, Andrew Gray, Keenan Munno, Jennifer Lynch, Hannah Hapich, Sebastian Primpke, Hannah De Frond, Chelsea Rochman, and Orestis Herodotou 

Cite This: Anal. Chem. 2021, 93, 7543−7548 

Read Online 

ACCESS Metrics & More Article Recommendations *sı Supporting Information 

ABSTRACT: Microplastic pollution research has suffered from inadequate data and tools for spectral (Raman and infrared) classification. Spectral matching tools often are not accurate for microplastics identification and are cost-prohibitive. Lack of accuracy stems from the diversity of microplastic pollutants, which are not represented in spectral libraries. Here, we propose a viable software solution: Open Specy. Open Specy is on the web (www. openspecy.org) and in an R package. Open Specy is free and allows users to view, process, identify, and share their spectra to a community library. Users − can upload and process their spectra using smoothing (Savitzky Golay filter) and polynomial baseline correction techniques (IModPolyFit). The processed spectrum can be downloaded to be used in other applications or 

**==> picture [202 x 109] intentionally omitted <==**

identified using an onboard reference library and correlation-based matching criteria. Open Specy’s data sharing and session log features ensure reproducible results. Open Specy houses a growing library of reference spectra, which increasingly represents the diversity of microplastics as a contaminant suite. We compared the functionality and accuracy of Open Specy for microplastic identification to commonly used spectral analysis software. We found that Open Specy was the only open source software and the only software with a community library, and Open Specy had comparable accuracy to popular software (OMNIC Picta and KnowItAll). Future developments will enhance spectral identification accuracy as the reference library and functionality grows through community-contributed spectra and community-developed code. Open Specy can also be used for applications beyond microplastic analysis. Open Specy’s source code is open source (CC-BY-4.0, attribution only) (https://github.com/wincowgerDEV/ OpenSpecy). 

S pectroscopymicroplastics.is[1][,][2] aMicroplastics are plastic particles betweencritical step for polymer identification of 1 mm and 1 μm in size with various physical and chemical properties.[3][,][4] Raman and Fourier transform infrared (FTIR) spectroscopy are the most common techniques for identifying plastic particles in microplastic studies.[5] In environmental microplastic studies, plastic particles are extracted from an environmental matrix (e.g., sediment, water) using chemical and physical procedures. In some procedures, particles are filtered and the whole sample is analyzed using automated Raman or FTIR. Alternatively, particles are counted on a filter manually or extracted from a matrix, and individual particles are analyzed via Raman or FTIR. The spectra are first visually assessed for quality to determine if additional spectral measurements are necessary, then processed to amplify the signal-to-noise ratio and remove the presence of baseline signals, and finally matched using a reference library that contains plastic and nonplastic spectra. 

Because microplastics are a diverse suite of contaminants,[3] they require adaptable tools and extensive reference libraries for accurate matching. New specialized matching techniques that focus on peak regions of the reference spectra are shown to drastically outperform the standard techniques for micro- 

plastics research.[6] Open source software could be rapidly adapted to include this and other new techniques. Pure unweathered polymers are not commonly found in the environment.[7][,][8] Microplastic reference libraries should include many phases of particle degradation, additive mixtures, and colors for accurate matching,[9][,][10] but only a small number of spectra are openly available. A recently published review on microplastics data analysis techniques found that more than half of the research groups duplicated efforts by developing inhouse spectral tools and matching libraries but not sharing them with the wider scientific community.[5] We developed an open source tool, library, and community called Open Specy to satisfy these needs while improving functionality and accuracy for identifying plastic particles compared to commercial tools and libraries. 

**==> picture [39 x 58] intentionally omitted <==**

Received: January 11, 2021 Accepted: May 6, 2021 Published: May 19, 2021 

https://doi.org/10.1021/acs.analchem.1c00123 Anal. Chem. 2021, 93, 7543−7548 

© 2021 American Chemical Society 

7543 

Analytical Chemistry pubs.acs.org/ac 

Technical Note 

**==> picture [505 x 281] intentionally omitted <==**

Figure 1. Workflow diagram for features and data pipeline in Open Specy. Interactive and updated version: https://lucid.app/lucidchart/e43cc83bb50a-46c5-a58c-a8a2d5b7423f/view. 

First, we describe the design of Open Specy and its supporting documentation. Then, we compare Open Specy’s functionality to other spectroscopy software. Lastly, we validate Open Specy for microplastic analysis by comparing its accuracy to commercial spectroscopy software and outline how Open Specy will foster a scientific community and better spectral identification moving forward. 

## ■[EXPERIMENTAL][SECTION] 

Open Specy Features and Documentation. Open Specy users can view, process, identify, and share their IR and Raman spectra (Figure 1). We created Open Specy in R (4.0.4)[11] using the RStudio IDE,[12] with the shiny,[13] ggplot2,[14] smoother,[15] dplyr,[16] plotly,[17] data.table,[18] signal,[19] shinyjs,[20] shinythemes,[21] shinyWidgets,[22] shinyBS,[23] digest,[24] config,[25] osfr,[26] knitr,[27] rmarkdown,[28] testthat,[29] mongolite,[30] loggit,[31] DT,[32] rdrop2,[33] hyperSpec,[34] and hexView[35] libraries. Open Specy is online at www.openspecy.org and on CRAN as an R package[36] with extensive documentation, help guidance, and error guidance on the Web site. In the R package, the base functions in Open Specy can be accessed to expand the existing functionality for other use cases. The source code (written in R) and reference library materials are available on Github (https://github.com/wincowgerDEV/OpenSpecy) and Open Science Framework (OSF, https://osf.io/x7dpz/). The code and databases are version-controlled so that older versions can be retrieved by users who need to revive an older working session for any reason. We also thoroughly detailed step-by-step instructions for using the tool.[37] 

A typical workflow for microplastic spectral identification in Open Specy consists of file upload, processing, and identification. Before upload, users select whether they want their uploaded data and session logs to be shared with the 

spectroscopy community or not. Shared data will help advance the tool and make users’ work reproducible. Users can add metadata to make their uploaded data more useful. Metadata explanations are given in a live document (https://osf.io/ bgdqf/) and in the tool. Any shared data with metadata will be vetted by experienced spectroscopy experts and added to the tool if it meets our quality requirements (https://osf.io/ w9s43/). All shared data is automatically shared under a license of the user’s choice and uploaded on OSF as funding allows (https://osf.io/rjg3c/). A test spectrum can be uploaded in several formats (asp, csv, spa, spc, jdx, and 0). Once uploaded, a spectrum can be viewed in an interactive window with zoom, pan, screenshot, and layer on and off functionality. 

Users can then process their spectrum using smoothing with a Savitzky and Golay filter,[38] and baseline correction with IModPolyFit.[39] We translated the script provided at https:// github.com/michaelstchen/modPolyFit for IModPolyFit from MATLAB to R.[40] The IModPolyFit function iteratively finds the baseline by fitting a polynomial regression of the specified order to the whole spectrum. Many of the large peaks are identified on the first iteration because they stand above the fit and are ignored for further iterations. The iterative process finalizes once the difference between successive fits is minimal. The processed spectrum can be downloaded as a csv file. 

Lastly, users can identify their spectrum to the onboard spectral library and interactively view the matches. The spectral library currently consists of a Raman library with 3696 spectra from RRUFF,[41] 759 spectra from the Raman Open Database,[42] 208 spectra from Cabernard et al.,[43] 58 spectra from the Raman Spectroscopic Library UCL Chemistry,[44] 44 spectra from the Open Specy community members Dora Mehn, Jennifer Lynch, and Claudia Cella, and 15 spectra from Horiba Scientific. The FTIR library consists of 325 spectra 

7544 

https://doi.org/10.1021/acs.analchem.1c00123 Anal. Chem. 2021, 93, 7543−7548 

Analytical Chemistry pubs.acs.org/ac Technical Note 

Table 1. Meta-Analysis of Tool Base Functionality and Utility for Spectroscopy Analysis Software Available Today[a] 

||Open<br>Specy48|siMPle46|Spectragryph47|KnowItAll49|OMNIC50|Essential<br>FTIR51|Spec<br>Tools52|FDM Search<br>Faster53|Raman<br>Tool Set54|LabSpec55|
|---|---|---|---|---|---|---|---|---|---|---|
|process spectra|X|X|X|X|X|X|X||X|X|
|fnd match to library|X|X|X|X|X|X||X|||
|made for Raman and|X|X|X|X|X||X|X|||
|FTIR|||||||||||
|technical support|X|X|X|X|X|X||X||X|
|free|X|X|X||||X||X||
|add spectra to library|X|X|X|X|X||||||
|nonplastic spectra in|X|X|X|X|||||||
|library|||||||||||
|plastic spectra in library|X|X|X|X|||||||
|spectral map analysis||X|||||||X|X|
|library data open access|X|X|X||||||||
|environmentally|X|X|||||||||
|weathered materials|||||||||||
|documented software|X|X|||||||||
|QAQC|||||||||||
|source code available|X||||||||||
|crowdsourced library|X||||||||||



> aSoftware tools are listed on the top row. All software are assessed for basic functions/uses listed on the left axis. Tools are organized from most functions to least from left to right, and functions are organized from most common to least from top to bottom. “X” indicates that the tool has the functionality, and blank indicates the tool does not have the functionality. 

from Primke et al.,[45] 272 spectra from Chabuka et al.,[10] and 39 spectra from Thermo Fisher Scientific. These spectra have all been manually adjusted to remove baseline and noise. A second version of each reference library was made by removing signal regions that are not the peaks as described in Renner et al.[6] The user can choose to use the whole spectrum libraries or the peak spectrum libraries for identification. The matching procedure consists of a Pearson correlation between the chosen reference spectra and test spectrum. When matching is initiated, a grouped correction strategy first minimum-normalizes (intensity minus minimum intensity) over the whole spectrum or for each peak region depending on what the user specifies. The Pearson correlation coefficient is used directly as the hit quality index for ranking matches. The matches are returned in an interactive display that allows users to view matches individually alongside the test spectrum, and detailed metadata of any selected spectrum is displayed. To assess a good match, inspect peaks to ensure that the match has all of the same peaks with the same shape and the same height ratio. From our experience, when top matches are below 0.6 Pearson correlation coefficient, they should be suspected to be a result of incorrect preprocessing, poor quality spectra, or of a material type not currently in the reference library. User selections during preprocessing and matching are also logged to advance future developments of the application and ensure reproducibility of all manipulations to the spectra. 

Ensuring accuracy through validation, inclusivity, and transparency are primary goals for our group. Validation is conducted on Open Specy whenever new spectra or default settings are added to the library (https://osf.io/zcafk/). Validation must demonstrate greater than 80% accuracy for the whole procedure for these updates to be made to the tool. Currently, the validation statistics are above 90%. Anyone can use Open Specy free of charge. As Open Specy grows, these features will become more robust and numerous. Everyone is welcomed to collaborate with us to write publications, develop the tool, and share data. We have detailed a framework for collaboration in the Open Specy group (https://osf.io/q94dc/ 

), and anyone is welcome to take the project and build something new with it that they publish themselves. Furthermore, we respond to any bug reports and feature requests from users as quickly as possible and track updates that are pushed to the web (https://github.com/ wincowgerDEV/OpenSpecy/issues). 

## ■[RESULTS][AND][DISCUSSION] 

Review of the Current Tools. We searched for other Raman and FTIR spectroscopy spectral analysis tools and compared their base functionality to Open Specy (Table 1). We found that Open Specy has microplastic identification functionality that is not standard in all commercial spectroscopy software (e.g., standard OMNIC does not have a reference library and standard LabSpec cannot find a match to a library). Two other notable tools, siMPle[46] and Spectragryph,[47] share their library spectra, are free to use, and are highly functional at processing spectra and spectral matching. siMPle was also developed with microplastic analysis in mind and was designed to analyze full spectral maps from hyperspectral scanning devices.[46] Due to web hosting costs for large data sets, we have not yet implemented that functionality in Open Specy online. However, automation routines can be deployed using the R package functions from the Open Specy package, which could be iterated on a hyperspectral map or a large number of spectra. Only siMPle and Open Specy provided documented validation of the entire software routine for accurately identifying spectra. We suspect that the tools lacking validation documentation are undergoing validation, but the procedure is not transparent, which should be relevant to anyone using those tools. Most of the tools, including free tools like Open Specy and siMPle, offered users technical support. None of the spectral tools, besides Open Specy, made their source code available or had a crowd sourced library. Making the source code available will allow others to remix and reuse all the field components and subject the tool to perpetual peer review from users who identify software bugs as they arise and fix them. The crowd sourced library will make Open Specy 

7545 

https://doi.org/10.1021/acs.analchem.1c00123 Anal. Chem. 2021, 93, 7543−7548 

Analytical Chemistry 

pubs.acs.org/ac 

Technical Note 

competitive with commercial libraries, which rely heavily on pure materials for their reference spectra. Open Specy incorporates diverse spectra from diverse materials and already includes weathered materials to improve spectral identification accuracy for microplastic research.[10] The advancements brought by Open Specy are critical to the advancement of microplastic identification. Identifying microplastics accurately requires a maximum level of transparency and modularity in the tools. 

Validation of Open Specy. We compared the material identification accuracy of Open Specy to OMNIC Picta software for FTIR and KnowItAll and ID Expert for Raman spectra using 50 highly validated plastic materials published in another manuscript.[9] The samples included 1 to 10 representatives of 9 polymer Raman spectra and 1 to 5 representatives of 14 different FTIR ATR polymers. The Raman and FTIR spectra from these test materials did not exist in any of the software tested. We processed the test spectra using baseline correction and smoothing techniques to amplify the signal-to-noise ratio in each software, then had the software identify the spectra using the standard matching procedure, and assessed the top ten matches for a true positive result to the known identity of the spectra. If at least one of the spectra in the top 10 matches was true, we accepted the software answer as true. A detailed explanation of the validation procedure and supporting data is available in the Supporting Information (https://osf.io/6yjmc/). We found that Open Specy currently outperforms KnowItAll (correct: Open Specy = 48/50, KnowItAll = 44/50) for Raman spectra and slightly underperforms OMNIC Picta for FTIR spectra (correct: Open Specy = 48/50, OMNIC = 49/50). The Raman spectra misidentified in Open Specy were a polyethylene spectrum and a polyamide spectrum. The two misidentified FTIR spectra were polyethylene vinyl acetate and polyvinyl chloride. We are prioritizing additions of a greater diversity of these spectra in future releases of Open Specy and encourage community members to share references for these spectra. We expect that OMNIC Picta performed similarly to Open Specy because the Primkpe library,[45] which has a diverse suite of consumer plastic materials relevant to microplastic research, was installed in OMNIC. Since Open Specy is an open source tool, we will be able to increase the accuracy over time using community shared spectra (https://osf.io/rjg3c/). 

## ■[CONCLUSION] 

Over 2000 unique users have currently visited Open Specy, usage time on the Web site averages 250 h per month, and nine peer-reviewed publications have already used and recommended Open Specy for microplastic spectral analysis.[5][,][56][−][63] We are dedicated to continual improvements in Open Specy, and we respond to all inquiries. In this way, the authors, their research groups, and the scientific community at large will support the development of a robust and evergrowing spectral identification and processing tool. There is a growing list of feature requests that we will respond to as time and funding allow (https://github.com/wincowgerDEV/ OpenSpecy/issues). Immediate future developments will incorporate machine learning (in process, https://osf.io/ bes7h/) and fusion matching approaches[10] to improve match accuracy and analysis simplicity. We made the source code for the tool entirely open source so that industry, scientists, and governments can develop and expand its functionality. We invite contributors to join us and have outlined how to 

contribute in the supporting documentation (https://osf.io/ q94dc/). 

## ■[ASSOCIATED][CONTENT] 

## *sı Supporting Information 

The Supporting Information is available free of charge at https://pubs.acs.org/doi/10.1021/acs.analchem.1c00123. 

Offline desktop version Open Specy (ZIP) Uploaded data (ZIP) Deep learning spectral classification (ZIP) Technical documents (ZIP) Shiny app code and data (ZIP) 

## ■[AUTHOR][INFORMATION] 

## Corresponding Author 

- Win Cowger − Department of Environmental Science, University of California, Riverside, Riverside, California 92521, United States; orcid.org/0000-0001-9226-3104; Email: wincowger@gmail.com, wcowg001@ucr.edu 

## Authors 

- Zacharias Steinmetz − University of Koblenz-Landau, iES Landau, Institute for Environmental Sciences, Group of Environmental and Soil Chemistry, 76829 Landau, Germany; orcid.org/0000-0001-6675-5033 

- Andrew Gray − Department of Environmental Science, University of California, Riverside, Riverside, California 92521, United States 

- Keenan Munno − University of Toronto, Toronto, Ontario M5S 3B2, Canada; orcid.org/0000-0003-2916-5944 

- Jennifer Lynch − Chemical Sciences Division, National Institute of Standards and Technology, Waimanalo, Hawai‘i 96795, United States; Center for Marine Debris Research, Hawai‘i Pacific University, Waimanalo, Hawai‘i 96795, United States; orcid.org/0000-0003-3572-8782 

- Hannah Hapich − Department of Environmental Science, University of California, Riverside, Riverside, California 92521, United States 

- Sebastian Primpke − Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Biologische Anstalt Helgoland, 27498 Helgoland, Germany; orcid.org/00000001-7633-8524 

- Hannah De Frond − University of Toronto, Toronto, Ontario M5S 3B2, Canada; orcid.org/0000-0003-1199-0727 

- Chelsea Rochman − University of Toronto, Toronto, Ontario M5S 3B2, Canada; orcid.org/0000-0002-7624-711X 

- Orestis Herodotou − 

Complete contact information is available at: https://pubs.acs.org/10.1021/acs.analchem.1c00123 

## Author Contributions 

W. Cowger created the software and led the writing of the manuscript. Z. Steinmetz led the development and deployment of the Open Specy CRAN package, advanced the code base, advised on development priorities, and drafted and revised the manuscript. O. Herodotou provided technical assistance for web deployment of Open Specy. All others contributed equally by beta testing and validating Open Specy, advising on development priorities, and drafting and revising the manuscript. 

## Notes 

The authors declare no competing financial interest. 

7546 

https://doi.org/10.1021/acs.analchem.1c00123 Anal. Chem. 2021, 93, 7543−7548 

Analytical Chemistry 

pubs.acs.org/ac 

Technical Note 

All supporting information is cited as links throughout the manuscript as living documents, data, and source code, which will be indefinitely available on the OSF home page https:// osf.io/3uatf/. These documents were downloaded into a zip file at the time of publication as part of the Supporting Information in this manuscript but will not be perpetually updated like the OSF page. The zip file structure follows the OSF page. Documents are grouped by use. Folder names follow the citations referenced throughout the manuscript. ReadMe text files are written in folders that need an additional explanation about the files contained within and their relationships. The ReadMe files follow the documentation on OSF. 

(7) Waldschläger, K.; Born, M.; Cowger, W.; Gray, A.; Schuttrumpf, H. Environ. Res. 2020, 191, 110192. 

(8) ter Halle, A.; Ladirat, L.; Martignac, M.; Mingotaud, A. F.; Boyron, O.; Perez, E. Environ. Pollut. 2017, 227, 167−174. 

(9) Munno, K.; De Frond, H.; O’Donnell, B.; Rochman, C. M. Anal. Chem. 2020, 92 (3), 2443−2451. 

(10) Chabuka, B. K.; Kalivas, J. H. Appl. Spectrosc. 2020, 74 (9), 1167−1183. 

(11) R Core Team. R: A Language and Environment for Statistical Computing; The R Foundation: Vienna, Austria,2020. 

(12) RStudio Team. RStudio: Integrated Development Environment for R; RStudio Team: Boston, MA,2020. 

(13) Chang, W.; Cheng, J.; Allaire, J. J.; Xie, Y.; McPherson, J. Shiny: Web Application Framework for R; 2020. 

(14) Wickham, H. Ggplot2: Elegant Graphics for Data Analysis; 2016. 

## ■[ACKNOWLEDGMENTS] 

We would like to thank the active Open Specy community for providing feedback and guidance on developing the tool to where it is today. Horiba Scientific and Thermo Fischer Scientific donated reference spectra and expert time to inform the tool development, specifically Bridget O’Donnell, Suja Sukumaran, Eunah Lee, and Andrew Whitley provided substantial support. W. Cowger was supported by the National Science Foundation Graduate Research Fellowship. The UCR Office of Technology Partnerships partially supported Open Specy’s development. A. Gray was supported in part by the USDA National Institute of Food and Agriculture Hatch program [Project Number CA-R-ENS-5120-H], USDA Multistate Project W4170 funds, UCANR AES Mission funds, and a NOAA Marine Debris Research grant [Grant NA19NOS990086]. K. Munno was supported by funds from the Georgia Aquarium and H. De Frond by funds from the Southern California Coastal Water Research Project. Certain commercial equipment, instruments, or materials are identified in this paper to adequately specify the experimental procedure. Such identification does not imply recommendation or endorsement by the National Institute of Standards and Technology nor does it imply that the materials or equipment identified are necessarily the best available for the purpose. 

## ■[REFERENCES] 

(1) Brander, S. M.; Renick, V. C.; Foley, M. M.; Steele, C.; Woo, M.; Lusher, A.; Carr, S.; Helm, P.; Box, C.; Cherniak, S. L.; Andrews, R. C.; Rochman, C. Appl. Spectrosc. 2020, 74, 1099. 

(2) Primpke, S.; Christiansen, S. H.; Cowger, W.; De Frond, H.; Deshpande, A.; Fischer, M.; Holland, E. B.; Meyns, M.; O’Donnell, B. A.; Ossmann, B. E.; Pittroff, M.; Sarau, G.; Scholz-Böttcher, B. M.; Wiggin, K. J. Appl. Spectrosc. 2020, 74, 1012. 

(3) Rochman, C. M.; Brookson, C.; Bikker, J.; Djuric, N.; Earn, A.; Bucci, K.; Athey, S.; Huntington, A.; McIlwraith, H.; Munno, K.; De Frond, H.; Kolomijeca, A.; Erdle, L.; Grbic, J.; Bayoumi, M.; Borrelle, S. B.; Wu, T.; Santoro, S.; Werbowski, L. M.; Zhu, X.; Giles, R. K.; Hamilton, B. M.; Thaysen, C.; Kaura, A.; Klasios, N.; Ead, L.; Kim, J.; Sherlock, C.; Ho, A.; Hung, C. Environ. Toxicol. Chem. 2019, 38 (4), 703−711. 

(4) Hartmann, N. B.; Huffer, T.; Thompson, R. C.; Hassellöv, M.; Verschoor, A.; Daugaard, A. E.; Rist, S.; Karlsson, T.; Brennholt, N.; Cole, M.; Herrling, M. P.; Hess, M. C.; Ivleva, N. P.; Lusher, A. L.; Wagner, M. Environ. Sci. Technol. 2019, 53 (3), 1039−1047. 

(5) Cowger, W.; Gray, A.; Christiansen, S. H.; DeFrond, H.; Deshpande, A. D.; Hemabessiere, L.; Lee, E.; Mill, L.; Munno, K.; Ossmann, B. E.; Pittroff, M.; Rochman, C.; Sarau, G.; Tarby, S.; Primpke, S. Appl. Spectrosc. 2020, 74, 989. 

(6) Renner, G.; Schmidt, T. C.; Schram, J. Anal. Chem. 2017, 89 (22), 12045−12053. 

(15) Hamilton, N. Smoother: Functions Relating to the Smoothing of Numerical Data; 2015. 

(16) Wickham, H.; Francois, R.; Henry, L.; Muller, K. Dplyr: A Grammar of Data Manipulation; 2020. 

(17) Sievert, C. Interactive Web-Based Data Visualization with R, Plotly, and Shiny; Chapman and Hall/CRC, 2020. 

(18) Dowle, M.; Srinivasan, A. Data.Table: Extension of data.Frame; 2020. 

(19) signal developers. signal: Signal Processing; 2014. 

(20) Attali, D. Shinyjs: Easily Improve the User Experience of Your Shiny Apps in Seconds; 2020. 

(21) Chang, W. Shinythemes: Themes for Shiny; 2018. 

(22) Perrier, V.; Meyer, F.; Granjon, D. ShinyWidgets: Custom Inputs Widgets for Shiny; 2020. 

(23) Bailey, E. ShinyBS: Twitter Bootstrap Components for Shiny; 2015. 

(24) Eddlebuettel, D.; Antoine Lucas, D. E.; Tuszynski, J.; Bengtsson, H.; Urbanek, S.; Frasca, M.; Lewis, B.; Stokely, M.; Muehleisen, H.; Murdoch, D.; Hester, J.; Wu, W.; Kou, Q.; Onkelinx, 

T.; Lang, M.; Simko, V.; Hornik, K.; Neal, R.; Bell, K.; de Queljoe, M.; Suruceanu, I.; Denney, B.; Schumacher, D.; Chang, W. Digest: Create Compact Hash Digests of R Objects; 2020. 

(25) Allaire, J. J. Config: Manage Environment Specific Configuration Values; 2020. 

(26) Wolen, A. R.; Hartgerink, C. H. J.; Hafen, R.; Richards, B. G.; Soderberg, C. K.; York, T. P. J. Open Source Softw. 2020, 5 (46), 2071. (27) Xie, Y. Knitr: A General-Purpose Package for Dynamic Report Generation in R; 2020. 

(28) Allaire, J. J.; Xie, Y.; McPherson, J.; Luraschi, J.; Ushey, K.; Atkins, A.; Wickham, H.; Cheng, J.; Chang, W.; Iannone, R. Rmarkdown: Dynamic Documents for R; 2020. 

(29) Wickham, H. R J. 2011, 3, 5−10. 

(30) Ooms, J. The Jsonlite Package: A Practical and Consistent Mapping Between JSON Data and R Objects arXiv 2014, 1403.2805 

- (31) Price, R. Loggit: Modern Logging for the R Ecosystem; 2021. 

- (32) Xie, Y.; Cheng, J.; Tan, X. DT: A Wrapper of the JavaScript 

- Library “DataTables; 2020. 

(33) Ram, K.; Yochum, C. Rdrop2: Programmatic Interface to the “Dropbox” API; 2020. 

(34) Beleites, C.; Sergo, V. HyperSpec: A Package to Handle Hyperspectral Data Sets in R; 2020. 

- (35) Murrell, P. HexView: Viewing Binary Files; 2019. 

(36) Cowger, W.; Steinmetz, Z. OpenSpecy: Analyze, Process, Identify, and Share, Raman and (FT)IR Spectra; 2021. 

(37) Meyers, J.; Conkle, J.; Cowger, W.; Steinmetz, Z.; Gray, A.; Rochman, C.; Primpke, S.; Lynch, J.; Hapich, H.; De Frond, H.; Keenan Munno, B. O. Open Specy Standard Operating Procedure . https://htmlpreview.github.io/?https://github.com/ wincowgerDEV/OpenSpecy/blob/main/vignettes/sop.html (accessed 2021-04-04). 

(38) Savitzky, A.; Golay, M. J. E. Anal. Chem. 1964, 36 (8), 1627− 1639. 

(39) Zhao, J.; Lui, H.; McLean, D. I.; Zeng, H. Appl. Spectrosc. 2007, 61 (11), 1225−1232. 

7547 

https://doi.org/10.1021/acs.analchem.1c00123 Anal. Chem. 2021, 93, 7543−7548 

Analytical Chemistry 

pubs.acs.org/ac 

Technical Note 

(40) Ghosal, S.; Chen, M.; Wagner, J.; Wang, Z.-M.; Wall, S. Environ. Pollut. 2018, 233, 1113−1124. 

(41) Lafuente, B.; Downs, R.; Yang, H.; Stone, N. The Power of Databases: The RRUFF Project. In Highlights in Mineralogical Crystallography; Armbruster, T., Danisi, R. M., Eds.; W. Gruyter: Berlin, Germany, 2015. 

(42) El Mendili, Y.; Vaitkus, A.; Merkys, A.; Grazulis, S.; Chateigner, D.; Mathevet, F.; Gascoin, S.; Petit, S.; Bardeau, J.-F.; Zanatta, M.; Secchi, M.; Mariotto, G.; Kumar, A.; Cassetta, M.; Lutterotti, L.; Borovin, E.; Orberger, B.; Simon, P.; Hehlen, B.; Le Guen, M. J. Appl. Crystallogr. 2019, 52 (3), 618−625. 

(43) Cabernard, L.; Roscher, L.; Lorenz, C.; Gerdts, G.; Primpke, S. Environ. Sci. Technol. 2018, 52 (22), 13279−13288. 

(44) Ian M. Bell, Robin J. H. Clark and Peter J. Gibbs Christopher Ingold Laboratories. Raman Spectroscopic Library. http://www.chem. ucl.ac.uk/resources/raman/. 

(45) Primpke, S.; Wirth, M.; Lorenz, C.; Gerdts, G. Anal. Bioanal. Chem. 2018, 410, 5131−5141. 

(46) Primpke, S.; Cross, R. K.; Mintenig, S. M.; Simon, M.; Vianello, 

A.; Gerdts, G.; Vollertsen, J. Appl. Spectrosc. 2020, 74 (9), 1127. 

(47) Menges, F. Spectragryph. https://www.effemm2.de/ spectragryph/about.html. 

(48) Cowger, W.; Steinmetz, Z.; Gray, A.; Hapich, H.; Rochman, C.; Lynch, J.; Primpke, S.; Herodotou, O. Open Specy. www.openspecy. org. 

(49) Wiley. KnowItAll. https://sciencesolutions.wiley.com/ knowitall-spectroscopy-software/. 

(50) ThermoFisher Scientific. OMNIC. https://www.thermofisher. com/order/catalog/product/833-036200#/833-036200. 

(51) Operant LLC. Essential FTIR. https://www.essentialftir.com/. 

(52) Schlösser, M. Spec Tools. http://spectools.sourceforge.net/ software.html. 

(53) Fiveash Data Management, Inc. FDM Search Faster. https:// www.fdmspectra.com/FDM_SearchFaster_for_FTIR_and_Raman. html. 

(54) Source Forge. Raman Tool Set. https://sourceforge.net/ projects/ramantoolset/. 

(55) Horiba. LabSpec. https://www.horiba.com/en_en/products/ detail/action/show/Product/labspec-6-spectroscopy-suite-software1843/. 

(56) Amrutha, K.; Warrier, A. K. Sci. Total Environ. 2020, 739, 140377. 

(57) Yokota, K.; Mehlrose, M. Water 2020, 12 (9), 2650. 

(58) Battaglia, F. M.; Beckingham, B. A.; McFee, W. E. Mar. Pollut. Bull. 2020, 160, 111677. 

(59) Miller, E.; Sedlak, M.; Lin, D.; Box, C.; Holleman, C.; Rochman, C. M.; Sutton, R. J. Hazard. Mater. 2021, 409, 124770. (60) Prata, J. C.; da Costa, J. P.; Fernandes, A. J. S.; Mendes da Costa, F.; Duarte, A. C.; Rocha-Santos, T. Sci. Total Environ. 2021, 783, 146979. 

(61) Sarkar, D. J.; Das Sarkar, S.; Das, B. K.; Praharaj, J. K.; Mahajan, D. K.; Purokait, B.; Mohanty, T. R.; Mohanty, D.; Gogoi, P.; Kumar V, S.; Behera, B. K.; Manna, R. K.; Samanta, S. J. Hazard. Mater. 2021, 413, 125347. 

(62) Sparks, C.; Awe, A.; Maneveld, J. Mar. Pollut. Bull. 2021, 166, 112186. 

(63) Sarkar, D. J.; Das Sarkar, S.; Das, B. K.; Sahoo, B. K.; Das, A.; Nag, S. K.; Manna, R. K.; Behera, B. K.; Samanta, S. Water Res. 2021, 192, 116853. 

7548 

https://doi.org/10.1021/acs.analchem.1c00123 Anal. Chem. 2021, 93, 7543−7548 

