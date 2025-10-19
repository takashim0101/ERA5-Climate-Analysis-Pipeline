import cdsapi
import os

dataset = "reanalysis-era5-single-levels"
output_dir = "downloaded_data"

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Base request parameters common to all downloads
base_request_params = {
    "product_type": "reanalysis",
    "year": "2024",
    "day": [
        "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12", "13", "14", "15", "16", "17", "18",
        "19", "20", "21", "22", "23", "24", "25", "26", "27",
        "28", "29", "30", "31"
    ],
    "time": [
        "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
    ],
    "format": "netcdf",
    "area": [-30, 165, -50, 180]
}

# Define variables for temperature/wind and precipitation
temp_wind_variables = [
    "2m_temperature",            
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
]
precip_variables = [
    "total_precipitation"
]

months = [
    "01", "02", "03", "04", "05", "06",
    "07", "08", "09", "10", "11", "12"
]

client = cdsapi.Client()

for month in months:
    # --- Request 1: Temperature and Wind ---
    request_temp_wind = base_request_params.copy()
    request_temp_wind["month"] = month
    request_temp_wind["variable"] = temp_wind_variables
    
    target_file_temp_wind = os.path.join(output_dir, f"era5_2024_{month}_temp_wind.nc")
    
    print(f"Requesting Temperature and Wind data for month: {month}")
    client.retrieve(
        dataset,
        request_temp_wind,
        target_file_temp_wind
    )
    print(f"Successfully downloaded {target_file_temp_wind}")

    # --- Request 2: Precipitation ---
    request_precip = base_request_params.copy()
    request_precip["month"] = month
    request_precip["variable"] = precip_variables
    
    target_file_precip = os.path.join(output_dir, f"era5_2024_{month}_precip.nc")
    
    print(f"Requesting Precipitation data for month: {month}")
    client.retrieve(
        dataset,
        request_precip,
        target_file_precip
    )
    print(f"Successfully downloaded {target_file_precip}")

print("All downloads complete.")