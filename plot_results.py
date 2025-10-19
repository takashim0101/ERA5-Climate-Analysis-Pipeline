
import os
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs

def plot_monthly_temperature_violin(temp_df, lat, lon, output_dir="plots", filename="monthly_temperature_violin.png"):
    """
    Generates and saves a violin plot of monthly temperature distributions.

    Args:
        temp_df (pd.DataFrame): DataFrame with 'Temperature' and 'Month' columns.
        lat (float): Latitude of the target location.
        lon (float): Longitude of the target location.
        output_dir (str): Directory to save the plot.
        filename (str): Name of the output file.
    """
    print(f"Generating monthly temperature violin plot for {lat}, {lon}...")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']

    plt.figure(figsize=(14, 8))
    sns.violinplot(x='Month', y='Temperature', data=temp_df, order=month_order, inner='quartile')
    plt.title(f"Monthly Temperature Distribution at Lat: {lat}, Lon: {lon}")
    plt.ylabel("Temperature (C)")
    plt.xlabel("Month")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Violin plot saved to: {output_path}")

def plot_annual_mean_temperature_map(mean_temp_da, year, output_dir="plots", filename="annual_mean_temperature_map.png"):
    """
    Generates and saves a map of the annual mean temperature.

    Args:
        mean_temp_da (xr.DataArray): DataArray of annual mean temperature with lat/lon coords.
        year (int): The year of the data being plotted.
        output_dir (str): Directory to save the plot.
        filename (str): Name of the output file.
    """
    print(f"Generating annual mean temperature map for {year}...")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Plot the data
    mean_temp_da.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis', 
                                 cbar_kwargs={'label': 'Mean Temperature (C)'})
    
    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    
    plt.title(f"Annual Mean Temperature for {year}")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Map plot saved to: {output_path}")
