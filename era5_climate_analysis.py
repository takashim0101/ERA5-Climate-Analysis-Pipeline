import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
import cartopy.crs as ccrs
from matplotlib.colors import LogNorm

# --- Dask Client Setup ---
try:
    from dask.distributed import Client
    client = Client(n_workers=4, threads_per_worker=1)
    print("Dask client started:", client)
except (ImportError, RuntimeError):
    print("Dask distributed is not installed or failed to start. Running in single-threaded mode.")

# --- Data Loading and Chunking (Initial checks omitted for brevity) ---
temp_wind_files = glob.glob("downloaded_data/era5_2024_*_temp_wind.nc")
precip_files = glob.glob("downloaded_data/era5_2024_*_precip.nc")

print(f"Found {len(temp_wind_files)} temp/wind files.")
print(f"Found {len(precip_files)} precip files.")

try:
    xr.set_options(use_new_combine_kwarg_defaults=True)
except ValueError:
    pass

ds_temp_wind = xr.open_mfdataset(temp_wind_files, combine='by_coords', chunks={'valid_time': 'auto'})
ds_precip = xr.open_mfdataset(precip_files, combine='by_coords', chunks={'valid_time': 'auto'})
era5_ds = xr.merge([ds_temp_wind, ds_precip])
print("\nERA5 Dataset (Temp, Wind, Precip) merged and chunked for Dask.")

# -----------------------------------------------------------------
# --- Monthly and Annual Mean Wind Speeds ---
U = era5_ds['u10']
V = era5_ds['v10']
wind_speed = np.sqrt(U**2 + V**2)
wind_speed.name = 'wind_speed'

# Note: latitude slice is reversed to ensure correct selection
canterbury_speed = wind_speed.sel(latitude=slice(-43, -45), longitude=slice(170, 174))

annual_mean = canterbury_speed.mean().compute()
print(f"Canterbury Region Annual Mean Wind Speed: {annual_mean.item():.2f} m/s")

# !!! CRITICAL FIX: Average across 'latitude' and 'longitude' to get only 12 monthly values !!!
# Step 1: Group by month and compute mean (this is what produced the 1836 rows)
monthly_mean_by_loc = canterbury_speed.groupby('valid_time.month').mean()

# Step 2: Now, average these means across the spatial dimensions (latitude and longitude)
monthly_mean = monthly_mean_by_loc.mean(dim=['latitude', 'longitude']).compute()

# Step 3: Convert the 12-value xarray DataArray into a DataFrame
monthly_df = monthly_mean.to_dataframe(name='Mean_Wind_Speed')
monthly_df.index.name = 'Month'
# -----------------------------------------------------------------

print("\nCanterbury Region Monthly Mean Wind Speed:")
# This output should now show only 12 rows (Month 1 to 12)
print(monthly_df)

# --- Visualization 1: Monthly Mean Wind Speed Bar Chart ---
plt.figure(figsize=(12, 6))

# This will now plot only 12 bars
monthly_df['Mean_Wind_Speed'].plot(kind='bar', color='skyblue') 

plt.title('Canterbury Region Monthly Mean Wind Speed')
plt.ylabel('Mean Wind Speed (m/s)')
plt.xlabel('Month')

month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Matplotlib can now easily label the 12 bars
plt.xticks(ticks=np.arange(len(month_labels)), labels=month_labels, rotation=45) 

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot to a file
monthly_wind_bar_path = "plots/monthly_wind_speed_bar.png"
os.makedirs(os.path.dirname(monthly_wind_bar_path), exist_ok=True)
plt.savefig(monthly_wind_bar_path)

# Use plt.show() to display the plot in VS Code (instead of plt.close())
plt.show() 

print(f"\nMonthly wind speed bar chart saved to: {monthly_wind_bar_path}")

cities = {
    'Christchurch': [-43.53, 172.63],
    'Timaru': [-44.39, 171.27],
    'Ashburton': [-43.90, 171.75],
    'Kaikoura': [-42.40, 173.68]
}

plot_data = []
city_labels = []

for city, coords in cities.items():
    city_series = canterbury_speed.sel(latitude=coords[0], longitude=coords[1], method='nearest')
    data_points = city_series.compute().values.flatten()
    plot_data.append(data_points)
    city_labels.append(city)

plt.figure(figsize=(12, 7))
plt.violinplot(plot_data, showmedians=True)
plt.xticks(np.arange(1, len(cities) + 1), city_labels)
plt.title("Wind Speed Distribution in Canterbury Cities (ERA5 Data)")
plt.ylabel("Hourly Wind Speed (m/s)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
violin_plot_path = "plots/wind_speed_violin.png"
plt.savefig(violin_plot_path)
plt.close()
print(f"\nViolin plot saved to: {violin_plot_path}")

# --- Median Annual Statistics and Visualizations ---
temp_celsius = era5_ds['t2m'] - 273.15
canterbury_temp = temp_celsius.sel(latitude=slice(-43, -45), longitude=slice(170, 174))
canterbury_annual_mean_temp_map = canterbury_temp.mean(dim='valid_time').compute()
canterbury_annual_mean_temp = float(np.nanmedian(canterbury_annual_mean_temp_map))
print(f"\nCanterbury Median of Annual Mean Temperature: {canterbury_annual_mean_temp:.2f} °C")

# --- Visualization 2: Canterbury Annual Mean Temperature Map ---
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
canterbury_annual_mean_temp_map.plot.pcolormesh(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap='coolwarm',
    cbar_kwargs={'label': 'Mean Temperature (°C)'}
)
ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.title('Canterbury Annual Mean Temperature')
plt.tight_layout()
canterbury_temp_map_path = "plots/canterbury_mean_temp_map.png"
plt.savefig(canterbury_temp_map_path)
plt.close()
print(f"Canterbury temperature map saved to: {canterbury_temp_map_path}")

# --- Precipitation Analysis ---
precip_mm = era5_ds['tp'].diff(dim='valid_time', label='lower') * 1000
precip_mm = precip_mm.fillna(0)
canterbury_rain = precip_mm.sel(latitude=slice(-43, -45), longitude=slice(170, 174))
canterbury_total_rainfall_map = canterbury_rain.sum(dim='valid_time').compute()
canterbury_total_rainfall = float(np.nanmedian(canterbury_total_rainfall_map))
print(f"\nCanterbury Median of Annual Total Precipitation: {canterbury_total_rainfall:.2f} mm")

# --- Visualization 3: Canterbury Annual Total Precipitation Map ---
plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
canterbury_total_rainfall_map.plot.pcolormesh(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap='Blues',
    # norm=LogNorm(),
    cbar_kwargs={'label': 'Total Precipitation (mm)'}
)
ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.title('Canterbury Annual Total Precipitation')
plt.tight_layout()
canterbury_precip_map_path = "plots/canterbury_total_precip_map.png"
plt.savefig(canterbury_precip_map_path)
plt.close()
print(f"Canterbury precipitation map saved to: {canterbury_precip_map_path}")

print("\nAnalysis and visualization complete.")