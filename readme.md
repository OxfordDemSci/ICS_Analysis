<img src="./assets/figure_1.png" width="700"/>

# The SHAPE of Impact

![coverage](https://img.shields.io/badge/Purpose-Research-yellow)
[![Generic badge](https://img.shields.io/badge/Python-3.7-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/License-CCBY4.0-purple.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/BuildPassing-Yes-orange.svg)](https://shields.io/)

A repository to analyse the Impact Case Studies submitted to the Research Excellence Framework, 2021. A link to the final, published version of the report will be available in due course.

**Investigators:** Sander Wagner (Co-I), Charles Rahal (Co-I), Douglas Leasure (Co-I), Mark Verhagen (Co-I), Bo Zhao (Co-I) and Melinda C. Mills (PI).

**Researchers/Research Assistants:** Simon Cooper, Ekaterina Degtiareva, Giordano Epifani, Yifan Liu, Brenda Mccollum, Alice Spiers and Reja Wyss.

**Research Support:** Hamza Shams, Bradley Smith, Michelle Thorpe.

**Funders:** British Academy and Academy of Social Sciences.

### Data

The main source of raw data which powers this analysis is the REF 2021 Database. The five key files relate to:
1. The raw REF ICS dataset itself.
2. The 'tags' associated with the raw ICS.
3. The 'environmental' data associated with submitting departments.
4. The 'outputs' dataset, which contains information on submitted academic outputs.
5. The 'results' dataset, which details results across impact, environment, and output.

The REF 2021 data is generally available from [https://results2021.ref.ac.uk/](https://results2021.ref.ac.uk/). All REF submissions information, including downloadable submissions data, REF impact case studies, institution environment statements and unit environment statements can be used under the CC BY 4.0 licence. Use is permitted under [these licence conditions](http://creativecommons.org/licenses/by/4.0/legalcode). Shapefiles for the static analysis are provided by Natural Earth: Free vector and raster map data @ [naturalearthdata.com](naturalearthdata.com).

For specific parts of the analysis (gender, interdisciplinarity, funding, citations and altmetrics), we use data obtained from [Dimensions](https://dimensions.ai/), and re-share parts of it with explicit agreement from [Digital Science](https://www.digital-science.com/).

For a certain number of our analyses, manual curation is necessary. Our manually curated files can be found at `./data/manual`, and include information on:

* Funders who power the Impact Case Studies
* Countries where beneficiaries of the research are located.
* GRID lookup data.
* Identifiers of the underpinning research
* A manually curated list of stopwords.
* A lookup table which maps ICS documents to Topics and Grand Impact Areas.

The final, enhanced, and complete version of our dataset which is made available as part of this project can be found at `./data/final/enhanced_ref_data.csv`, i.e. [here].

### Analysis

The majority of the analysis is split into three distinct types/parts.

1. The first is the BERTopic based large language model. The code which creates this can be found in `./src/topic_modelling.` Thanks to the hard work of [bs-dev](https://github.com/bz-dev) and [lindali97](https://github.com/lindali97) on here!

2. General descriptive code found in `./src/analysis`, which is split into two parts:

* The static analysis, which is found in `./src/analysis/static`, and:
      a. 'Grand Impact Area' by Grand Impact Area outputs (Figures 3-12), and:
* Figures 13-18 which provide broad level analysis of:
    * i. Environment of Impact
    * ii. The Geography of Impact
    * iii. The Funding of Impact
    * iv. The Inter- and Multidisciplinary Nature of Impact	83
    * v. The Gendered Nature of Underpinning Research

* The interactive dashboard. This is found in `./src/dashboard`, and is a standalone repository which is linked to this one as a submodule. 

### Dashboard

An online interactive dashboard accompanies this work, found at [https://shape-impact.co.uk](https://shape-impact.co.uk). This dashboard is entirely reproducible, with code which creates it available at `./src/dashboard. We are especially grateful for the help of [GisRede](https://www.gisrede.com/) for their role in it's development.

### Contact

For any general queries related to this work, please contact `lcds.office@demography.ox.ac.uk` or for media related enquiries, please contact `lcds.office@demography.ox.ac.uk`. For technical issues related to the programmatic analysis of this work, please raise an Issue, or feel free to open a Pull Request.

### License

This work is made available under CC BY 4.0. See `LICENSE` for details.
