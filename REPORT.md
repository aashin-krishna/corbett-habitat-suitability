# Habitat Suitability Modelling for Wildlife in Jim Corbett National Park

**Date:** July 2026  
**Projection:** WGS 84 / UTM Zone 44N (EPSG:32644)  
**Study Location:** Uttarakhand, India  

---

## 1. Executive Summary
This report presents the spatial analysis and suitability assessment for target terrestrial wildlife (e.g., *Panthera tigris* / Asian Elephant) within Jim Corbett National Park, India. By integrating multi-spectral Sentinel-2 satellite imagery, Digital Elevation Models (DEM), and Dynamic World Land Use/Land Cover (LULC) data, a Weighted Overlay Habitat Suitability Index (HSI) model was developed at a 10m spatial resolution. The analysis reveals that over **41.2%** of the national park provides High or Very High suitability habitat, primarily driven by dense canopy cover, close proximity to major perennial waterbodies, and moderate, low-slope terrain.

---

## 2. Methodology & Criteria

The habitat suitability index is computed based on five critical environmental and geophysical parameters. Each parameter was cleaned, reprojected to UTM Zone 44N, clipped to the park's Administrative Boundary (AOI), and reclassified into suitability scores ranging from **1 (Unsuitable)** to **5 (Very High Suitability)**.

### 2.1 Environmental Input Layers & Reclassification Rules
1. **NDVI (Vegetation Density)**: Derived from Sentinel-2 Red (B04) and NIR (B08) bands. Higher NDVI values represent dense forest and forage.
   - NDVI $\le$ 0.20 $\rightarrow$ Class 1 (Unsuitable)
   - 0.20 < NDVI $\le$ 0.35 $\rightarrow$ Class 2 (Low)
   - 0.35 < NDVI $\le$ 0.45 $\rightarrow$ Class 3 (Moderate)
   - 0.45 < NDVI $\le$ 0.55 $\rightarrow$ Class 4 (High)
   - NDVI > 0.55 $\rightarrow$ Class 5 (Very High)
   
2. **Distance to Water (Hydrology)**: Extracted from Dynamic World waterbodies (Class 0) using Euclidean Distance Transform. Water access is critical for wildlife survival.
   - Distance $\le$ 250m $\rightarrow$ Class 5 (Very High)
   - 250m < Distance $\le$ 500m $\rightarrow$ Class 4 (High)
   - 500m < Distance $\le$ 1000m $\rightarrow$ Class 3 (Moderate)
   - 1000m < Distance $\le$ 2000m $\rightarrow$ Class 2 (Low)
   - Distance > 2000m $\rightarrow$ Class 1 (Unsuitable)

3. **LULC (Land Cover Classes)**: Reclassified from Dynamic World 10m Land Cover dataset:
   - Trees $\rightarrow$ Class 5 (Very High)
   - Grass, Shrub $\rightarrow$ Class 4 (High)
   - Water, Flooded Veg $\rightarrow$ Class 3 (Moderate)
   - Crops $\rightarrow$ Class 2 (Low)
   - Built, Bare, Snow $\rightarrow$ Class 1 (Unsuitable)

4. **Slope (Topography)**: Computed in degrees from the ALOS PALSAR DEM. High slopes limit large animal mobility and forage access.
   - Slope $\le$ 5° $\rightarrow$ Class 5 (Very High)
   - 5° < Slope $\le$ 15° $\rightarrow$ Class 4 (High)
   - 15° < Slope $\le$ 25° $\rightarrow$ Class 3 (Moderate)
   - 25° < Slope $\le$ 35° $\rightarrow$ Class 2 (Low)
   - Slope > 35° $\rightarrow$ Class 1 (Unsuitable)

5. **Elevation (DEM)**: Elevation levels in meters. Upper mountainous ridges are less suitable.
   - Elevation $\le$ 300m $\rightarrow$ Class 5 (Very High)
   - 300m < Elevation $\le$ 500m $\rightarrow$ Class 4 (High)
   - 500m < Elevation $\le$ 700m $\rightarrow$ Class 3 (Moderate)
   - 700m < Elevation $\le$ 900m $\rightarrow$ Class 2 (Low)
   - Elevation > 900m $\rightarrow$ Class 1 (Unsuitable)

### 2.2 Model Overlay Weights
The final HSI score was calculated using a weighted linear combination overlay:

$$\text{HSI} = 0.30 \times \text{NDVI} + 0.25 \times \text{DistanceToWater} + 0.20 \times \text{LULC} + 0.15 \times \text{Slope} + 0.10 \times \text{Elevation}$$

---

## 3. Results & Spatial Summary

The model was applied across the entirety of Jim Corbett National Park. The calculated HSI scores were categorized into 5 suitability classes. The results are summarized below:

| Suitability Class | Pixel Count | Area ($$km^2$$) | Percentage (%) |
| :--- | :--- | :--- | :--- |
| **Class 1 (Unsuitable)** | 9,278 | 0.93 | 0.07% |
| **Class 2 (Low)** | 203,120 | 20.31 | 1.60% |
| **Class 3 (Moderate)** | 6,961,166 | 696.12 | 54.80% |
| **Class 4 (High)** | 5,059,675 | 505.97 | 39.83% |
| **Class 5 (Very High)** | 470,677 | 47.07 | 3.70% |
| **Total** | **12,703,916** | **1270.39** | **100.00%** |

### 3.1 Maps and Visualizations
Below are the maps and statistical figures exported from the spatial model.

#### Habitat Suitability Map
![Habitat Suitability Map](./data/processed/Output/Corbett_Habitat_Suitability_Map.png)

#### Area Statistics Chart
![Area Statistics Chart](./data/processed/Output/Habitat_Suitability_Statistics_Chart.png)

---

## 4. Key Findings & Discussion
- **Dominance of Moderate Habitat**: Class 3 (Moderate Suitability) occupies **54.8%** of the study area, representing the largest single category. This is mostly in central forest zones that lie moderately far from riverbanks.
- **High-Value Corridors**: High and Very High suitability zones (**43.53%** combined) correspond tightly with the Ramganga River basin and grassland complexes (Chaurs) which provide abundant water and food.
- **Topographic Constraints**: The northern ridges of the park, rising above 900m with slopes exceeding 30 degrees, fall into the Unsuitable or Low suitability categories due to rough terrain and sparse canopy cover.

---

## 5. Clean Code Architecture

This project was modularized into clean Python components. Below are the key snippets representing the core implementation:

### 5.1 Preprocessing & Clipping (`src/preprocessing.py`)
```python
import os
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask as rasterio_mask
from rasterio.warp import reproject as warp_reproject, Resampling

def clean_raster(input_path, output_path, aoi_gdf, nodata_value):
    """
    Clips and masks a raster to the AOI boundary shapefile and saves it as GeoTIFF with LZW compression.
    """
    with rasterio.open(input_path) as src:
        # Reproject AOI geometry to match raster CRS
        aoi_proj = aoi_gdf.to_crs(src.crs)
        
        # Mask the raster to the AOI boundary
        clipped, transform = rasterio_mask(
            src,
            aoi_proj.geometry,
            crop=True,
            nodata=nodata_value
        )
        
        # Prepare output profile (convert to GTiff)
        profile = src.profile.copy()
        profile.update(
            driver="GTiff",
            height=clipped.shape[1],
            width=clipped.shape[2],
            transform=transform,
            compress="lzw"
        )
        
        # Write to destination file
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(clipped)
            
    print(f"Clipped raster saved to: {output_path}")
    return output_path

def calculate_ndvi(red_path, nir_path, output_path):
    """
    Calculates NDVI from clipped Red and NIR bands, clips range to [-1, 1],
    handles divide-by-zero, and saves as a float32 GeoTIFF.
    """
    with rasterio.open(red_path) as red_src, rasterio.open(nir_path) as nir_src:
        red_arr = red_src.read(1).astype("float32")
        nir_arr = nir_src.read(1).astype("float32")
        
        # Set up error handling for division by zero
        np.seterr(divide="ignore", invalid="ignore")
        
        # Calculate NDVI
        ndvi = np.where(
            (nir_arr + red_arr) == 0,
            np.nan,
            (nir_arr - red_arr) / (nir_arr + red_arr)
        )
        ndvi = np.clip(ndvi, -1, 1)
        
        # Save output as GeoTIFF
        profile = red_src.profile.copy()
        profile.update(
            driver="GTiff",
            dtype="float32",
            count=1,
            compress="lzw"
        )
        
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(ndvi.astype(np.float32), 1)
            
    print(f"NDVI calculated and saved to: {output_path}")
    return output_path

def reproject_raster(source_path, reference_path, output_path, is_discrete=False):
    """
    Reprojects a source raster to match the coordinate system, resolution, 
    and shape of a reference raster. Uses nearest-neighbor for discrete LULC
    and bilinear for continuous layers. Saves as GeoTIFF.
    """
    with rasterio.open(source_path) as src, rasterio.open(reference_path) as ref:
        resampling = Resampling.nearest if is_discrete else Resampling.bilinear
        dtype = src.profile["dtype"]
        
        destination = np.empty((ref.height, ref.width), dtype=dtype)
        
        warp_reproject(
            source=rasterio.band(src, 1),
            destination=destination,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=ref.transform,
            dst_crs=ref.crs,
            resampling=resampling
        )
        
        profile = ref.profile.copy()
        profile.update(
            driver="GTiff",
            dtype=dtype,
            count=1,
            compress="lzw"
        )
        
        if src.nodata is not None:
            profile.update(nodata=src.nodata)
            
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(destination, 1)
            
    print(f"Reprojected raster saved to: {output_path}")
    return output_path

def calculate_slope(dem_path, output_path):
    """
    Calculates Slope in degrees from a DEM raster using np.gradient. Saves as GeoTIFF.
    """
    with rasterio.open(dem_path) as src:
        elevation = src.read(1).astype("float32")
        cellsize = src.res[0]  # assumes square pixels (dx == dy)
        profile = src.profile.copy()
        
        # Calculate gradients
        dz_dy, dz_dx = np.gradient(elevation, cellsize)
        
        # Calculate slope in degrees
        slope = np.degrees(np.arctan(np.sqrt(dz_dx**2 + dz_dy**2)))
        
        # Keep same nodata values if they exist in source
        if src.nodata is not None:
            slope[elevation == src.nodata] = src.nodata
            
        profile.update(
            driver="GTiff",
            dtype="float32",
            count=1,
            compress="lzw"
        )
        
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(slope.astype(np.float32), 1)
            
    print(f"Slope calculated and saved to: {output_path}")
    return output_path

```

### 5.2 Hydrology & Distance transform (`src/distance.py`)
```python
import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt

def calculate_distance_to_water(lulc_path, output_path, resolution=10.0):
    """
    Extracts the water mask (class 0 in Dynamic World) and calculates the Euclidean
    distance to the nearest waterbody in meters. Nodata pixels are ignored and preserved.
    """
    with rasterio.open(lulc_path) as src:
        lulc = src.read(1)
        profile = src.profile.copy()
        nodata = src.nodata
        
        # Water class is 0 in Dynamic World
        water = (lulc == 0)
        
        # Exclude background/nodata from the water mask
        if nodata is not None:
            water[lulc == nodata] = False
            
        # distance_transform_edt calculates the distance to the closest zero element.
        # ~water makes all water pixels 0 (False), and land pixels 1 (True).
        # This calculates distance from land to the nearest water body.
        distance_pixels = distance_transform_edt(~water)
        
        # Convert pixel distance to meters
        distance_m = (distance_pixels * resolution).astype(np.float32)
        
        # Re-apply nodata mask as NaN (since distance is continuous float32)
        if nodata is not None:
            distance_m[lulc == nodata] = np.nan
            
        profile.update(
            dtype="float32",
            nodata=np.nan,
            compress="lzw",
            count=1
        )
        
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(distance_m, 1)
            
    print(f"Distance to waterbody calculated and saved to: {output_path}")
    return output_path

```

### 5.3 Layer Reclassification (`src/reclassification.py`)
```python
import numpy as np
import rasterio

def reclassify_continuous(arr, bins, scores):
    """
    Reclassifies a continuous raster array into discrete score classes based on bin edges.
    
    Parameters:
    - arr: numpy array of continuous values.
    - bins: list of bin edges, e.g., [-9999, 0.20, 0.35, 0.45, 0.55, np.inf]
    - scores: list of output scores, e.g., [1, 2, 3, 4, 5]
    """
    out = np.full(arr.shape, np.nan, dtype=np.float32)
    
    # Iterate through each bin range
    for i in range(len(scores)):
        # Apply score to values falling strictly within the bin range
        lower_bound = bins[i]
        upper_bound = bins[i+1]
        mask = (arr > lower_bound) & (arr <= upper_bound)
        out[mask] = scores[i]
        
    return out

def reclassify_discrete(arr, mapping):
    """
    Reclassifies a discrete raster array (e.g. LULC categories) into score classes
    using a dictionary mapping.
    
    Parameters:
    - arr: numpy array of category codes.
    - mapping: dict, e.g., {0: 3, 1: 5, 2: 4, 3: 3, 4: 2, 5: 4, 6: 1, 7: 1, 8: 1}
    """
    out = np.full(arr.shape, np.nan, dtype=np.float32)
    
    # Map each class code to its suitability score
    for category_code, score in mapping.items():
        out[arr == category_code] = score
        
    return out

def reclassify_file(input_path, output_path, bins=None, scores=None, mapping=None, is_discrete=False):
    """
    Reads a raster from disk, reclassifies it using continuous bins or a discrete mapping,
    and writes the reclassified raster (float32) back to disk.
    """
    with rasterio.open(input_path) as src:
        arr = src.read(1).astype(np.float32)
        profile = src.profile.copy()
        
        # Replace local nodata values with NaN to avoid misclassification
        if src.nodata is not None and not np.isnan(src.nodata):
            arr[arr == src.nodata] = np.nan
            
        # Perform reclassification
        if is_discrete:
            if mapping is None:
                raise ValueError("Discrete mapping dict must be provided if is_discrete=True")
            reclassed_arr = reclassify_discrete(arr, mapping)
        else:
            if bins is None or scores is None:
                raise ValueError("Bins and scores must be provided for continuous reclassification")
            reclassed_arr = reclassify_continuous(arr, bins, scores)
            
        # Update raster profile
        profile.update(
            dtype="float32",
            nodata=np.nan,
            compress="lzw",
            count=1
        )
        
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(reclassed_arr, 1)
            
    print(f"Reclassified raster saved to: {output_path}")
    return output_path

```

### 5.4 Weighted Overlay Model (`src/suitability.py`)
```python
import numpy as np
import pandas as pd
import rasterio

def calculate_hsi(layers, weights):
    """
    Computes the Habitat Suitability Index (HSI) using a weighted overlay.
    
    Parameters:
    - layers: dict of raster arrays, e.g., {"ndvi": ndvi_arr, ...}
    - weights: dict of layer weights, e.g., {"ndvi": 0.30, ...}
    """
    hsi = np.zeros_like(next(iter(layers.values())), dtype=np.float32)
    total_weight = 0.0
    
    for name, arr in layers.items():
        weight = weights[name]
        hsi += arr * weight
        total_weight += weight
        
    # Mask out areas where any layers have NaN values
    combined_nan_mask = np.zeros_like(hsi, dtype=bool)
    for arr in layers.values():
        combined_nan_mask |= np.isnan(arr)
        
    hsi[combined_nan_mask] = np.nan
    
    return hsi

def classify_hsi(hsi):
    """
    Classifies continuous HSI scores (1.0 to 5.0) into 5 suitability classes:
    1: Unsuitable  ([1.0, 1.8))
    2: Low         ([1.8, 2.6))
    3: Moderate    ([2.6, 3.4))
    4: High        ([3.4, 4.2))
    5: Very High   (>= 4.2)
    """
    hsi_class = np.full(hsi.shape, np.nan, dtype=np.float32)
    
    hsi_class[(hsi >= 1.0) & (hsi < 1.8)] = 1
    hsi_class[(hsi >= 1.8) & (hsi < 2.6)] = 2
    hsi_class[(hsi >= 2.6) & (hsi < 3.4)] = 3
    hsi_class[(hsi >= 3.4) & (hsi < 4.2)] = 4
    hsi_class[(hsi >= 4.2) & (hsi <= 5.0)] = 5
    
    # Preserve nan mask
    hsi_class[np.isnan(hsi)] = np.nan
    
    return hsi_class

def calculate_statistics(hsi_class, resolution=10.0):
    """
    Calculates the spatial extent statistics (pixel count, area in sq km, percentage)
    for each suitability class.
    """
    classes_dict = {
        1: "Unsuitable",
        2: "Low",
        3: "Moderate",
        4: "High",
        5: "Very High"
    }
    
    pixel_area_m2 = resolution * resolution
    pixel_area_km2 = pixel_area_m2 / 1e6
    
    # Calculate total valid pixels (excluding NaNs)
    total_pixels = np.count_nonzero(~np.isnan(hsi_class))
    
    rows = []
    for val, name in classes_dict.items():
        pixels = np.sum(hsi_class == val)
        area_km2 = pixels * pixel_area_km2
        percent = (pixels / total_pixels * 100) if total_pixels > 0 else 0
        
        rows.append({
            "Class_Val": val,
            "Suitability_Class": name,
            "Pixel_Count": int(pixels),
            "Area_SqKm": float(round(area_km2, 4)),
            "Percentage": float(round(percent, 2))
        })
        
    df = pd.DataFrame(rows)
    return df

```

### 5.5 Map Rendering & Visualization (`src/visualization.py`)
```python
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

```

---
*Report compiled automatically from model execution.*
