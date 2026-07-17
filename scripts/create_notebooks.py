import nbformat as nbf
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
NOTEBOOKS_DIR.mkdir(exist_ok=True)

def create_notebook_01():
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell(
            "# Notebook 01: GIS Data Preprocessing & Input Preparation\n\n"
            "This notebook handles the initial preprocessing of spatial layers for the Jim Corbett National Park Habitat Suitability Index (HSI) model. "
            "We will load the study area boundary (AOI), process Sentinel-2 multispectral bands, calculate the Normalized Difference Vegetation Index (NDVI), "
            "and reproject the digital elevation model (DEM) to compute slope.\n\n"
            "## Objectives:\n"
            "1. Read and visualize the Jim Corbett Administrative Boundary (AOI).\n"
            "2. Clip Sentinel-2 bands (Red, NIR, Blue, Green) to the study area.\n"
            "3. Calculate the Normalized Difference Vegetation Index (NDVI).\n"
            "4. Reproject the Digital Elevation Model (DEM) and compute the Slope."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import geopandas as gpd\n"
            "import matplotlib.pyplot as plt\n"
            "import rasterio\n\n"
            "# Configure project paths (allowing imports from src/)\n"
            "NOTEBOOK_DIR = Path(os.getcwd())\n"
            "PROJECT_ROOT = NOTEBOOK_DIR.parent\n"
            "sys.path.append(str(PROJECT_ROOT))\n\n"
            "from src.preprocessing import clean_raster, calculate_ndvi, reproject_raster, calculate_slope\n\n"
            "print('Environment set up successfully!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Load and Visualize the Study Area (AOI)\n\n"
            "We read the Jim Corbett National Park boundary using GeoPandas."
        ),
        nbf.v4.new_code_cell(
            "aoi_path = PROJECT_ROOT / 'data' / 'raw' / 'AOI' / 'Corbett_AOI.shp'\n"
            "aoi = gpd.read_file(aoi_path)\n"
            "print(f'Coordinate Reference System (CRS): {aoi.crs}')\n"
            "aoi.plot(color='lightgreen', edgecolor='black', alpha=0.5)\n"
            "plt.title('Jim Corbett National Park AOI Boundary')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Locate Sentinel-2 Multispectral Data\n\n"
            "We locate the raw Sentinel-2 bands. If they are not in the repository `data/raw/Sentinel/`, "
            "we fall back to the local workspace folder."
        ),
        nbf.v4.new_code_cell(
            "# Locate JP2 band files\n"
            "sentinel_dir = PROJECT_ROOT / 'data' / 'raw' / 'Sentinel'\n"
            "fallback_dir = Path(r'C:\\Users\\DELL\\Desktop\\gis project\\Habitat_Suitability_Corbett\\Sentinel\\S2A_MSIL2A_20241126T052141_N0511_R062_T44RKT_20241126T083053.SAFE')\n\n"
            "jp2_files = list(sentinel_dir.rglob('*.jp2'))\n"
            "if not jp2_files and fallback_dir.exists():\n"
            "    print('Using local workspace fallback directory...')\n"
            "    sentinel_dir = fallback_dir\n"
            "    jp2_files = list(sentinel_dir.rglob('*.jp2'))\n\n"
            "band_files = {}\n"
            "for file in jp2_files:\n"
            "    if '_B02_10m' in file.name: band_files['B02'] = file\n"
            "    elif '_B03_10m' in file.name: band_files['B03'] = file\n"
            "    elif '_B04_10m' in file.name: band_files['B04'] = file\n"
            "    elif '_B08_10m' in file.name: band_files['B08'] = file\n\n"
            "print('Found bands:')\n"
            "for b, p in band_files.items():\n"
            "    print(f' - {b}: {p.name}')"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Clip Sentinel-2 Bands to AOI\n\n"
            "We clip the bands using our modular `clean_raster` function, which handles reprojecting the AOI to the raster CRS."
        ),
        nbf.v4.new_code_cell(
            "clean_dir = PROJECT_ROOT / 'data' / 'processed' / 'Cleaned'\n"
            "clean_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "clipped_red = clean_dir / 'B04.tif'\n"
            "clipped_nir = clean_dir / 'B08.tif'\n"
            "clipped_blue = clean_dir / 'B02.tif'\n"
            "clipped_green = clean_dir / 'B03.tif'\n\n"
            "clean_raster(band_files['B04'], clipped_red, aoi, nodata_value=0)\n"
            "clean_raster(band_files['B08'], clipped_nir, aoi, nodata_value=0)\n"
            "clean_raster(band_files['B02'], clipped_blue, aoi, nodata_value=0)\n"
            "clean_raster(band_files['B03'], clipped_green, aoi, nodata_value=0)\n\n"
            "print('Sentinel bands clipped and saved to data/processed/Cleaned!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Calculate Normalized Difference Vegetation Index (NDVI)\n\n"
            "NDVI evaluates canopy density and biomass: \n\n"
            "$$\\text{NDVI} = \\frac{\\text{NIR} - \\text{Red}}{\\text{NIR} + \\text{Red}}$$"
        ),
        nbf.v4.new_code_cell(
            "ndvi_clean = clean_dir / 'NDVI_Clean.tif'\n"
            "calculate_ndvi(clipped_red, clipped_nir, ndvi_clean)\n\n"
            "# Visualize NDVI\n"
            "with rasterio.open(ndvi_clean) as src:\n"
            "    ndvi_arr = src.read(1)\n"
            "    \n"
            "plt.figure(figsize=(8,8))\n"
            "plt.imshow(ndvi_arr, cmap='RdYlGn', vmin=-0.2, vmax=0.8)\n"
            "plt.colorbar(label='NDVI Value')\n"
            "plt.title('Processed NDVI Layer')\n"
            "plt.axis('off')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Reproject DEM and Calculate Slope\n\n"
            "The raw DEM resolution is 30m. We reproject it to 10m to match the Sentinel grids, clip to the AOI, "
            "and calculate the Slope."
        ),
        nbf.v4.new_code_cell(
            "raw_dem = PROJECT_ROOT / 'data' / 'raw' / 'DEM' / 'DEM_30m.tif'\n"
            "dem_reprojected = clean_dir / 'DEM_Reprojected.tif'\n"
            "dem_clean = clean_dir / 'DEM_Clean.tif'\n"
            "slope_clean = clean_dir / 'Slope_Clean.tif'\n\n"
            "# 1. Reproject\n"
            "reproject_raster(raw_dem, clipped_red, dem_reprojected, is_discrete=False)\n\n"
            "# 2. Clip\n"
            "clean_raster(dem_reprojected, dem_clean, aoi, nodata_value=-9999)\n\n"
            "# 3. Calculate Slope\n"
            "calculate_slope(dem_clean, slope_clean)\n\n"
            "# Remove temporary reprojected file\n"
            "if dem_reprojected.exists():\n"
            "    os.remove(dem_reprojected)\n\n"
            "# Visualize Slope\n"
            "with rasterio.open(slope_clean) as src:\n"
            "    slope_arr = src.read(1)\n"
            "    # Set nodata to NaN for plot\n"
            "    slope_arr[slope_arr == src.nodata] = np.nan\n"
            "    \n"
            "plt.figure(figsize=(8,8))\n"
            "plt.imshow(slope_arr, cmap='YlOrBr', vmin=0, vmax=45)\n"
            "plt.colorbar(label='Slope (degrees)')\n"
            "plt.title('Processed Slope Layer')\n"
            "plt.axis('off')\n"
            "plt.show()"
        )
    ]
    nb['cells'] = cells
    nbf.write(nb, NOTEBOOKS_DIR / "01_data_preprocessing.ipynb")
    print("Notebook 01 created successfully.")

def create_notebook_02():
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell(
            "# Notebook 02: Land Use Land Cover (LULC) & Distance to Water Calculation\n\n"
            "This notebook covers reprojecting and standardizing the Land Use / Land Cover (LULC) dataset, "
            "and calculating the Euclidean distance to waterbodies (critical hydrology layer for HSI).\n\n"
            "## Objectives:\n"
            "1. Reproject and clip Dynamic World LULC layer.\n"
            "2. Extract waterbodies (Class 0 in Dynamic World).\n"
            "3. Compute Euclidean Distance to waterbodies in meters using scipy EDT."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import geopandas as gpd\n"
            "import matplotlib.pyplot as plt\n"
            "import rasterio\n\n"
            "# Configure paths\n"
            "NOTEBOOK_DIR = Path(os.getcwd())\n"
            "PROJECT_ROOT = NOTEBOOK_DIR.parent\n"
            "sys.path.append(str(PROJECT_ROOT))\n\n"
            "from src.preprocessing import clean_raster, reproject_raster\n"
            "from src.distance import calculate_distance_to_water\n\n"
            "print('Environment ready!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Reproject and Clip Dynamic World LULC\n\n"
            "We load the raw 2024 Dynamic World GeoTIFF, reproject it using **nearest-neighbor** resampling "
            "(since land cover categories are discrete integers), and clip it to the park boundary."
        ),
        nbf.v4.new_code_cell(
            "raw_lulc = PROJECT_ROOT / 'data' / 'raw' / 'DynamicWorld' / 'DynamicWorld_2024.tif'\n"
            "clipped_red = PROJECT_ROOT / 'data' / 'processed' / 'Cleaned' / 'B04.tif'\n"
            "aoi_path = PROJECT_ROOT / 'data' / 'raw' / 'AOI' / 'Corbett_AOI.shp'\n"
            "aoi = gpd.read_file(aoi_path)\n\n"
            "dw_reprojected = PROJECT_ROOT / 'data' / 'processed' / 'Cleaned' / 'DynamicWorld_Reprojected.tif'\n"
            "dw_clean = PROJECT_ROOT / 'data' / 'processed' / 'Cleaned' / 'DynamicWorld_Clean.tif'\n\n"
            "# Reproject LULC (discrete=True)\n"
            "reproject_raster(raw_lulc, clipped_red, dw_reprojected, is_discrete=True)\n\n"
            "# Clip LULC to AOI\n"
            "clean_raster(dw_reprojected, dw_clean, aoi, nodata_value=255)\n\n"
            "if dw_reprojected.exists():\n"
            "    os.remove(dw_reprojected)\n\n"
            "# Visualize LULC classes\n"
            "with rasterio.open(dw_clean) as src:\n"
            "    lulc_arr = src.read(1)\n"
            "    \n"
            "plt.figure(figsize=(8,8))\n"
            "plt.imshow(lulc_arr, cmap='tab10', vmin=0, vmax=9)\n"
            "plt.colorbar(label='LULC Category Code')\n"
            "plt.title('Processed LULC (Dynamic World)')\n"
            "plt.axis('off')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Calculate Distance to Waterbody\n\n"
            "Wildlife requires close proximity to water sources. Class 0 in Dynamic World represents water bodies. "
            "We extract this mask, calculate the distance in pixels to the closest water cell, "
            "and multiply by pixel resolution (10m) to get the distance in meters."
        ),
        nbf.v4.new_code_cell(
            "distance_clean = PROJECT_ROOT / 'data' / 'processed' / 'Cleaned' / 'DistanceToWater_Clean.tif'\n"
            "calculate_distance_to_water(dw_clean, distance_clean, resolution=10.0)\n\n"
            "# Visualize Distance to Water\n"
            "with rasterio.open(distance_clean) as src:\n"
            "    dist_arr = src.read(1)\n"
            "    \n"
            "plt.figure(figsize=(8,8))\n"
            "plt.imshow(dist_arr, cmap='viridis')\n"
            "plt.colorbar(label='Distance (meters)')\n"
            "plt.title('Distance to Waterbody')\n"
            "plt.axis('off')\n"
            "plt.show()"
        )
    ]
    nb['cells'] = cells
    nbf.write(nb, NOTEBOOKS_DIR / "02_raster_cleaning_distance.ipynb")
    print("Notebook 02 created successfully.")

def create_notebook_03():
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell(
            "# Notebook 03: Raster Reclassification & Suitability Scoring\n\n"
            "This notebook reclassifies the continuous and discrete spatial variables (NDVI, DEM, Slope, Distance to Water, and LULC) "
            "into integer suitability scores ranging from **1 (Least Suitable)** to **5 (Most Suitable)**.\n\n"
            "## Objectives:\n"
            "1. Implement continuous reclassification functions.\n"
            "2. Implement discrete LULC category reclass mapping.\n"
            "3. Export five reclassified GeoTIFF raster layers."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import rasterio\n\n"
            "# Configure paths\n"
            "NOTEBOOK_DIR = Path(os.getcwd())\n"
            "PROJECT_ROOT = NOTEBOOK_DIR.parent\n"
            "sys.path.append(str(PROJECT_ROOT))\n\n"
            "from src.reclassification import reclassify_file\n\n"
            "print('Environment ready!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Define Reclassification Criteria & Run Scoring\n\n"
            "We establish reclassification bins for continuous variables (NDVI, DEM, Slope, Water Distance) "
            "and a dictionary lookup mapping for LULC classes. We then save the reclassified rasters in `data/processed/Reclassified/`."
        ),
        nbf.v4.new_code_cell(
            "clean_dir = PROJECT_ROOT / 'data' / 'processed' / 'Cleaned'\n"
            "reclass_dir = PROJECT_ROOT / 'data' / 'processed' / 'Reclassified'\n"
            "reclass_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "criteria = {\n"
            "    'ndvi': {\n"
            "        'bins': [-np.inf, 0.20, 0.35, 0.45, 0.55, np.inf],\n"
            "        'scores': [1, 2, 3, 4, 5],\n"
            "        'input': clean_dir / 'NDVI_Clean.tif',\n"
            "        'output': reclass_dir / 'NDVI_Reclass.tif',\n"
            "        'discrete': False\n"
            "    },\n"
            "    'slope': {\n"
            "        'bins': [-np.inf, 5, 15, 25, 35, np.inf],\n"
            "        'scores': [5, 4, 3, 2, 1],  # Steeper is less suitable\n"
            "        'input': clean_dir / 'Slope_Clean.tif',\n"
            "        'output': reclass_dir / 'Slope_Reclass.tif',\n"
            "        'discrete': False\n"
            "    },\n"
            "    'dem': {\n"
            "        'bins': [-np.inf, 300, 500, 700, 900, np.inf],\n"
            "        'scores': [5, 4, 3, 2, 1],  # Higher is less suitable\n"
            "        'input': clean_dir / 'DEM_Clean.tif',\n"
            "        'output': reclass_dir / 'DEM_Reclass.tif',\n"
            "        'discrete': False\n"
            "    },\n"
            "    'distance': {\n"
            "        'bins': [-np.inf, 250, 500, 1000, 2000, np.inf],\n"
            "        'scores': [5, 4, 3, 2, 1],  # Closer is more suitable\n"
            "        'input': clean_dir / 'DistanceToWater_Clean.tif',\n"
            "        'output': reclass_dir / 'Distance_Reclass.tif',\n"
            "        'discrete': False\n"
            "    },\n"
            "    'lulc': {\n"
            "        'mapping': {\n"
            "            0: 3,  # Water\n"
            "            1: 5,  # Trees\n"
            "            2: 4,  # Grass\n"
            "            3: 3,  # Flooded vegetation\n"
            "            4: 2,  # Crops\n"
            "            5: 4,  # Shrub\n"
            "            6: 1,  # Built\n"
            "            7: 1,  # Bare\n"
            "            8: 1   # Snow/Ice\n"
            "        },\n"
            "        'input': clean_dir / 'DynamicWorld_Clean.tif',\n"
            "        'output': reclass_dir / 'LULC_Reclass.tif',\n"
            "        'discrete': True\n"
            "    }\n"
            "}\n\n"
            "for name, c in criteria.items():\n"
            "    if c['discrete']:\n"
            "        reclassify_file(c['input'], c['output'], mapping=c['mapping'], is_discrete=True)\n"
            "    else:\n"
            "        reclassify_file(c['input'], c['output'], bins=c['bins'], scores=c['scores'], is_discrete=False)\n\n"
            "print('All layers successfully reclassified!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Visualize Reclassified Scores\n\n"
            "Let's plot the resulting reclassified rasters to inspect the score distributions (1-5)."
        ),
        nbf.v4.new_code_cell(
            "fig, axes = plt.subplots(2, 3, figsize=(15, 10))\n"
            "layers = [\n"
            "    ('NDVI Reclass', reclass_dir / 'NDVI_Reclass.tif'),\n"
            "    ('DEM Reclass', reclass_dir / 'DEM_Reclass.tif'),\n"
            "    ('Slope Reclass', reclass_dir / 'Slope_Reclass.tif'),\n"
            "    ('Distance Reclass', reclass_dir / 'Distance_Reclass.tif'),\n"
            "    ('LULC Reclass', reclass_dir / 'LULC_Reclass.tif')\n"
            "]\n\n"
            "for idx, (title, path) in enumerate(layers):\n"
            "    ax = axes[idx // 3, idx % 3]\n"
            "    with rasterio.open(path) as src:\n"
            "        arr = src.read(1)\n"
            "        im = ax.imshow(arr, cmap='RdYlGn', vmin=1, vmax=5)\n"
            "        ax.set_title(title)\n"
            "        ax.axis('off')\n"
            "        \n"
            "# Turn off the empty last subplot\n"
            "axes[1, 2].axis('off')\n"
            "fig.colorbar(im, ax=axes.ravel().tolist()[:5], label='Suitability Score (1-5)', shrink=0.8)\n"
            "plt.show()"
        )
    ]
    nb['cells'] = cells
    nbf.write(nb, NOTEBOOKS_DIR / "03_reclassification.ipynb")
    print("Notebook 03 created successfully.")

def create_notebook_04():
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell(
            "# Notebook 04: HSI Weighted Overlay, Statistics & Map layout\n\n"
            "This notebook calculates the final Habitat Suitability Index (HSI) using a Weighted Overlay, "
            "classifies HSI into suitability categories, computes spatial extent statistics, "
            "and plots a publication-ready final map.\n\n"
            "## Objectives:\n"
            "1. Calculate Weighted Overlay (HSI).\n"
            "2. Classify HSI into 5 category classes.\n"
            "3. Compute area statistics ($$km^2$$ and percentage) and export to CSV.\n"
            "4. Plot the final publication map with a scale bar, north arrow, coordinate grid, and legend."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import geopandas as gpd\n"
            "import matplotlib.pyplot as plt\n"
            "import rasterio\n\n"
            "# Configure paths\n"
            "NOTEBOOK_DIR = Path(os.getcwd())\n"
            "PROJECT_ROOT = NOTEBOOK_DIR.parent\n"
            "sys.path.append(str(PROJECT_ROOT))\n\n"
            "from src.suitability import calculate_hsi, classify_hsi, calculate_statistics\n"
            "from src.visualization import plot_publication_map, plot_statistics_chart\n\n"
            "print('Environment ready!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. HSI Weighted Overlay Model\n\n"
            "We apply the weights: \n"
            "- NDVI: 30%\n"
            "- Distance to Water: 25%\n"
            "- LULC: 20%\n"
            "- Slope: 15%\n"
            "- DEM (Elevation): 10%\n\n"
            "$$\\text{HSI} = 0.30 \\times \\text{NDVI} + 0.25 \\times \\text{DistanceToWater} + 0.20 \\times \\text{LULC} + 0.15 \\times \\text{Slope} + 0.10 \\times \\text{Elevation}$$"
        ),
        nbf.v4.new_code_cell(
            "reclass_dir = PROJECT_ROOT / 'data' / 'processed' / 'Reclassified'\n"
            "output_dir = PROJECT_ROOT / 'data' / 'processed' / 'Output'\n"
            "output_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "reclass_paths = {\n"
            "    'ndvi': reclass_dir / 'NDVI_Reclass.tif',\n"
            "    'dem': reclass_dir / 'DEM_Reclass.tif',\n"
            "    'slope': reclass_dir / 'Slope_Reclass.tif',\n"
            "    'distance': reclass_dir / 'Distance_Reclass.tif',\n"
            "    'lulc': reclass_dir / 'LULC_Reclass.tif'\n"
            "}\n\n"
            "reclassed_data = {}\n"
            "for name, path in reclass_paths.items():\n"
            "    with rasterio.open(path) as src:\n"
            "        reclassed_data[name] = src.read(1)\n"
            "        out_profile = src.profile.copy()\n\n"
            "weights = {\n"
            "    'ndvi': 0.30,\n"
            "    'distance': 0.25,\n"
            "    'lulc': 0.20,\n"
            "    'slope': 0.15,\n"
            "    'dem': 0.10\n"
            "}\n\n"
            "hsi = calculate_hsi(reclassed_data, weights)\n"
            "hsi_class = classify_hsi(hsi)\n\n"
            "# Mask out water bodies (class 0 in Dynamic World LULC) from the suitability calculations\n"
            "with rasterio.open(PROJECT_ROOT / 'data' / 'processed' / 'Cleaned' / 'DynamicWorld_Clean.tif') as src:\n"
            "    lulc_clean = src.read(1)\n\n"
            "hsi[lulc_clean == 0] = np.nan\n"
            "hsi_class[lulc_clean == 0] = np.nan\n\n"
            "# Save GeoTIFFs\n"
            "hsi_path = output_dir / 'Habitat_Suitability_Index.tif'\n"
            "class_path = output_dir / 'Habitat_Suitability_Class.tif'\n\n"
            "out_profile.update(dtype='float32', nodata=np.nan, compress='lzw')\n\n"
            "with rasterio.open(hsi_path, 'w', **out_profile) as dst:\n"
            "    dst.write(hsi, 1)\n"
            "with rasterio.open(class_path, 'w', **out_profile) as dst:\n"
            "    dst.write(hsi_class, 1)\n\n"
            "print('HSI maps saved!')"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Area Statistics\n\n"
            "We calculate the area in square kilometers for each suitability class (assuming 10m pixel resolution)."
        ),
        nbf.v4.new_code_cell(
            "stats_df = calculate_statistics(hsi_class, resolution=10.0)\n"
            "stats_df.to_csv(output_dir / 'Habitat_Suitability_Statistics.csv', index=False)\n"
            "stats_df"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Publication-Grade Map and Chart\n\n"
            "We call the visualization functions to generate high-resolution figures."
        ),
        nbf.v4.new_code_cell(
            "aoi_path = PROJECT_ROOT / 'data' / 'raw' / 'AOI' / 'Corbett_AOI.shp'\n"
            "map_jpg = output_dir / 'Corbett_Habitat_Suitability_Map.png'\n"
            "chart_jpg = output_dir / 'Habitat_Suitability_Statistics_Chart.png'\n\n"
            "# Generate map\n"
            "plot_publication_map(class_path, aoi_path, map_jpg)\n\n"
            "# Generate chart\n"
            "plot_statistics_chart(stats_df, chart_jpg)\n\n"
            "# Display the map here in notebook\n"
            "from IPython.display import Image\n"
            "Image(filename=str(map_jpg), width=600)"
        )
    ]
    nb['cells'] = cells
    nbf.write(nb, NOTEBOOKS_DIR / "04_hsi_overlay_statistics.ipynb")
    print("Notebook 04 created successfully.")

def main():
    print("Generating all consolidated notebooks...")
    create_notebook_01()
    create_notebook_02()
    create_notebook_03()
    create_notebook_04()
    print("All notebooks created successfully!")

if __name__ == "__main__":
    main()
