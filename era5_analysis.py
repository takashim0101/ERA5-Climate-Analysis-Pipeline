
import xarray as xr
import numpy as np
import dask.diagnostics
import plot_results # Import the plotting module

# ----------------- Configuration -----------------
# Define the directory where downloaded data is stored
DATA_DIR = r'downloaded_data'
# Use glob to find all downloaded NetCDF files for 2024
import glob
DATA_FILES_TEMP_WIND = glob.glob(f'{DATA_DIR}/era5_2024_*_temp_wind.nc')
DATA_FILES_PRECIP = glob.glob(f'{DATA_DIR}/era5_2024_*_precip.nc')


# Read multiple NetCDF files as a single dataset using dask for chunking (Out-of-Core processing).
# This is a crucial design for memory efficiency when scaling to larger datasets.
with dask.diagnostics.ProgressBar():
    ds_temp_wind = xr.open_mfdataset(DATA_FILES_TEMP_WIND, combine='by_coords', chunks={'time': 'auto'}, engine='netcdf4')
    ds_precip = xr.open_mfdataset(DATA_FILES_PRECIP, combine='by_coords', chunks={'time': 'auto'}, engine='netcdf4')
    
    # Merge the two datasets
    ds = xr.merge([ds_temp_wind, ds_precip])
    
print("Data loading complete.")
print("Variables in dataset:", ds.data_vars)
# Convert ERA5 temperature from Kelvin (K) to Celsius (C)
ds['t2m_c'] = ds['t2m'] - 273.15 
# Convert precipitation from [m] to [mm]
ds['tp'] = ds['tp'] * 1000  

# ----------------- Target Location Configuration -----------------
# Example: A location near Wellington, New Zealand
TARGET_LAT = -41.3  # South Latitude
TARGET_LON = 174.7 # East Longitude

# Calculate wind speed (WS) using U (u10) and V (v10) components
ds['wind_speed'] = np.sqrt(ds['u10']**2 + ds['v10']**2)

# Extract data for the grid point closest to the target location
target_point = ds.sel(latitude=TARGET_LAT, longitude=TARGET_LON, method='nearest')

# Get hourly temperature and wind speed
hourly_temp = target_point['t2m_c'].to_series()
hourly_wind = target_point['wind_speed'].to_series()

# Organize monthly temperature distribution into a DataFrame (preparation for violin plot)
temp_df = hourly_temp.rename('Temperature').to_frame()
temp_df['Month'] = temp_df.index.month_name()

# Call the violin plot function
plot_results.plot_monthly_temperature_violin(temp_df, TARGET_LAT, TARGET_LON, output_dir="plots", filename="monthly_temperature_violin.png")

# Calculate mean temperature over the 'time' dimension.
with dask.diagnostics.ProgressBar():
    # Corrected dimension from 'valid_time' to 'time'
    annual_mean_temp = ds['t2m_c'].mean(dim='time').load()

print("Annual mean temperature calculation complete.")

# Calculate total precipitation over the 'time' dimension.
with dask.diagnostics.ProgressBar():
    # Corrected dimension from 'valid_time' to 'time'
    annual_total_precip = ds['tp'].sum(dim='time').load()

print("Annual total precipitation calculation complete.")

# Call the map plot function from plot_results.py
# Assuming the year is 2024 from the filenames
plot_results.plot_annual_mean_temperature_map(annual_mean_temp, 2024, output_dir="plots", filename="annual_mean_temperature_map.png")
