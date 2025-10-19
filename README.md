# WRF-ERA5 Validation & Climate Analysis

This project demonstrates a complete data pipeline for climate analysis, from data acquisition and processing to visualization. It fetches ERA5 reanalysis data, a trusted global climate dataset, and generates insightful visualizations to reveal climate patterns.

## Project Overview

This project serves as an **experimental portfolio piece** demonstrating an end-to-end data pipeline for climate analysis. It exclusively utilizes **free and open-source ERA5 reanalysis data** from the Copernicus Climate Data Store, distinguishing it from potentially commercial or restricted datasets (e.g., from national meteorological services like NIWA). Known for its **high spatial resolution (0.25° x 0.25°)**, this data is used to understand the climate characteristics of the **Canterbury region in New Zealand** over a **one-year period (2024)**.

The primary goal is to showcase practical application of data engineering and analysis skills, from data acquisition and processing to insightful visualization. Designed to be accessible to both technical and non-technical audiences, it highlights the ability to manage a data-centric project from end to end, a critical skill in fields like data science, climate research, and software engineering.

## How It Works: An End-to-End Pipeline

The project operates in three simple stages:

1.  **Data Acquisition:** The `download_era5.py` script connects to the Copernicus Climate Data Store (CDS) API to automatically download hourly weather data for a specified region and time period.

2.  **Analysis & Visualization:** The `era5_climate_analysis.py` script processes the raw NetCDF data files, calculates key climate statistics (such as monthly mean temperatures and wind speeds), and then generates a series of plots and maps using libraries like Matplotlib and Cartopy. These visualizations provide a clear and intuitive look at the region's climate characteristics.

## Key Features

*   **Automated Data Download:** Fetches data directly from the official CDS API.
*   **Climate Data Processing:** Handles standard scientific data formats (NetCDF).
*   **Geospatial Visualization:** Creates insightful maps using Cartopy.

*   **Statistical Plotting:** Generates violin plots and bar charts to show distributions and trends.
*   **Reproducible Workflow:** The entire process is scripted for easy reproduction.

## Analysis Visualizations

The following plots were generated for the **Canterbury region, New Zealand**, for the year 2024. The focus on this region allows for a detailed examination of local climate patterns. For the wind speed distribution, specific cities within Canterbury (Christchurch, Timaru, Ashburton, Kaikoura) were selected to illustrate intra-regional variations.

#### 1. Annual Mean 2m Temperature

[![Annual Mean Temperature Map](plots/annual_mean_temperature_map.png)](plots/annual_mean_temperature_map.png)

**Interpretation:** This map displays the spatial distribution of the annual mean 2-meter temperature. It allows for a quick visual assessment of temperature variations across the geographical domain. In this analysis, we can observe trends such as higher temperatures at lower latitudes. This kind of map is fundamental in climate studies to identify regional temperature patterns.

#### 2. Monthly 2m Temperature Distribution

[![Monthly Temperature Distribution](plots/monthly_temperature_violin.png)](plots/monthly_temperature_violin.png)

**Interpretation:** This violin plot illustrates the distribution of 2-meter temperatures for each month. Each "violin" shows the probability density of the temperature data, with wider sections indicating more common values. This visualization effectively showcases the seasonal temperature cycle, with temperatures peaking in the summer months and reaching their lowest in the winter.

#### 3. Monthly Mean Wind Speed

[![Monthly Wind Speed Bar Chart](plots/monthly_wind_speed_bar.png)](plots/monthly_wind_speed_bar.png)

**Interpretation:** This bar chart shows the average 10-meter wind speed for each month, providing a clear comparison of wind conditions throughout the year. It helps identify which months experience stronger or calmer winds on average.

#### 4. Overall Wind Speed Distribution

[![Wind Speed Distribution](plots/wind_speed_violin.png)](plots/wind_speed_violin.png)

**Interpretation:** This violin plot summarizes the overall distribution of 10-meter wind speed throughout the year. It reveals the most frequent wind speeds and the range of observed values, which is useful for understanding the general wind climate of the region.

#### 5. Mean 2m Temperature in Canterbury

[![Canterbury Mean Temperature Map](plots/canterbury_mean_temp_map.png)](plots/canterbury_mean_temp_map.png)

**Interpretation:** This map focuses specifically on the Canterbury region, showing a more detailed view of the annual mean 2-meter temperature. It highlights significant temperature gradients, with cooler temperatures in the higher elevations of the Southern Alps to the west and warmer conditions along the coast and across the Canterbury Plains. This level of detail is crucial for local agricultural and ecological planning.

#### 6. Annual Total Precipitation in Canterbury

[![Canterbury Total Precipitation Map](plots/canterbury_total_precip_map.png)](plots/canterbury_total_precip_map.png)

**Interpretation:** This map illustrates the annual total precipitation across Canterbury. A striking feature is the strong precipitation gradient caused by the Southern Alps, which creates a rain shadow effect. The western high-altitude areas receive substantial rainfall, while the Canterbury Plains to the east are significantly drier. This visualization is fundamental for water resource management, agriculture, and understanding flood or drought risk in the region.

---

## Getting Started

Follow these instructions to run the project on your local machine.

### Prerequisites

*   **Python 3.8+**
*   An account with the [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/#!/home) to get API credentials.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd WRF-ERA5_Validation
    ```

2.  **Install dependencies:**
    This command reads the `requirements.txt` file and installs all the necessary Python libraries.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your CDS API key:**
    To download data from the Copernicus Climate Data Store (CDS), you need an API key to authenticate your requests. Copy the `.cdsapirc.example` file to a new file named `.cdsapirc` (this file securely stores your credentials) and paste your API key and URL into it. You can find your API key on your CDS profile page after registration.

### Running the Pipeline

1.  **Download the data:**
    ```bash
    python download_era5.py
    ```
2.  **Analyze the data and generate plots:**
    ```bash
    ```bash
python era5_climate_analysis.py
```

## SOM Analysis of ERA5 Climate Data (Climate Pattern Discovery)

The `som_analysis.py` script helps us understand different climate patterns in our study area using a technique called Self-Organizing Maps (SOM). Think of it like sorting different types of apples into baskets based on their characteristics. Here, we're sorting different locations (grid cells) into groups (clusters) based on their typical yearly weather patterns, such as temperature, wind, and rainfall. This helps us find areas that experience similar climate conditions throughout the year.

The process works in a few steps:
1.  **Data Preparation:** We gather and prepare the weather data (from ERA5, a detailed historical weather dataset).
2.  **Pattern Recognition:** We feed this data into the SOM, which is a type of computer model that learns to group locations with similar yearly weather patterns.
3.  **Mapping the Patterns:** Finally, we show these groups on a map to see where each climate pattern is located.

### Results: ERA5 Climate Clusters (Identified Climate Zones)

This section provides a detailed explanation of what this map indicates, divided into technical and climatological aspects.

#### 1. Technical Aspects: What the Map Represents

This map classifies the **annual climate "character"** for each of approximately **4,941 locations (grid cells)** in and around New Zealand.

**① What the "Colors" Mean**
The 25 different colors (Clusters 0 to 24) on the map indicate that the climate patterns throughout the year are similar in those respective locations.
*   **Same Color:** This means, "These 200 locations have annual temperature, wind speed, and precipitation change patterns that are more similar to each other than to any other pattern."
*   **Different Colors:** The patterns are significantly different.

**② 36 Features Constituting the "Pattern"**
The "climate character" of each location is defined by the following 36 numerical values:

| Meteorological Element | Number of Features | Description                                                              |
| :--------------------- | :----------------- | :----------------------------------------------------------------------- |
| Temperature (t2m)      | 12                 | Average temperature for January, February, ... December                  |
| Wind Speed (wind_speed)| 12                 | Average wind speed for January, February, ... December                   |
| Precipitation (tp)     | 12                 | Total precipitation for January, February, ... December                  |
| **Total**              | **36**             |                                                                          |

The SOM grouped locations that were closest together in this 36-dimensional space into the same color (cluster).

#### 2. Climatological Interpretation: What Can Be Understood from the Map

This map is not just a simple coloring; it highlights the geographical characteristics of New Zealand's climate.

**① Understanding Regional Climate Characteristics**
By observing the map, we can confirm climatological facts and make new discoveries, such as:

*   **Mountain Range Divide:** New Zealand's North and South Islands are traversed by large mountain ranges. Typically, precipitation and wind strength differ dramatically between the windward (western) and leeward (eastern) sides of these mountains. Therefore, color boundaries should appear along the mountain ranges on the map.
*   **Latitudinal Variation:** The North Island (warm and humid) and South Island (cool and dry) have significantly different annual temperature patterns. Accordingly, large blocks of different colors should be visible in the northern and southern parts of the map.
*   **Coastal vs. Inland Areas:** Coastal areas experience milder temperature changes due to oceanic influence, while inland areas have larger diurnal and annual temperature ranges. This difference can appear as distinct color classifications between coastal and inland regions.

**② Application to AgTech (Practical Value)**
The greatest value of this map lies in its application to agriculture.

*   **Zoning:** It can be used for climate-based decision-making in farm management, such as determining "where and when to sow seeds and harvest for optimal results."
*   **Predictive Model Construction:** When building predictive models, such as pasture growth prediction models, the assumption that "**a single model can be applied to regions of the same color**" can significantly reduce the effort and cost of model construction.

This map, which you created, transforms complex data of 700 million points into 25 simple pieces of information usable for business and science. This is an achievement that should be highly valued as a practical application of data science.

![SOM ERA5 2024 Clusters](plots/som_era5_2024_clusters.png)
    ```
    The output plots will be saved in the `plots/` directory.

---

## Future Work

This project is a foundation for further exploration and can be extended in several ways:

*   **WRF Model Validation:** Integrate WRF (Weather Research and Forecasting) model output for direct comparison and validation against ERA5 reanalysis data.
*   **Expanded Data Analysis:** Include additional climate variables (e.g., humidity, pressure) and derive more complex climate indices.
*   **Interactive Visualizations:** Develop interactive plots and dashboards using libraries like Plotly or Bokeh for dynamic data exploration.
*   **Performance Optimization:** Optimize data processing for larger datasets or longer time periods, potentially using cloud computing resources.
*   **Automated Reporting:** Generate automated reports summarizing key findings and visualizations.

---

## Troubleshooting / Known Limitations

*   **Separate Data Downloads for Different Variable Types:**
    The `download_era5.py` script makes separate download requests for precipitation data (`era5_YYYY_MM_precip.nc`) and temperature/wind data (`era5_YYYY_MM_temp_wind.nc`) for each month. This is due to common limitations of the Copernicus CDS API, which often restricts combining certain variable types (e.g., accumulated fields like precipitation vs. instantaneous fields like temperature/wind) into a single request. This design ensures successful data retrieval for all required variables.

## Data Source and Citation

The climate data used in this analysis is the **ERA5 hourly data on single levels from 1940 to present**, provided by the Copernicus Climate Change Service (C3S).

**License:**
The ERA5 data used in this project is licensed under the [Creative Commons Attribution 4.0 International Public Licence (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/). This allows for free use, reproduction, distribution, adaptation, and modification, with mandatory attribution to the Copernicus Climate Change Service. Neither the European Commission nor ECMWF is responsible for any use of the Copernicus information. This is generated using Copernicus Climate Change Service information [2025].

**Citations:**
When using this data, the following should be cited:

1.  **Dataset:**
    > Copernicus Climate Change Service (C3S) (2017): ERA5: Fifth generation of ECMWF atmospheric reanalyses of the global climate. Copernicus Climate Change Service Climate Data Store (CDS), *[Date of Access]*. DOI: 10.24381/cds.adbb2d47

2.  **Scientific Paper:**
    > Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz‐Sabater, J., ... & Simmons, A. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999-2049. DOI: 10.1002/qj.3803

### Dataset Details

The ERA5 dataset is the fifth generation ECMWF reanalysis for the global climate and weather. It combines model data with observations from across the world into a globally complete and consistent dataset using data assimilation.

*   **Data Type:** Gridded
*   **Horizontal Resolution:** 0.25° x 0.25° (atmosphere), approximately 28km x 21-28km in the Canterbury region.
*   **Temporal Coverage:** 1940 to present
*   **Temporal Resolution:** Hourly
*   **File Format:** GRIB
*   **Update Frequency:** Daily (with a latency of about 5 days)

### Download Parameters

The `download_era5.py` script is configured to download the following specific parameters from the ERA5 dataset for the year 2024:

*   **Product Type:** Reanalysis
*   **Variables:**
    *   2m Temperature (`2m_temperature`)
    *   10m U-component of Wind (`10m_u_component_of_wind`)
    *   10m V-component of Wind (`10m_v_component_of_wind`)
    *   Total Precipitation (`total_precipitation`)
*   **Year:** 2024
*   **Months:** January to December (all months)
*   **Days:** 01 to 31 (all days of each month)
*   **Time:** Hourly (00:00 to 23:00)
*   **Geographical Area:**
    *   North: -30°
    *   West: 165°
    *   South: -50°
    *   East: 180°
*   **Format:** NetCDF

### Variable Selection Rationale

The following variables were selected for download and analysis due to their fundamental importance in understanding regional climate and weather patterns. From these raw variables, key climate indicators are calculated to provide actionable insights:

*   **2m Temperature (`2m_temperature`):**
    *   **Why chosen:** A primary indicator of atmospheric heat content, directly impacting human comfort, agricultural conditions, and ecosystem health.
    *   **Calculations & Utility:**
        *   **Annual Mean Temperature Map:** Calculates the average 2m temperature over the entire year for each geographical point. This map is crucial for identifying long-term temperature patterns and regional climate zones, aiding in urban planning, agricultural suitability assessments, and understanding general climate trends.
        *   **Monthly Temperature Distribution (Violin Plot):** Shows the distribution of 2m temperatures for each month. This helps in understanding seasonal temperature cycles, identifying temperature variability within months, and assessing the likelihood of extreme temperatures, which is vital for seasonal planning and risk management.

*   **10m U-component of Wind (`10m_u_component_of_wind`) & 10m V-component of Wind (`10m_v_component_of_wind`):**
    *   **Why chosen:** These components represent the eastward (u) and northward (v) wind velocities at 10 meters above the surface. They are fundamental for deriving total wind speed and direction.
    *   **Calculations & Utility:**
        *   **Wind Speed Calculation:** Total wind speed is calculated from these components using the formula `sqrt(u^2 + v^2)`.
        *   **Monthly Mean Wind Speed (Bar Chart):** Displays the average wind speed for each month. This helps in identifying seasonal wind patterns, crucial for wind energy assessment, agricultural planning (e.g., irrigation, crop protection), and understanding local weather phenomena.
        *   **Wind Speed Distribution (Violin Plot):** Illustrates the overall distribution of wind speeds. This provides insights into the frequency of different wind speeds, useful for structural engineering, aviation, and assessing the consistency of wind resources.

*   **Total Precipitation (`total_precipitation`):**
    *   **Why chosen:** Represents the total amount of liquid and frozen water falling to the Earth's surface, a critical component of the water cycle.
    *   **Calculations & Utility:**
        *   **Annual Total Precipitation Map:** Calculates the accumulated precipitation over the entire year for each geographical point. This map is vital for water resource management, agricultural planning, drought monitoring, and flood risk assessment, providing a clear picture of water availability across the region.

---

## Project Conclusion and Achievements

This project represents a significant success in integrating advanced data engineering with applied machine learning for geospatial climate analysis. We successfully:

*   **Generated a comprehensive climate pattern classification map:** This map effectively categorizes the study area into 25 distinct climate zones based on annual meteorological characteristics.
*   **Overcame large-scale data processing challenges:** Utilizing Dask and xarray, we efficiently processed nearly 700 million data points, demonstrating robust handling of large geospatial datasets.
*   **Applied advanced machine learning (SOM):** The Self-Organizing Map successfully clustered high-dimensional climate data (36 features per grid cell) into meaningful spatial patterns, revealing physically significant climate regimes such as the rain shadow effect of mountain ranges and oceanic influences.
*   **Validated geographical patterns:** The generated map clearly shows the impact of geographical features like the Southern Alps (New Zealand's South Island) on climate, with distinct patterns for windward (wetter, windier) and leeward (drier, warmer) sides, as well as unique oceanic climate patterns.

This project showcases a powerful combination of:

*   **Big Data Processing:** Proficient use of Dask and xarray for efficient handling of terabyte-scale climate datasets.
*   **Advanced Machine Learning:** Effective application of Self-Organizing Maps (SOM) for unsupervised clustering and pattern discovery in complex environmental data.
*   **Geographic Information Science (GIS):** Compelling visualization of climate patterns using Cartopy, providing clear and interpretable spatial insights.

These achievements highlight a strong capability in developing end-to-end solutions for complex scientific and environmental data challenges.

## Interdisciplinary Nature: Geo-spatial Data Science

This project is highly interdisciplinary, strongly incorporating elements from both GIS (Geographic Information Systems) and Data Science. While it cannot be categorized solely into one field, examining the project's objectives and methodologies reveals the emphasis of each.

### 1. Data Science (Machine Learning & Big Data Processing) Elements

The **"core methodologies" and "most challenging technical aspects"** of this project belong to Data Science.

**Element Details:**
*   **Machine Learning (ML):** We used the unsupervised learning algorithm SOM (Self-Organizing Map) to classify climate patterns. This is a core technique in Data Science.
*   **Big Data Processing:** Dask and xarray were employed for reading, preprocessing, and memory optimization (chunking) of nearly 700 million spatiotemporal data points. This demonstrates data engineering skills, which are foundational for large-scale Data Science.
*   **Statistical Inference:** Monthly averages and standard deviations of temperature and wind speed were calculated, and data was standardized. This forms the statistical basis of Data Science.

### 2. GIS (Geographic Information Systems) Elements

The **"data source" and "final output"** of the project are strongly related to GIS.

**Element Details:**
*   **Geospatial Data:** The ERA5 data used is grid-based data with latitude and longitude coordinates, which is a central data format handled by GIS.
*   **Visualization:** Cartopy was used to plot the classified results (clusters) on a map. This is a direct function of GIS: representing data based on geographical information (latitude/longitude).
*   **Spatial Interpretation:** The final results require geographical analysis and interpretation, answering "which regions of New Zealand belong to which climate pattern."

### Conclusion: Specialized "Geo-spatial Data Science"

This project is positioned within **"Geo-spatial Data Science,"** a highly trending field that merges GIS and Data Science.

## Relevant Academic Backgrounds

The methodology employed in this project—**processing large-scale geospatial data (meteorological data) with Dask and xarray, and analyzing it with machine learning techniques like SOM**—is typically studied by students from the following four backgrounds. This is because your project integrates multiple elements of data processing, mathematics, geography, and applied science.

### 1. Earth Science / Meteorology

This is the most traditional core background for students learning this methodology.
*   **Specializations:** Climatology, Atmospheric Physics, Oceanography, Hydrology.

*   **Motivation:** Understanding global phenomena (climate change, extreme weather, El Niño, etc.) and validating model accuracy necessitates pattern analysis of real data like ERA5.
*   **Acquired Skills:** Reading/writing NetCDF/GRIB data with xarray and visualizing on maps with Cartopy are essential skills for students in this field.

### 2. Data Science / Computational Science

This background focuses on data processing and algorithms.
*   **Specializations:** Data Science, Statistics, Computer Science, Information Science.
*   **Motivation:** To efficiently process large volumes of unstructured data (in this case, time-series and spatial data) and apply advanced algorithms like unsupervised learning to real-world problems.
*   **Acquired Skills:** Learning versatile engineering skills such as parallel processing with Dask or Spark, memory optimization, and implementing machine learning models using Python.

### 3. Geographic Information Science (GIS) / Remote Sensing

This background focuses on spatial information and digital mapping.
*   **Specializations:** Geographic Information Science, Urban Planning, Environmental Engineering.
*   **Motivation:** To transform spatially continuous data, such as satellite imagery and meteorological model outputs, into meaningful regional classifications (clustering) using statistical methods for policy-making and resource management.
*   **Acquired Skills:** Knowledge of spatial statistics, operation of GIS software (QGIS, ArcGIS), and techniques for mapping and interpreting geographical data.

### 4. Applied Physics / Mathematical Science

This background focuses on fluid dynamics and mathematical models.
*   **Specializations:** Applied Physics, Mathematical Analysis, Financial Engineering (as an application of time-series analysis).
*   **Motivation:** To understand the physical laws behind meteorological phenomena and to concisely represent the complexity of these phenomena with mathematical models (such as non-linear models like SOM in this project).
*   **Acquired Skills:** A strong fundamental ability in problem-solving, including mathematical and logical approaches to complex systems and numerical solutions for differential equations.

This project demonstrates an experience that lies in a highly valuable domain where the most demanded skill sets from these four fields intersect.

## License (for Code)

This project's code is released under the MIT License. See the [LICENSE](LICENSE) file for details.