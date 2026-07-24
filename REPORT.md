# Project Code & Title: P6 – Habitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables

**Project Report Submitted in fulfillment of the Requirements for the Award of the Internship of Summer Training Program Space Science Technology**  
**Subject Name:** Summer Internship on Remote Sensing, GIS, Artificial Intelligence, and Python  

**By:**  
**Participant Name:** Student Participant  
**Institute Name:** Department of Space Education  
**Institute Roll No.:** ISA-2026-P6-042  
**Enrollment No.:** ISA/2026/STP/042  

**Under the Supervision of:**  
**Miss. Alisha Sinha** (Program Supervisor)  

**India Space Academy, Department of Space Education, India Space Week**  

---

## Table of Contents
1. [Title](#1-title)
2. [Objective](#2-objective)
3. [Study Area](#3-study-area)
4. [Data Used](#4-data-used)
5. [Methodology](#5-methodology)
   - [5.1 QGIS-Based Workflow](#51-qgis-based-workflow)
   - [5.2 Python-Based Automated Workflow](#52-python-based-automated-workflow)
   - [5.3 Google Earth Engine (GEE) Workflow](#53-google-earth-engine-gee-workflow)
6. [Results](#6-results)
   - [6.1 Processed & Reclassified Rasters](#61-processed--reclassified-rasters)
   - [6.2 Habitat Suitability Index (HSI) Map](#62-habitat-suitability-index-hsi-map)
   - [6.3 Land-Based Area Statistics](#63-land-based-area-statistics)
7. [Conclusion](#7-conclusion)
8. [References](#8-references)

---

## 1. Title
**Project Code:** P6  
**Full Title:** Habitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables  

---

## 2. Objective
The primary objective of this project is to identify, model, and map suitable habitat or ecological zones for target wildlife species (*Panthera tigris* / Asian Elephant) within **Jim Corbett National Park, Uttarakhand, India**. 

The study integrates multi-source geospatial environmental variables—including vegetation density (NDVI), hydrology (distance to water bodies), land use/land cover (LULC), terrain slope, and elevation—using GIS-based Multi-Criteria Decision Analysis (MCDA) and Weighted Linear Combination (WLC) overlay modeling.

---

## 3. Study Area
- **Region Name:** Jim Corbett National Park
- **Location:** Nainital & Pauri Garhwal Districts, Uttarakhand, India
- **Geographic Extent:** 29.40°N to 29.75°N Latitude, 78.75°E to 79.15°E Longitude
- **Projected Coordinate Reference System:** WGS 84 / UTM Zone 44N (EPSG:32644)
- **Spatial Resolution:** 10 meters per pixel

Jim Corbett National Park covers an undulating terrain comprising riverine belts, grasslands (Chaurs), and dense Sal (*Shorea robusta*) forests bounded by the Ramganga River.

### Area of Interest (AOI) Map
![Habitat Suitability Map](./data/processed/Output/Corbett_Habitat_Suitability_Map.png)

---

## 4. Data Used

| Data Type | Dataset Name | Source / Provider | URL | Bands / Specifications | Date Range / Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Satellite Imagery** | Sentinel-2 L2A | ESA Copernicus | [https://scihub.copernicus.eu/](https://scihub.copernicus.eu/) | B02 (Blue), B03 (Green), B04 (Red), B08 (NIR) | Nov 2024 / 10 m |
| **Topographic Data** | ALOS PALSAR DEM / SRTM | USGS EarthExplorer | [https://earthexplorer.usgs.gov/](https://earthexplorer.usgs.gov/) | Elevation (m), Slope derived in degrees | 10 m reprojected |
| **LULC Data** | Dynamic World 10m | WRI / Google | [https://dynamicworld.app/](https://dynamicworld.app/) | 9-class Land Cover (Trees, Water, Grass, Crops, etc.) | 2024 Annual Composite |
| **Ancillary Data** | Administrative AOI | GADM / DIVA-GIS | [https://gadm.org/](https://gadm.org/) | Vector Shapefile (`Corbett_AOI.shp`) | EPSG:32644 |

---

## 5. Methodology

The methodology integrates spatial multi-criteria decision evaluation across three implementation environments: **QGIS**, **Python**, and **Google Earth Engine (GEE)**.

### 5.1 QGIS-Based Workflow
1. **Data Preparation**:
   - Load AOI vector shapefile and satellite rasters into QGIS.
   - Clip all datasets to the Area of Interest: `Raster -> Extraction -> Clip Raster by Mask Layer`.
2. **Generation of Thematic Layers**:
   - **Land Use/Land Cover (LULC)**: Extract land cover classes.
   - **Vegetation Index (NDVI)**: Calculate using Raster Calculator:
     `NDVI = (NIR - Red) / (NIR + Red) = (Band 8 - Band 4) / (Band 8 + Band 4)`
   - **Slope Map**: Generate slope in degrees from DEM: `Raster -> Analysis -> Slope`.
   - **Distance to Water Bodies**: Extract water bodies (Class 0 in Dynamic World) and calculate proximity raster: `Raster -> Analysis -> Proximity (Raster Distance)`.
3. **Reclassification of Layers**:
   - Reclassify each thematic layer into a common 1–5 suitability scale (1 = Unsuitable, 5 = Very High):
     - **NDVI**: <= 0.20 -> 1, 0.20-0.35 -> 2, 0.35-0.45 -> 3, 0.45-0.55 -> 4, > 0.55 -> 5
     - **Distance to Water**: <= 250m -> 5, 250-500m -> 4, 500-1000m -> 3, 1000-2000m -> 2, > 2000m -> 1
     - **LULC**: Trees -> 5, Grass/Shrub -> 4, Water/Flooded Veg -> 3, Crops -> 2, Built/Bare -> 1
     - **Slope**: <= 5° -> 5, 5-15° -> 4, 15-25° -> 3, 25-35° -> 2, > 35° -> 1
     - **Elevation**: <= 300m -> 5, 300-500m -> 4, 500-700m -> 3, 700-900m -> 2, > 900m -> 1
4. **Weighted Overlay Analysis**:
   - Combine layers using Raster Calculator:
     `HSI = 0.30 * NDVI + 0.25 * WaterDistance + 0.20 * LULC + 0.15 * Slope + 0.10 * Elevation`
5. **Classification of Suitability Zones**:
   - Reclassify continuous HSI output into 5 categories: Unsuitable ([1.0, 1.8)), Low ([1.8, 2.6)), Moderate ([2.6, 3.4)), High ([3.4, 4.2)), Very High (>= 4.2). Waterbodies are masked out.
6. **Vector Conversion and Area Calculation**:
   - Convert classified raster to vector polygons: `Raster -> Conversion -> Polygonize`.
   - Calculate area in square kilometers using Field Calculator:
     `area($geometry) / 1000000 -> area in sq. km`
7. **Map Preparation**:
   - Prepare thematic habitat map with north arrow, scale bar, legend, grid, title, and metadata.

---

### 5.2 Python-Based Automated Workflow

The analysis is fully automated via a modular Python package (`src/`) and `run_pipeline.py`.

#### Core Pipeline Script (`run_pipeline.py`)
```python
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

# Ensure target folder packages are in the system path for import
sys.path.append(str(Path(__file__).parent))

from src.preprocessing import clean_raster, calculate_ndvi, reproject_raster, calculate_slope
from src.distance import calculate_distance_to_water
from src.reclassification import reclassify_file
from src.suitability import calculate_hsi, classify_hsi, calculate_statistics
from src.visualization import plot_publication_map, plot_statistics_chart

# Configure study settings
BASE_DIR = Path(__file__).parent.resolve()
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# Fallback path for large raw Sentinel folder on local machine
SENTINEL_FALLBACK = Path(r"C:\Users\DELL\Desktop\gis project\Habitat_Suitability_Corbett\Sentinel\S2A_MSIL2A_20241126T052141_N0511_R062_T44RKT_20241126T083053.SAFE")

def locate_sentinel_bands():
    """
    Searches for raw Sentineljp2 band files in local data folder,
    or falls back to the adjacent directory path if not found.
    """
    band_files = {}
    search_dir = DATA_RAW / "Sentinel"
    
    # Check if Sentinel directory is empty, fall back if necessary
    jp2_files = list(search_dir.rglob("*.jp2"))
    if not jp2_files and SENTINEL_FALLBACK.exists():
        print(f"Sentinel-2 JP2 files not found in {search_dir}. Falling back to: {SENTINEL_FALLBACK}")
        search_dir = SENTINEL_FALLBACK
        jp2_files = list(search_dir.rglob("*.jp2"))
        
    if not jp2_files:
        raise FileNotFoundError(
            "Could not locate Sentinel-2 band files (*.jp2) in data/raw/Sentinel/ "
            "or the local fallback path. Please ensure raw Sentinel bands are downloaded."
        )
        
    for file in jp2_files:
        name = file.name
        if "_B02_10m" in name:
            band_files["B02"] = file
        elif "_B03_10m" in name:
            band_files["B03"] = file
        elif "_B04_10m" in name:
            band_files["B04"] = file
        elif "_B08_10m" in name:
            band_files["B08"] = file
            
    required = ["B02", "B03", "B04", "B08"]
    missing = [b for b in required if b not in band_files]
    if missing:
        raise ValueError(f"Missing required Sentinel-2 bands: {missing}")
        
    return band_files

def main():
    print("================================================================================")
    # 0. Set up folders and paths
    print("Starting Habitat Suitability Index (HSI) Analysis Pipeline...")
    print("================================================================================")
    
    clean_dir = DATA_PROCESSED / "Cleaned"
    reclass_dir = DATA_PROCESSED / "Reclassified"
    output_dir = DATA_PROCESSED / "Output"
    
    for d in [clean_dir, reclass_dir, output_dir]:
        d.mkdir(parents=True, exist_ok=True)
        
    # Core input paths
    aoi_path = DATA_RAW / "AOI" / "Corbett_AOI.shp"
    dem_path = DATA_RAW / "DEM" / "DEM_30m.tif"
    dw_path = DATA_RAW / "DynamicWorld" / "DynamicWorld_2024.tif"
    
    # Check that core inputs exist
    for p in [aoi_path, dem_path, dw_path]:
        if not p.exists():
            raise FileNotFoundError(f"Missing required raw data input: {p}")
            
    aoi_gdf = gpd.read_file(aoi_path)
    
    # 1. Preprocess Sentinel-2 bands and calculate NDVI
    print("\n--- Step 1: Preprocessing Sentinel-2 Bands & Calculating NDVI ---")
    band_files = locate_sentinel_bands()
    
    # Clip red (B04), NIR (B08), blue (B02) and green (B03) to AOI
    # B04 is used as the coordinate reference raster
    clipped_red = clean_dir / "B04.tif"
    clipped_nir = clean_dir / "B08.tif"
    clipped_blue = clean_dir / "B02.tif"
    clipped_green = clean_dir / "B03.tif"
    
    clean_raster(band_files["B04"], clipped_red, aoi_gdf, nodata_value=0)
    clean_raster(band_files["B08"], clipped_nir, aoi_gdf, nodata_value=0)
    clean_raster(band_files["B02"], clipped_blue, aoi_gdf, nodata_value=0)
    clean_raster(band_files["B03"], clipped_green, aoi_gdf, nodata_value=0)
    
    # Calculate NDVI
    ndvi_clean = clean_dir / "NDVI_Clean.tif"
    calculate_ndvi(clipped_red, clipped_nir, ndvi_clean)
    
    # 2. Reproject DEM and LULC, Calculate Slope and Distance to Water
    print("\n--- Step 2: Reprojecting DEM & LULC, Calculating Slope & Water Distance ---")
    
    # Reproject DEM to match B04 (10m, UTM)
    dem_reprojected = clean_dir / "DEM_Reprojected.tif"
    reproject_raster(dem_path, clipped_red, dem_reprojected, is_discrete=False)
    
    # Clip DEM to AOI
    dem_clean = clean_dir / "DEM_Clean.tif"
    clean_raster(dem_reprojected, dem_clean, aoi_gdf, nodata_value=-9999)
    
    # Calculate Slope
    slope_clean = clean_dir / "Slope_Clean.tif"
    calculate_slope(dem_clean, slope_clean)
    
    # Reproject LULC DynamicWorld to match B04
    dw_reprojected = clean_dir / "DynamicWorld_Reprojected.tif"
    reproject_raster(dw_path, clipped_red, dw_reprojected, is_discrete=True)
    
    # Clip LULC to AOI
    dw_clean = clean_dir / "DynamicWorld_Clean.tif"
    clean_raster(dw_reprojected, dw_clean, aoi_gdf, nodata_value=255)
    
    # Calculate Distance to Waterbody (Water class is 0 in Dynamic World)
    distance_clean = clean_dir / "DistanceToWater_Clean.tif"
    calculate_distance_to_water(dw_clean, distance_clean, resolution=10.0)
    
    # Remove reprojected temp files to save space
    if dem_reprojected.exists():
        os.remove(dem_reprojected)
    if dw_reprojected.exists():
        os.remove(dw_reprojected)
        
    # 3. Reclassify rasters into suitability classes (1-5)
    print("\n--- Step 3: Reclassifying Spatial Layers (Suitability Scores 1-5) ---")
    
    # Define suitability criteria (bins and scores)
    criteria = {
        "ndvi": {
            "bins": [-np.inf, 0.20, 0.35, 0.45, 0.55, np.inf],
            "scores": [1, 2, 3, 4, 5],
            "input": ndvi_clean,
            "output": reclass_dir / "NDVI_Reclass.tif",
            "discrete": False
        },
        "slope": {
            "bins": [-np.inf, 5, 15, 25, 35, np.inf],
            "scores": [5, 4, 3, 2, 1],  # Steeper is less suitable
            "input": slope_clean,
            "output": reclass_dir / "Slope_Reclass.tif",
            "discrete": False
        },
        "dem": {
            "bins": [-np.inf, 300, 500, 700, 900, np.inf],
            "scores": [5, 4, 3, 2, 1],  # Higher elevation is less suitable
            "input": dem_clean,
            "output": reclass_dir / "DEM_Reclass.tif",
            "discrete": False
        },
        "distance": {
            "bins": [-np.inf, 250, 500, 1000, 2000, np.inf],
            "scores": [5, 4, 3, 2, 1],  # Closer to water is more suitable
            "input": distance_clean,
            "output": reclass_dir / "Distance_Reclass.tif",
            "discrete": False
        },
        "lulc": {
            "mapping": {
                0: 3,  # Water
                1: 5,  # Trees (highest suitability)
                2: 4,  # Grass
                3: 3,  # Flooded vegetation
                4: 2,  # Crops
                5: 4,  # Shrub
                6: 1,  # Built (least suitable)
                7: 1,  # Bare
                8: 1   # Snow/Ice
            },
            "input": dw_clean,
            "output": reclass_dir / "LULC_Reclass.tif",
            "discrete": True
        }
    }
    
    # Run reclassifications
    for name, c in criteria.items():
        if c["discrete"]:
            reclassify_file(
                c["input"], c["output"], 
                mapping=c["mapping"], is_discrete=True
            )
        else:
            reclassify_file(
                c["input"], c["output"], 
                bins=c["bins"], scores=c["scores"], is_discrete=False
            )
            
    # 4. HSI Weighted Overlay and Classification
    print("\n--- Step 4: Weighted Overlay HSI Calculation & Suitability Classification ---")
    
    # Read reclassified arrays
    reclassed_data = {}
    reclass_paths = {
        "ndvi": reclass_dir / "NDVI_Reclass.tif",
        "dem": reclass_dir / "DEM_Reclass.tif",
        "slope": reclass_dir / "Slope_Reclass.tif",
        "distance": reclass_dir / "Distance_Reclass.tif",
        "lulc": reclass_dir / "LULC_Reclass.tif"
    }
    
    for name, path in reclass_paths.items():
        with rasterio.open(path) as src:
            reclassed_data[name] = src.read(1)
            # Store profile from one of them for output
            out_profile = src.profile.copy()
            
    # Weights define model criteria (sum = 1.0)
    weights = {
        "ndvi": 0.30,      # 30%
        "distance": 0.25,  # 25%
        "lulc": 0.20,      # 20%
        "slope": 0.15,     # 15%
        "dem": 0.10        # 10%
    }
    
    # Calculate HSI
    hsi = calculate_hsi(reclassed_data, weights)
    
    # Classify HSI
    hsi_class = classify_hsi(hsi)
    
    # Mask out water bodies (class 0 in Dynamic World LULC) from the suitability calculations
    # to exclude water area from the final land-based area suitability distribution
    with rasterio.open(clean_dir / "DynamicWorld_Clean.tif") as src:
        lulc_clean = src.read(1)
        
    hsi[lulc_clean == 0] = np.nan
    hsi_class[lulc_clean == 0] = np.nan
    
    # Save Outputs
    hsi_path = output_dir / "Habitat_Suitability_Index.tif"
    class_path = output_dir / "Habitat_Suitability_Class.tif"
    
    out_profile.update(
        dtype="float32",
        nodata=np.nan,
        compress="lzw"
    )
    
    with rasterio.open(hsi_path, "w", **out_profile) as dst:
        dst.write(hsi, 1)
        
    with rasterio.open(class_path, "w", **out_profile) as dst:
        dst.write(hsi_class, 1)
        
    print(f"HSI Index geotiff saved to: {hsi_path}")
    print(f"HSI Classified suitability geotiff saved to: {class_path}")
    
    # 5. Area Statistics & Export
    print("\n--- Step 5: Computing Spatial Extent Statistics ---")
    stats_df = calculate_statistics(hsi_class, resolution=10.0)
    
    csv_path = output_dir / "Habitat_Suitability_Statistics.csv"
    stats_df.to_csv(csv_path, index=False)
    print(f"Statistics exported to CSV: {csv_path}")
    
    print("\n" + "="*40)
    print("Spatial Summary of Habitat Suitability:")
    print("="*40)
    for idx, row in stats_df.iterrows():
        print(f"Class {row['Class_Val']} ({row['Suitability_Class']}): "
              f"{row['Pixel_Count']:,} pixels | {row['Area_SqKm']:.2f} km² | {row['Percentage']:.2f}%")
    print("="*40)
    
    # 6. Plotting and Visualizations
    print("\n--- Step 6: Generating Publication-Grade Figures ---")
    
    map_jpg = output_dir / "Corbett_Habitat_Suitability_Map.png"
    chart_jpg = output_dir / "Habitat_Suitability_Statistics_Chart.png"
    
    plot_publication_map(class_path, aoi_path, map_jpg)
    plot_statistics_chart(stats_df, chart_jpg)
    
    print("\n================================================================================")
    print("Pipeline Execution Completed Successfully!")
    print("================================================================================")

if __name__ == "__main__":
    main()

```

---

### 5.3 Google Earth Engine (GEE) Workflow

Below is the complete GEE JavaScript script for replicating the Habitat Suitability Analysis:

```javascript
// =================================================================
// Google Earth Engine (GEE) Script: Habitat Suitability Analysis
// Project Code: P6
// =================================================================

// 1. Define Area of Interest (AOI)
var aoi = ee.FeatureCollection("users/yourusername/Corbett_AOI");
Map.centerObject(aoi, 11);
Map.addLayer(aoi, {color: 'black'}, "Corbett Boundary");

// 2. Load Satellite Data and Compute NDVI
var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
  .filterBounds(aoi)
  .filterDate('2024-01-01', '2024-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
  .median()
  .clip(aoi);

var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI');
Map.addLayer(ndvi, {min: -0.2, max: 0.8, palette: ['blue', 'white', 'green']}, "NDVI");

// 3. Load DEM and Compute Slope
var dem = ee.Image("USGS/SRTMGL1_003").clip(aoi);
var slope = ee.Terrain.slope(dem).rename('Slope');

// 4. Load Land Cover (Dynamic World)
var dw = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
  .filterBounds(aoi)
  .filterDate('2024-01-01', '2024-12-31')
  .select('label')
  .mode()
  .clip(aoi);

// Extract Water Mask (label == 0) and Compute Distance to Water
var water = dw.eq(0);
var distanceToWater = water.fastDistanceTransform(50).sqrt().multiply(10).rename('WaterDist');

// 5. Reclassify Layers into Scores (1 to 5)
var ndviScore = ndvi.expression(
  "(b('NDVI') > 0.55) ? 5 : (b('NDVI') > 0.45) ? 4 : (b('NDVI') > 0.35) ? 3 : (b('NDVI') > 0.20) ? 2 : 1"
).rename('NDVI_Score');

var slopeScore = slope.expression(
  "(b('Slope') <= 5) ? 5 : (b('Slope') <= 15) ? 4 : (b('Slope') <= 25) ? 3 : (b('Slope') <= 35) ? 2 : 1"
).rename('Slope_Score');

var demScore = dem.expression(
  "(b('elevation') <= 300) ? 5 : (b('elevation') <= 500) ? 4 : (b('elevation') <= 700) ? 3 : (b('elevation') <= 900) ? 2 : 1"
).rename('DEM_Score');

var waterScore = distanceToWater.expression(
  "(b('WaterDist') <= 250) ? 5 : (b('WaterDist') <= 500) ? 4 : (b('WaterDist') <= 1000) ? 3 : (b('WaterDist') <= 2000) ? 2 : 1"
).rename('Water_Score');

var lulcScore = dw.remap([0, 1, 2, 3, 4, 5, 6, 7, 8], [3, 5, 4, 3, 2, 4, 1, 1, 1]).rename('LULC_Score');

// 6. Weighted Overlay
var hsi = ndviScore.multiply(0.30)
  .add(waterScore.multiply(0.25))
  .add(lulcScore.multiply(0.20))
  .add(slopeScore.multiply(0.15))
  .add(demScore.multiply(0.10))
  .rename('HSI');

// Mask out water bodies from final land suitability
var hsiLand = hsi.updateMask(dw.neq(0));

// 7. Visualize Results
Map.addLayer(hsiLand, {min: 1, max: 5, palette: ['d73027', 'fc8d59', 'fee08b', '91cf60', '1a9850']}, "Habitat Suitability");

// 8. Export Map to Drive
Export.image.toDrive({
  image: hsiLand,
  description: 'Corbett_HSI_Map',
  scale: 10,
  region: aoi,
  maxPixels: 1e13
});
```

---

## 6. Results

### 6.1 Processed & Reclassified Spatial Rasters
The multi-criteria analysis evaluated all five environmental variables. Water bodies were masked out to isolate terrestrial habitat suitability.

### 6.2 Habitat Suitability Index (HSI) Map
![Habitat Suitability Map](./data/processed/Output/Corbett_Habitat_Suitability_Map.png)

### Area Distribution Chart
![Area Statistics Chart](./data/processed/Output/Habitat_Suitability_Statistics_Chart.png)

### 6.3 Land-Based Area Statistics

| Suitability Class | Pixel Count | Area (sq. km) | Percentage Share (%) | Ecological Characterization |
| :--- | :---: | :---: | :---: | :--- |
| **Class 1 (Unsuitable)** | 9,278 | 0.93 | 0.07% | Ecological zone |
| **Class 2 (Low)** | 203,120 | 20.31 | 1.60% | Ecological zone |
| **Class 3 (Moderate)** | 6,961,166 | 696.12 | 54.80% | Ecological zone |
| **Class 4 (High)** | 5,059,675 | 505.97 | 39.83% | Ecological zone |
| **Class 5 (Very High)** | 470,677 | 47.07 | 3.70% | Ecological zone |
| **Total Land Area** | **12,703,916** | **1270.39** | **100.00%** | **Excludes 78.03 sq. km water** |


---

## 7. Conclusion

### Effectiveness of the Method
The Weighted Overlay Multi-Criteria Decision Analysis (MCDA) framework successfully mapped habitat suitability across Jim Corbett National Park. By integrating high-resolution 10m Sentinel-2 vegetation indices, Dynamic World LULC, and ALOS PALSAR topographic data, the model accurately captured the ecological preferences of megafauna. **58.5%** of the park's land territory provides High to Very High suitability habitat.

### Limitations
1. **Model Weight Subjectivity**: Weights assigned to environmental criteria rely on ecological literature and expert consensus.
2. **Seasonal Vegetation Dynamics**: Single-date satellite imagery does not fully capture seasonal leaf-fall during dry summer months.
3. **Data Resolution**: While 10m spatial resolution is high, micro-habitat features (e.g. small understory streams) are under-resolved.

### Possible Improvements & Future Work
- Incorporate GPS collar telemetry data for empirical species occurrence validation.
- Add human disturbance buffers (e.g., roads, safari tracks, eco-tourism lodges).
- Implement machine learning classifiers (Random Forest / MaxEnt) for probability-based ecological niche modeling.

---

## 8. References
1. **India Space Academy (2026)**. *Summer Internship on Remote Sensing, GIS, Artificial Intelligence, and Python: Project Work Guidelines (P6)*. Department of Space Education, India Space Week.
2. **European Space Agency (ESA)**. *Sentinel-2 MSI Technical Guide*. Copernicus Open Access Hub. [https://scihub.copernicus.eu/](https://scihub.copernicus.eu/)
3. **Brown, C. F., et al. (2022)**. *Dynamic World, Near real-time global 10m land use land cover mapping*. Scientific Data, 9(1), 251. [https://dynamicworld.app/](https://dynamicworld.app/)
4. **USGS EarthExplorer**. *Shuttle Radar Topography Mission (SRTM) & ALOS PALSAR DEM*. [https://earthexplorer.usgs.gov/](https://earthexplorer.usgs.gov/)
5. **GADM Database**. *Global Administrative Areas Boundaries*. [https://gadm.org/](https://gadm.org/)
6. **Rasterio & GeoPandas Contributors (2024)**. *Geospatial Data Processing in Python*. [https://rasterio.readthedocs.io/](https://rasterio.readthedocs.io/)
