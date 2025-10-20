import xarray as xr
import pandas as pd
import numpy as np
from sklearn_som.som import SOM
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
from matplotlib.colors import Normalize

# --- Configuration ---
DATA_DIR = "downloaded_data"
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 1. Load ERA5 Data ---
print("--- 1. Loading ERA5 Data ---")

file_pattern_temp_wind = os.path.join(DATA_DIR, "era5_2024_*_temp_wind.nc")
file_pattern_precip = os.path.join(DATA_DIR, "era5_2024_*_precip.nc")

try:
    ds_temp_wind = xr.open_mfdataset(file_pattern_temp_wind, combine='by_coords') 
    ds_precip = xr.open_mfdataset(file_pattern_precip, combine='by_coords')
    
    ds = xr.merge([ds_temp_wind, ds_precip], compat='no_conflicts')

    # DASK OPTIMIZATION: Rechunk the data by month 
    ds = ds.chunk({'valid_time': 744, 'latitude': -1, 'longitude': -1}) 
    
    print("Overview of the ERA5 dataset:")
    print(ds)
    
except Exception as e:
    print(f"Error occurred while loading ERA5 data: {e}")
    print("Please ensure files exist in 'downloaded_data' and are not corrupted.")
    exit()

# --- 2. Preprocessing Data and Reshaping for SOM Input ---
print("""
--- 2. Preprocessing Data and Reshaping for SOM Input ---""") 

# --- Unit Conversions and Variable Creations ---
ds['temperature_c'] = ds['t2m'] - 273.15
ds['wind_speed'] = np.sqrt(ds['u10']**2 + ds['v10']**2)

precip_incremental = ds['tp'].diff(dim='valid_time', label='lower') * 1000
precip_incremental = precip_incremental.fillna(0)
ds['total_precipitation_mm_inc'] = precip_incremental

# --- Calculate Monthly Means/Sums ---
monthly_temp = ds['temperature_c'].resample(valid_time='1ME').mean() 
monthly_precip = ds['total_precipitation_mm_inc'].resample(valid_time='1ME').sum() 
monthly_wind = ds['wind_speed'].resample(valid_time='1ME').mean()

# --- Prepare SOM Input Array and Standardization ---
som_input_data_list = []
grid_coords = []
feature_vars = [monthly_temp, monthly_precip, monthly_wind]

# Standardize data (Z-score normalization)
scaled_features = []
for var in feature_vars:
    # Heavy computation part
    var_mean = var.mean().compute()
    var_std = var.std().compute()
    scaled = (var - var_mean) / var_std
    scaled_features.append(scaled)

# Determine coordinate dimensions
lat_dim = ds.latitude.name if 'latitude' in ds.coords else ds.lat.name
lon_dim = ds.longitude.name if 'longitude' in ds.coords else ds.lon.name


for lat_val in ds[lat_dim].values:
    for lon_val in ds[lon_dim].values:
        
        combined_features = []
        for scaled_var in scaled_features:
            features = scaled_var.sel({lat_dim: lat_val, lon_dim: lon_val}, method='nearest').values
            combined_features.extend(features)
        
        combined_features = np.array(combined_features)
        
        if not np.isnan(combined_features).any():
            som_input_data_list.append(combined_features)
            grid_coords.append((lat_val, lon_val))

som_input_data = np.array(som_input_data_list)
grid_coords = np.array(grid_coords)

print(f"Shape of SOM input data (samples x features): {som_input_data.shape}")
print(f"Number of features per sample (12 months * 3 variables): {som_input_data.shape[1]}")


# --- 3. Apply SOM ---
print("""
--- 3. Applying SOM ---""")

# SOM parameters
som_m = 5 
som_n = 5 
som_dim = som_input_data.shape[1]
som_iterations = 1000

print(f"SOM map size: {som_m}x{som_n}, Feature dimension: {som_dim}, Iterations: {som_iterations}")

# CRITICAL FIX: Changed 'num_iteration' to 'n_iter'
som = SOM(m=som_m, n=som_n, dim=som_dim, max_iter=som_iterations, random_state=42)
som.fit(som_input_data)

clusters = som.predict(som_input_data)
print(f"Shape of clustering results: {clusters.shape}")

# --- 4. Display Results and Plot on Map ---
print("""
--- 4. Displaying Results and Plotting on Map ---""")

# Display the number of grid cells belonging to each cluster
unique_clusters, counts = np.unique(clusters, return_counts=True)
print("Number of samples per cluster:")
for cluster_id, count in zip(unique_clusters, counts):
    print(f"  Cluster {cluster_id}: {count} grid cells")

# Plotting clustering results on a map
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Set extent around New Zealand
ax.set_extent([165, 180, -50, -30], crs=ccrs.PlateCarree())

ax.add_feature(cfeature.COASTLINE, linewidth=0.8, zorder=10)
ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
ax.add_feature(cfeature.LAND, facecolor='#f0f0f0') 
ax.add_feature(cfeature.OCEAN, facecolor='#c8e8ff') 
ax.add_feature(cfeature.LAKES, facecolor='#c8e8ff', edgecolor='gray')
ax.add_feature(cfeature.RIVERS, edgecolor='#6bb3ff', linewidth=0.5)

# Plotting clusters for each grid cell using scatter
scatter = ax.scatter(grid_coords[:, 1], grid_coords[:, 0], 
                     c=clusters, 
                     cmap='Spectral', 
                     s=50, 
                     transform=ccrs.PlateCarree(), 
                     edgecolors='none', 
                     alpha=0.8)

plt.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.7, 
             label='SOM Cluster ID (0 to 24)')
plt.title('SOM Clustering of ERA5 Climate Patterns (2024 Monthly Features)', fontsize=16)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Save the plot to a file
plot_filename = os.path.join(OUTPUT_DIR, "som_era5_2024_clusters.png")
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
plt.show()

print(f"\nSOM clustering map saved to '{plot_filename}'.")
print("SOM analysis script execution completed.")