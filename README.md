# Fuzzy logic to evaluate the SDG11 degree of compliance 

## Introduction
Today, our society faces challenges derived from technological, environmental, productive and social progress. One of the most widespread is to meet the Sustainable Development Goals, designed as a plan to achieve a better and more sustainable future for all. These 17 interconnected global goals are included in a UNGA Resolution called the 2030 Agenda.

Therefore, the challenge is not only to achieve these objectives but also to make them measurable to be comparable and to capture the real social progress in sustainability. One of the most widely used and referenced tools to date is the Sustainable Development Report. It is a global assessment of countries' progress towards Sustainable Development Goals and complements the official SDG indicators and voluntary national reviews.

The current development expressed here is intended to advance on the calculation of the report mentioned above, which, after a first strategic step, establishes a five-step decision tree and uses the normalisation criterion following the equation x′=(x-min. (x))/(max. (x)-min. (x))*100. Our development concretely advances Sustainable Development Goal 11, which focuses on making cities and human settlements inclusive, safe, liveable and sustainable.

The available data has been reinterpreted and the evaluation system based on an arithmetic mean has been replaced  with a system based on fuzzy logic, which allows for the incorporation of expert judgement.

# Fuzzy Inference System

In order to obtain an assessment of an SDG, its indicators as currently defined in the report are taken as input variables. In the case of SDG 11, these are: 
- Proportion of urban population living in slum, in percentage terms [%]
- Annual mean concentration of particulate matter of less than 2.5 microns in diameter (PM2.5) [mg/m3]
- Access to improved water source, in percentage terms of urban population [%]
- Satisfaction with public transport, in percentage [%]
- Population with rent overburden, in percentage [%]

## EDA
Firstly, data from Sustainable Development Report 2022 is explored in [sd-report.ipynb](https://github.com/marialonsogar/fuzzy-compliance-SDG11/blob/main/fuzzy-sdg11/sd-report.ipynb). We have seen that only 14.51% of data have information for all the five indicators. There are 8 possible combinations of avaible indicators, so 8 models are proposed depending on the input variables recorded. Finally, we have extracted the ranges of values that the variables can take for each defined colour. 

## Modeling
Subsequently, we use this information to define the Fuzzy logic Inference System (FIS) with the class defined in [VariableFIS.py](https://github.com/marialonsogar/fuzzy-compliance-SDG11/blob/main/fuzzy-sdg11/VariableFIS.py) and the process and demo explained in [fuzzy-system-demo.ipynb](https://github.com/marialonsogar/fuzzy-compliance-SDG11/blob/main/fuzzy-sdg11/fuzzy-system-demo.ipynb).

<img src="doc\fis.svg">

## Results
With this approach, a model is built dinamically after knowing the available indicators for a country. The system uses these as input variables. After applying this method, the best and worst ranked countries are, respectively:

| **Country**           | **$\nu_1$** | **$\nu_2$** | **$\nu_3$** | **$\nu_4$** | **$\nu_5$** | **FIS Evaluation** |
|:---------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:------------------:|
| **Brunei Darussalam** | -                    | 5.102                | 99.60                | -                    | -                    | 89.771             |
| **Tonga**             | -                    | 10.117               | 99.75                | -                    | -                    | 83.243             |
| **Tuvalu**            | -                    | 10.251               | 100.00               | -                    | -                    | 82.202             |
| **Andorra**           | -                    | 11.189               | 100.00               | -                    | -                    | 75.114             |
| **Netherlands**       | 0                    | 11.411               | 100.00               | 78.0                 | 6.144                | 74.950             |

| **Country**                  | **$\nu_1$** | **$\nu_2$** | **$\nu_3$** | **$\nu_4$** | **$\nu_5$** | **FIS Evaluation** |
|:----------------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:------------------:|
| **Togo**                     | 53.3                 | 41.082               | 41.827               | 29.0                 | -                    | 10.079             |
| **South Sudan**              | 97.3                 | 46.141               | 10.489               | 18.0                 | -                    | 10.079             |
| **Afghanistan**              | 73.5                 | 54.950               | 41.859               | 34.0                 | -                    | 10.078             |
| **Equatorial Guinea**        | 66.1                 | 59.020               | 48.115               | -                    | -                    | 10.078             |
| **Central African Republic** | 98.5                 | 61.733               | 32.291               | 25.0                 | -                    | 10.078             |


| Best ranked countries by FIS | Worst ranked countries by FIS |
|------------------------------|-------------------------------|
| Brunei Darussalam            | Togo                          |
| Tonga                        | South Sudan                   |
| Tuvalu                       | Afghanistan                   |
| Andorra                      | Equatorial Guinea             |
| Netherlands                  | Central African Republic      |
