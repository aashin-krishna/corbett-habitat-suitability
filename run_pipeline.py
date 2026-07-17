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
