import xarray as xr
import glob
import os

print("--- Starting Debug Script ---")

try:
    # --- Data Loading and Debugging ---
    temp_wind_files = glob.glob("downloaded_data/era5_2024_*_temp_wind.nc")
    precip_files = glob.glob("downloaded_data/era5_2024_*_precip.nc")

    print(f"Found {len(temp_wind_files)} temp/wind files.")
    print(f"Found {len(precip_files)} precip files.")

    # Load and print the structure of the first dataset
    print("\n--- Loading ds_temp_wind ---")
    ds_temp_wind = xr.open_mfdataset(temp_wind_files, combine='by_coords')
    print(ds_temp_wind)
    print("-" * 30)

    # Load and print the structure of the second dataset
    print("\n--- Loading ds_precip ---")
    ds_precip = xr.open_mfdataset(precip_files, combine='by_coords')
    print(ds_precip)
    print("-" * 30)

    # Merge and print the structure of the final dataset
    print("\n--- Merging datasets into era5_ds ---")
    era5_ds = xr.merge([ds_temp_wind, ds_precip])
    print(era5_ds)
    print("-" * 30)

    print("\n--- Checking Coordinates of final merged dataset ---")
    print(era5_ds.coords)
    print("-" * 30)

    print("\nDebug script finished successfully.")

except Exception as e:
    import traceback
    print(f"\nAn error occurred during debugging: {e}")
    traceback.print_exc()
