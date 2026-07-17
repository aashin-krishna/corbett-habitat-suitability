import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import geopandas as gpd
import rasterio

# High-quality color palette for HSI classes
SUITABILITY_COLORS = [
    "#d73027",  # Class 1: Unsuitable (Vibrant Red)
    "#fc8d59",  # Class 2: Low (Soft Orange)
    "#fee08b",  # Class 3: Moderate (Creamy Yellow)
    "#91cf60",  # Class 4: High (Lime Green)
    "#1a9850"   # Class 5: Very High (Deep Forest Green)
]

def add_scale_bar(ax, bounds, length_km=10, height_m=600):
    """
    Draws a professional alternating black-and-white scale bar on the map axes.
    Coordinates are in UTM meters.
    """
    total_length_m = length_km * 1000
    half_len_m = total_length_m / 2
    
    # Position in the bottom-right corner, inset by some margin
    margin_x = 4000
    margin_y = 4000
    x_anchor = bounds.right - total_length_m - margin_x
    y_anchor = bounds.bottom + margin_y
    
    # Block 1 (Left): White with black border (0 to half_len)
    rect1 = Rectangle(
        (x_anchor, y_anchor), 
        half_len_m, 
        height_m, 
        facecolor='white', 
        edgecolor='black', 
        linewidth=1
    )
    # Block 2 (Right): Black (half_len to total_len)
    rect2 = Rectangle(
        (x_anchor + half_len_m, y_anchor), 
        half_len_m, 
        height_m, 
        facecolor='black', 
        edgecolor='black', 
        linewidth=1
    )
    
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    # Scale text labels (slightly below the scale bar)
    text_y = y_anchor - (height_m * 1.5)
    ax.text(x_anchor, text_y, "0", ha='center', va='top', fontsize=9, fontweight='medium')
    ax.text(x_anchor + half_len_m, text_y, f"{int(length_km/2)}", ha='center', va='top', fontsize=9, fontweight='medium')
    ax.text(x_anchor + total_length_m, text_y, f"{length_km} km", ha='center', va='top', fontsize=9, fontweight='medium')
    
    # Scale bar title (slightly above the scale bar)
    ax.text(x_anchor + half_len_m, y_anchor + (height_m * 1.5), "SCALE", ha='center', va='bottom', fontsize=8, fontweight='bold')

def plot_publication_map(raster_path, aoi_path, output_path, title="Habitat Suitability Map of Jim Corbett National Park"):
    """
    Generates a publication-grade map containing the suitability raster, AOI boundary,
    legend, north arrow, scale bar, gridlines, and dataset credits.
    Saves the figure at 300 DPI.
    """
    # 1. Load data
    with rasterio.open(raster_path) as src:
        raster_data = src.read(1)
        bounds = src.bounds
        crs_str = str(src.crs)
        transform = src.transform
        
    # Mask out nodata values (e.g. background)
    raster_data_masked = np.where(np.isnan(raster_data), np.nan, raster_data)
    
    aoi_gdf = gpd.read_file(aoi_path)
    # Reproject AOI boundary to match the raster CRS
    with rasterio.open(raster_path) as src:
        aoi_proj = aoi_gdf.to_crs(src.crs)
        
    # 2. Setup Plot
    fig, ax = plt.subplots(figsize=(10, 11), dpi=300)
    
    # Create custom ListedColormap
    cmap = ListedColormap(SUITABILITY_COLORS)
    cmap.set_bad(color='none')  # Transparent background for NaNs
    
    # Plot raster data using coordinate extent
    img = ax.imshow(
        raster_data_masked,
        cmap=cmap,
        extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
        vmin=1,
        vmax=5,
        zorder=1
    )
    
    # Plot AOI boundary shapefile
    aoi_proj.boundary.plot(
        ax=ax,
        color='black',
        linewidth=1.5,
        linestyle='-',
        zorder=2
    )
    
    # 3. Add Grid and Coordinates
    ax.grid(True, which='both', color='#d3d3d3', linestyle='--', linewidth=0.5, alpha=0.7, zorder=3)
    ax.ticklabel_format(style='plain', useOffset=False)
    ax.set_xlabel("Easting (m) - UTM Zone 44N", fontsize=10, fontweight='bold', labelpad=8)
    ax.set_ylabel("Northing (m)", fontsize=10, fontweight='bold', labelpad=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    
    # Set plot display window to bounds
    ax.set_xlim(bounds.left, bounds.right)
    ax.set_ylim(bounds.bottom, bounds.top)
    
    # 4. Add Legend
    legend_patches = [
        mpatches.Patch(color=SUITABILITY_COLORS[0], label="Unsuitable (Class 1)"),
        mpatches.Patch(color=SUITABILITY_COLORS[1], label="Low (Class 2)"),
        mpatches.Patch(color=SUITABILITY_COLORS[2], label="Moderate (Class 3)"),
        mpatches.Patch(color=SUITABILITY_COLORS[3], label="High (Class 4)"),
        mpatches.Patch(color=SUITABILITY_COLORS[4], label="Very High (Class 5)"),
        mpatches.Patch(fill=False, edgecolor='black', linewidth=1.5, label="AOI Boundary")
    ]
    ax.legend(
        handles=legend_patches,
        loc='lower left',
        frameon=True,
        facecolor='white',
        framealpha=0.9,
        edgecolor='#b0b0b0',
        fontsize=9,
        title="Suitability Category",
        title_fontsize=10,
        borderpad=0.8,
        labelspacing=0.6
    )
    
    # 5. Add Scale Bar
    add_scale_bar(ax, bounds, length_km=10, height_m=500)
    
    # 6. Add North Arrow (Inset Compass Indicator)
    # Positions are relative to the axes fraction (0 to 1)
    x_arrow, y_arrow = 0.95, 0.95
    ax.annotate(
        'N', 
        xy=(x_arrow, y_arrow), 
        xytext=(x_arrow, y_arrow - 0.05),
        arrowprops=dict(facecolor='black', width=3, headwidth=10, headlength=10),
        ha='center', 
        va='center', 
        fontsize=12, 
        fontweight='bold',
        xycoords='axes fraction', 
        bbox=dict(boxstyle='circle,pad=0.25', fc='white', ec='#b0b0b0', alpha=0.8)
    )
    
    # 7. Add Title and Metadata Block
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    
    metadata_text = (
        "Projection: WGS 84 / UTM Zone 44N (EPSG:32644)\n"
        "Data Sources: Sentinel-2 (ESA), Dynamic World (WRI/Google), ALOS PALSAR DEM (JAXA)"
    )
    # Placing info text at the bottom left inset
    props = dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#d3d3d3', alpha=0.8)
    ax.text(
        0.02, 0.98, 
        metadata_text, 
        transform=ax.transAxes, 
        fontsize=8, 
        verticalalignment='top', 
        bbox=props,
        fontstyle='italic'
    )
    
    # 8. Adjust Layout and Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Publication map saved to: {output_path}")
    return output_path

def plot_statistics_chart(df, output_path):
    """
    Generates a publication-grade bar chart showing the area in sq km for each 
    habitat suitability class.
    """
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    
    classes = df["Suitability_Class"].tolist()
    areas = df["Area_SqKm"].tolist()
    percentages = df["Percentage"].tolist()
    
    # Plot bar chart matching the suitability colors
    bars = ax.bar(classes, areas, color=SUITABILITY_COLORS, edgecolor='black', linewidth=0.7, width=0.6)
    
    # Add values on top of each bar
    for bar, pct in zip(bars, percentages):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.0, 
            height + max(areas)*0.01, 
            f"{height:,.1f} km²\n({pct}%)", 
            ha='center', 
            va='bottom', 
            fontsize=9, 
            fontweight='bold'
        )
        
    ax.set_ylabel("Area (square kilometers)", fontsize=11, fontweight='bold', labelpad=10)
    ax.set_title("Habitat Suitability Class Distribution (Jim Corbett National Park)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylim(0, max(areas) * 1.15)  # add space for labels
    
    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', labelsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Statistics chart saved to: {output_path}")
    return output_path
