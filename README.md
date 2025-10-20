# WRF–ERA5 Validation & Climate Analysis

This project demonstrates a complete **climate data analysis pipeline**, covering data acquisition, processing, and visualization. It uses **ERA5 reanalysis data**—a trusted global climate dataset—to reveal regional climate patterns in **Canterbury, New Zealand (2024)**.

---

## 1. Overview

This **experimental portfolio project** highlights an end-to-end workflow for climate data processing using **free and open-source ERA5 reanalysis data** from the **Copernicus Climate Data Store (CDS)**.  
The analysis focuses on the **year 2024**, at a **0.25° × 0.25°** spatial resolution, to demonstrate practical data engineering, geospatial, and visualization techniques.

---

## 2. Pipeline Summary

The project consists of three main stages:

1. **Data Acquisition**  
   `download_era5.py` connects to the CDS API to download hourly weather data for a specific region and time period.

2. **Climate Statistics & Visualization**  
   `era5_climate_analysis.py` processes NetCDF files, computes key statistics (e.g., temperature, wind speed, precipitation), and generates visualizations with Matplotlib + Cartopy.

3. **Advanced Pattern Analysis (SOM)**  
   `som_analysis.py` applies a Self-Organizing Map (SOM) to identify dominant regional climate regimes—an example of unsupervised machine learning for pattern discovery.

---

## 3. Key Features

- Automated data download from CDS API  
- Standard NetCDF data processing  
- Geospatial visualization with Cartopy  
- SOM-based climate pattern detection  
- Violin and bar plots for seasonal statistics  
- Fully reproducible, script-based workflow  

---

## 4. Visual Outputs

Representative plots for **Canterbury (2024)**:

| Visualization | Description |
|----------------|-------------|
| ![Annual Mean Temperature](plots/annual_mean_temperature_map.png) | Annual mean 2 m temperature — spatial gradients across the region |
| ![Monthly Temperature Distribution](plots/monthly_temperature_violin.png) | Monthly temperature distributions (violin plot) showing seasonal cycles |
| ![Monthly Wind Speed](plots/monthly_wind_speed_bar.png) | Average monthly wind speed (bar chart) |
| ![Wind Speed Distribution](plots/wind_speed_violin.png) | Annual wind-speed variability (violin plot) |
| ![Mean Temperature Map](plots/canterbury_mean_temp_map.png) | Coastal-to-mountain temperature contrast |
| ![Total Precipitation](plots/canterbury_total_precip_map.png) | Annual precipitation totals — illustrating the rain-shadow effect |
| ![SOM Clustering](plots/som_era5_2024_clusters.png) | SOM clustering of ERA5 climate patterns, revealing dominant regimes |

---

## 5. Getting Started

### Prerequisites
- Python 3.8 or later  
- CDS API account (Copernicus Climate Data Store)

### Installation
```bash
git clone <your-repository-url>
cd WRF-ERA5_Validation
pip install -r requirements.txt
```

### API Configuration
Copy `.cdsapirc.example` → `.cdsapirc` and add your CDS API URL & key (available on your CDS profile).

---

## 6. Running the Workflow

```bash
# 1. Download ERA5 data
python download_era5.py

# 2. Analyze and visualize
python era5_climate_analysis.py

# 3. Run SOM clustering
python som_analysis.py
```

All plots are saved under the `plots/` directory.

---

## 7. Future Improvements

- Integrate **WRF model outputs** for validation  
- Extend analysis to additional variables (e.g., humidity, pressure)  
- Add **interactive dashboards** (Plotly, Bokeh)  
- Enable large-scale or cloud-based processing  
- Automate **report generation** and archiving  

---

## 8. Limitations / Notes

Due to CDS API constraints, data are downloaded **per month** to separate files:

- `era5_YYYY_MM_temp_wind.nc` – temperature & wind  
- `era5_YYYY_MM_precip.nc` – precipitation  

This ensures consistent handling of instantaneous and accumulated fields.

---

## 9. Data Source & Citation

**Dataset:**  
ERA5 Hourly Data on Single Levels (1940 – present)  
DOI: [10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.adbb2d47)

**Reference:**  
Hersbach H. et al. (2020). *The ERA5 global reanalysis.*  
*Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999 – 2049.  
DOI: [10.1002/qj.3803](https://doi.org/10.1002/qj.3803)

**License:**  
ERA5 data © Copernicus Climate Change Service, licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## 10. Dataset Summary

| Attribute | Details |
|------------|----------|
| **Type** | Gridded reanalysis data |
| **Resolution** | 0.25° × 0.25° (~28 km) |
| **Temporal Coverage** | 1940 – present (hourly) |
| **Format** | NetCDF |
| **Region** | 30° S – 50° S, 165° E – 180° E |
| **Year** | 2024 |

### Variables Used
| Variable | Description | Derived Metrics |
|-----------|--------------|-----------------|
| 2 m Temperature | Near-surface air temperature | Annual mean, monthly distribution |
| 10 m U/V Wind Components | Eastward & northward wind velocity | Mean speed, wind regime patterns |
| Total Precipitation | Accumulated liquid + frozen water | Annual total, spatial distribution |

---

## 11. License (for Code)

All source code is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
