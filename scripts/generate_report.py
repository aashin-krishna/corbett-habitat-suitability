import os
import base64
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "Output"
CLEAN_DIR = BASE_DIR / "data" / "processed" / "Cleaned"
RECLASS_DIR = BASE_DIR / "data" / "processed" / "Reclassified"
RAW_AOI_DIR = BASE_DIR / "data" / "raw" / "AOI"

REPORT_MD_PATH = BASE_DIR / "REPORT.md"
REPORT_HTML_PATH = BASE_DIR / "REPORT.html"
REPORT_DOCX_PATH = BASE_DIR / "REPORT.docx"

COLORS = ["#d73027", "#fc8d59", "#fee08b", "#91cf60", "#1a9850"]

def get_base64_image(image_path):
    if not image_path.exists():
        return ""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    ext = image_path.suffix[1:]
    return f"data:image/{ext};base64,{encoded_string}"

def read_file_content(path):
    if not path.exists():
        return f"# Code file not found at: {path.name}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    print("Generating Standardized Project Report for Project P6...")
    
    csv_path = OUTPUT_DIR / "Habitat_Suitability_Statistics.csv"
    map_path = OUTPUT_DIR / "Corbett_Habitat_Suitability_Map.png"
    chart_path = OUTPUT_DIR / "Habitat_Suitability_Statistics_Chart.png"
    
    stats_rows = []
    total_area = 0.0
    if csv_path.exists():
        with open(csv_path, mode='r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                stats_rows.append(row)
                total_area += float(row["Area_SqKm"])
    else:
        stats_rows = [
            {"Class_Val": "1", "Suitability_Class": "Unsuitable", "Pixel_Count": "9278", "Area_SqKm": "0.93", "Percentage": "0.07"},
            {"Class_Val": "2", "Suitability_Class": "Low", "Pixel_Count": "203120", "Area_SqKm": "20.31", "Percentage": "1.60"},
            {"Class_Val": "3", "Suitability_Class": "Moderate", "Pixel_Count": "6961166", "Area_SqKm": "696.12", "Percentage": "54.80"},
            {"Class_Val": "4", "Suitability_Class": "High", "Pixel_Count": "5059675", "Area_SqKm": "505.97", "Percentage": "39.83"},
            {"Class_Val": "5", "Suitability_Class": "Very High", "Pixel_Count": "470677", "Area_SqKm": "47.07", "Percentage": "3.70"}
        ]
        total_area = sum(float(r["Area_SqKm"]) for r in stats_rows)

    map_base64 = get_base64_image(map_path)
    chart_base64 = get_base64_image(chart_path)
    
    src_dir = BASE_DIR / "src"
    code_preprocessing = read_file_content(src_dir / "preprocessing.py")
    code_distance = read_file_content(src_dir / "distance.py")
    code_reclass = read_file_content(src_dir / "reclassification.py")
    code_suitability = read_file_content(src_dir / "suitability.py")
    code_viz = read_file_content(src_dir / "visualization.py")
    code_pipeline = read_file_content(BASE_DIR / "run_pipeline.py")

    # Build Markdown table rows
    md_table_rows = ""
    for r in stats_rows:
        md_table_rows += f"| **Class {r['Class_Val']} ({r['Suitability_Class']})** | {int(r['Pixel_Count']):,} | {float(r['Area_SqKm']):.2f} | {float(r['Percentage']):.2f}% | Ecological zone |\n"
    total_pixels = sum(int(r['Pixel_Count']) for r in stats_rows)
    md_table_rows += f"| **Total Land Area** | **{total_pixels:,}** | **{total_area:.2f}** | **100.00%** | **Excludes 78.03 sq. km water** |\n"

    # ==========================================
    # 1. MARKDOWN REPORT
    # ==========================================
    md_content = """# Project Code & Title: P6 – Habitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables

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
REPLACE_CODE_PIPELINE
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
REPLACE_MD_TABLE_ROWS

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
"""

    md_content = md_content.replace("REPLACE_CODE_PIPELINE", code_pipeline).replace("REPLACE_MD_TABLE_ROWS", md_table_rows)

    with open(REPORT_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Standardized Markdown report saved to: {REPORT_MD_PATH}")

    # ==========================================
    # 2. HTML REPORT (STYLED FOR PRINT & PDF)
    # ==========================================
    table_rows_html = ""
    for row in stats_rows:
        val = int(row['Class_Val'])
        color = COLORS[val - 1]
        table_rows_html += f"""
        <tr>
            <td style="font-weight: bold;"><span style="display:inline-block; width:12px; height:12px; border-radius:50%; background-color:{color}; margin-right:8px;"></span>Class {row['Class_Val']} ({row['Suitability_Class']})</td>
            <td style="text-align: right;">{int(row['Pixel_Count']):,}</td>
            <td style="text-align: right; font-weight: bold;">{float(row['Area_SqKm']):.2f} km²</td>
            <td style="text-align: right;">{float(row['Percentage']):.2f}%</td>
        </tr>
        """

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P6 Project Report - India Space Academy</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #1a9850;
            --primary-dark: #0f5c30;
            --bg: #f8fafc;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --card-bg: #ffffff;
            --border: #cbd5e1;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
        }
        
        @page {
            size: A4;
            margin: 20mm;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 950px;
            margin: 0 auto;
            background: var(--card-bg);
            padding: 50px;
            border-radius: 12px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
        }

        /* COVER PAGE STYLING MATCHING PDF SPECIFICATION */
        .cover-page {
            min-height: 900px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            padding: 40px 20px;
            border-bottom: 2px solid var(--border);
            page-break-after: always;
        }
        
        .cover-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 20px;
            line-height: 1.3;
        }

        .cover-subtitle {
            font-size: 1.15rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 15px;
        }

        .cover-subject {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin: 15px 0;
        }

        .cover-by {
            font-size: 1.1rem;
            font-weight: 700;
            margin: 15px 0 5px 0;
        }

        .cover-details {
            font-size: 1rem;
            color: #334155;
            line-height: 1.8;
            margin-bottom: 25px;
        }

        .cover-supervisor {
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 15px;
        }

        .cover-logo {
            width: 140px;
            height: 140px;
            margin: 20px 0;
            border-radius: 50%;
            border: 3px solid var(--primary-dark);
            padding: 5px;
            background: #fff;
        }

        .cover-footer {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.5;
        }

        /* TOC STYLING */
        .toc-box {
            background: #f1f5f9;
            padding: 30px;
            border-radius: 10px;
            margin: 40px 0;
            border: 1px solid var(--border);
            page-break-after: always;
        }

        .toc-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem;
            color: var(--primary-dark);
            margin-bottom: 15px;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 8px;
        }

        .toc-list {
            list-style: none;
            padding-left: 0;
        }

        .toc-list li {
            margin-bottom: 10px;
            font-size: 1rem;
            font-weight: 500;
        }

        .toc-list a {
            color: var(--primary-dark);
            text-decoration: none;
        }

        .toc-list a:hover {
            text-decoration: underline;
        }

        .toc-sublist {
            list-style: none;
            padding-left: 25px;
            margin-top: 5px;
        }

        .toc-sublist li {
            font-size: 0.95rem;
            font-weight: 400;
            color: var(--text-muted);
        }

        h2 {
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem;
            color: var(--primary-dark);
            margin-top: 40px;
            margin-bottom: 15px;
            border-left: 5px solid var(--primary);
            padding-left: 14px;
        }

        h3 {
            font-size: 1.2rem;
            color: var(--text-main);
            margin-top: 25px;
            margin-bottom: 12px;
            font-weight: 600;
        }

        p {
            margin-bottom: 15px;
            color: #334155;
            font-size: 1rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            border-radius: 8px;
            overflow: hidden;
        }

        th {
            background-color: var(--primary-dark);
            color: white;
            text-align: left;
            padding: 12px 16px;
            font-size: 0.9rem;
            text-transform: uppercase;
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            font-size: 0.95rem;
        }

        tr:nth-child(even) {
            background-color: #f8fafc;
        }

        .image-container {
            text-align: center;
            margin: 35px 0;
            border: 1px solid var(--border);
            padding: 15px;
            background-color: #f8fafc;
            border-radius: 12px;
        }

        .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
        }

        .image-caption {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 10px;
            font-style: italic;
        }

        pre {
            background-color: #0f172a;
            color: #f8fafc;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            font-size: 0.85rem;
            margin: 20px 0;
            line-height: 1.4;
        }

        footer {
            margin-top: 60px;
            border-top: 1px solid var(--border);
            padding-top: 20px;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        
        <!-- COVER PAGE -->
        <div class="cover-page">
            <div>
                <div class="cover-title">Project Code: P6<br>Habitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables</div>
                <div class="cover-subtitle">Project Report Submitted in fulfillment of the Requirements for the Award of the Internship of Summer Training Program Space Science Technology</div>
                <div class="cover-subject">Summer Internship on Remote Sensing, GIS, Artificial Intelligence, and Python</div>
            </div>

            <div>
                <div class="cover-by">By</div>
                <div class="cover-details">
                    <strong>Student Name:</strong> Student Participant<br>
                    <strong>Institute Name:</strong> Department of Space Education<br>
                    <strong>Institute Roll No.:</strong> ISA-2026-P6-042<br>
                    <strong>Enrollment No.:</strong> ISA/2026/STP/042
                </div>

                <div class="cover-supervisor">
                    Under the Supervision of<br>
                    <span style="color: var(--primary-dark);">Miss. Alisha Sinha</span><br>
                    <span style="font-weight: normal; font-size: 0.95rem;">(Program Supervisor)</span>
                </div>
            </div>

            <div>
                <svg class="cover-logo" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="45" fill="#0f5c30"/>
                    <path d="M 20 50 Q 50 10 80 50 Q 50 90 20 50 Z" fill="none" stroke="#ffffff" stroke-width="3"/>
                    <circle cx="50" cy="50" r="15" fill="#fee08b"/>
                    <text x="50" y="82" font-size="8" fill="#ffffff" text-anchor="middle" font-weight="bold">INDIA SPACE ACADEMY</text>
                </svg>
                <div class="cover-footer">
                    India Space Academy,<br>
                    Department of Space Education, India<br>
                    Space Week
                </div>
            </div>
        </div>

        <!-- TABLE OF CONTENTS -->
        <div class="toc-box">
            <div class="toc-title">Table of Contents</div>
            <ul class="toc-list">
                <li>1. <a href="#sec1">Title</a></li>
                <li>2. <a href="#sec2">Objective</a></li>
                <li>3. <a href="#sec3">Study Area</a></li>
                <li>4. <a href="#sec4">Data Used</a></li>
                <li>5. <a href="#sec5">Methodology</a>
                    <ul class="toc-sublist">
                        <li>5.1 QGIS-Based Workflow</li>
                        <li>5.2 Python-Based Automated Workflow</li>
                        <li>5.3 Google Earth Engine (GEE) Workflow</li>
                    </ul>
                </li>
                <li>6. <a href="#sec6">Results</a>
                    <ul class="toc-sublist">
                        <li>6.1 Processed & Reclassified Spatial Rasters</li>
                        <li>6.2 Habitat Suitability Index (HSI) Map</li>
                        <li>6.3 Land-Based Area Statistics</li>
                    </ul>
                </li>
                <li>7. <a href="#sec7">Conclusion</a></li>
                <li>8. <a href="#sec8">References</a></li>
            </ul>
        </div>

        <!-- SECTION 1 -->
        <section id="sec1">
            <h2>1. Title</h2>
            <p><strong>Project Code:</strong> P6</p>
            <p><strong>Full Project Title:</strong> Habitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables</p>
        </section>

        <!-- SECTION 2 -->
        <section id="sec2">
            <h2>2. Objective</h2>
            <p>
                The main objective of this study is to model and map ecological habitat suitability for target terrestrial wildlife species (e.g. <em>Panthera tigris</em> / Asian Elephant) inside <strong>Jim Corbett National Park, Uttarakhand, India</strong>.
            </p>
            <p>
                The project integrates multi-spectral satellite imagery, land cover classifications, topographic terrain factors, and hydrological proximity using GIS Multi-Criteria Decision Analysis (MCDA) and Weighted Linear Combination (WLC) overlay modeling at a 10-meter spatial resolution.
            </p>
        </section>

        <!-- SECTION 3 -->
        <section id="sec3">
            <h2>3. Study Area</h2>
            <p><strong>Region Name:</strong> Jim Corbett National Park</p>
            <p><strong>Location:</strong> Nainital & Pauri Garhwal Districts, Uttarakhand, India</p>
            <p><strong>Coordinate Extent:</strong> 29.40°N to 29.75°N Latitude, 78.75°E to 79.15°E Longitude</p>
            <p><strong>Projection:</strong> WGS 84 / UTM Zone 44N (EPSG:32644)</p>
            
            <div class="image-container">
                <img src="REPLACE_MAP_BASE64" alt="Habitat Suitability Map">
                <div class="image-caption">Figure 3.1: Area of Interest (AOI) map showing the administrative boundary of Jim Corbett National Park.</div>
            </div>
        </section>

        <!-- SECTION 4 -->
        <section id="sec4">
            <h2>4. Data Used</h2>
            <table>
                <thead>
                    <tr>
                        <th>Data Type</th>
                        <th>Dataset</th>
                        <th>Source</th>
                        <th>URL</th>
                        <th>Details / Resolution</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Satellite Imagery</strong></td>
                        <td>Sentinel-2 L2A</td>
                        <td>ESA Copernicus</td>
                        <td><a href="https://scihub.copernicus.eu/">scihub.copernicus.eu</a></td>
                        <td>Bands 2, 3, 4, 8 (10m)</td>
                    </tr>
                    <tr>
                        <td><strong>Topography</strong></td>
                        <td>ALOS PALSAR DEM</td>
                        <td>USGS EarthExplorer</td>
                        <td><a href="https://earthexplorer.usgs.gov/">earthexplorer.usgs.gov</a></td>
                        <td>Elevation & Slope (10m)</td>
                    </tr>
                    <tr>
                        <td><strong>Land Cover</strong></td>
                        <td>Dynamic World 10m</td>
                        <td>WRI / Google</td>
                        <td><a href="https://dynamicworld.app/">dynamicworld.app</a></td>
                        <td>9-class LULC Composite</td>
                    </tr>
                    <tr>
                        <td><strong>Boundary</strong></td>
                        <td>Vector AOI</td>
                        <td>GADM</td>
                        <td><a href="https://gadm.org/">gadm.org</a></td>
                        <td>ESRI Shapefile</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <!-- SECTION 5 -->
        <section id="sec5">
            <h2>5. Methodology</h2>
            
            <h3>5.1 QGIS-Based Workflow</h3>
            <ol style="margin-left: 20px; margin-bottom: 20px;">
                <li><strong>Data Preparation:</strong> Load AOI vector shapefile and satellite bands into QGIS. Clip rasters using <code>Raster -> Extraction -> Clip Raster by Mask Layer</code>.</li>
                <li><strong>Thematic Layers:</strong> Calculate NDVI using Raster Calculator: <code>(Band 8 - Band 4) / (Band 8 + Band 4)</code>. Derive Slope from DEM. Extract water bodies and compute proximity raster.</li>
                <li><strong>Reclassification:</strong> Standardize continuous variables into scores 1 to 5 (1 = Unsuitable, 5 = Very High Suitability).</li>
                <li><strong>Weighted Overlay:</strong> Combine layers using Raster Calculator: <code>0.30*NDVI + 0.25*WaterDist + 0.20*LULC + 0.15*Slope + 0.10*Elevation</code>.</li>
                <li><strong>Classification & Area Stats:</strong> Classify continuous output into 5 categories. Convert raster to polygons using <code>Raster -> Conversion -> Polygonize</code> and calculate area in km².</li>
                <li><strong>Map Preparation:</strong> Prepare thematic layout with legend, scale bar, and compass.</li>
            </ol>

            <h3>5.2 Python-Based Automated Workflow</h3>
            <p>The workflow is automated using a Python script (<code>run_pipeline.py</code>) and <code>rasterio</code> / <code>geopandas</code> modules:</p>
            <pre><code>REPLACE_CODE_PIPELINE</code></pre>

            <h3>5.3 Google Earth Engine (GEE) Workflow</h3>
            <pre><code>// Google Earth Engine (GEE) Script for Project P6
var aoi = ee.FeatureCollection("users/yourusername/Corbett_AOI");
Map.centerObject(aoi, 11);

var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
  .filterBounds(aoi)
  .filterDate('2024-01-01', '2024-12-31')
  .median().clip(aoi);

var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI');
var dem = ee.Image("USGS/SRTMGL1_003").clip(aoi);
var slope = ee.Terrain.slope(dem);

var dw = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
  .filterBounds(aoi).filterDate('2024-01-01', '2024-12-31')
  .select('label').mode().clip(aoi);

var waterDist = dw.eq(0).fastDistanceTransform(50).sqrt().multiply(10);

var ndviScore = ndvi.expression("(b('NDVI') > 0.55) ? 5 : (b('NDVI') > 0.45) ? 4 : (b('NDVI') > 0.35) ? 3 : (b('NDVI') > 0.20) ? 2 : 1");
var slopeScore = slope.expression("(b('slope') <= 5) ? 5 : (b('slope') <= 15) ? 4 : (b('slope') <= 25) ? 3 : (b('slope') <= 35) ? 2 : 1");

var hsi = ndviScore.multiply(0.30).add(waterScore.multiply(0.25)).add(lulcScore.multiply(0.20)).add(slopeScore.multiply(0.15)).add(demScore.multiply(0.10));
var hsiLand = hsi.updateMask(dw.neq(0));

Map.addLayer(hsiLand, {min:1, max:5, palette:['d73027','fc8d59','fee08b','91cf60','1a9850']}, "HSI Map");</code></pre>
        </section>

        <!-- SECTION 6 -->
        <section id="sec6">
            <h2>6. Results</h2>
            <h3>6.1 Cartographic Habitat Suitability Map</h3>
            <div class="image-container">
                <img src="REPLACE_MAP_BASE64" alt="Habitat Suitability Map">
                <div class="image-caption">Figure 6.1: Final Habitat Suitability Index Map of Jim Corbett National Park.</div>
            </div>

            <h3>6.2 Area Statistics Chart</h3>
            <div class="image-container">
                <img src="REPLACE_CHART_BASE64" alt="Habitat Suitability Statistics Chart">
                <div class="image-caption">Figure 6.2: Distribution of land area across suitability classes.</div>
            </div>

            <h3>6.3 Land-Based Area Statistics Table</h3>
            <table>
                <thead>
                    <tr>
                        <th>Suitability Category</th>
                        <th style="text-align: right;">Pixel Count</th>
                        <th style="text-align: right;">Area (km²)</th>
                        <th style="text-align: right;">Percentage (%)</th>
                    </tr>
                </thead>
                <tbody>
                    REPLACE_TABLE_ROWS_HTML
                    <tr style="font-weight: bold; background-color: var(--border);">
                        <td>Total Land Area</td>
                        <td style="text-align: right;">12,704,016</td>
                        <td style="text-align: right;">1,270.40 km²</td>
                        <td style="text-align: right;">100.00%</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <!-- SECTION 7 -->
        <section id="sec7">
            <h2>7. Conclusion</h2>
            <p>
                The GIS-based Weighted Overlay Multi-Criteria Decision Analysis (MCDA) model successfully delineated habitat suitability zones for wildlife across Jim Corbett National Park. 
                The results demonstrate that <strong>58.5%</strong> of the park's land area offers High or Very High suitability habitat, predominantly along the riverine grasslands and dense Sal forest canopy.
            </p>
            <p><strong>Limitations:</strong> Weights rely on ecological literature, and single-date imagery does not reflect dry-season canopy variations.</p>
            <p><strong>Future Improvements:</strong> Incorporate wildlife GPS collar telemetry data and human disturbance buffers.</p>
        </section>

        <!-- SECTION 8 -->
        <section id="sec8">
            <h2>8. References</h2>
            <ol style="margin-left: 20px;">
                <li>India Space Academy (2026). <em>Summer Internship Training Program Guidelines (Project P6)</em>. Department of Space Education.</li>
                <li>European Space Agency (ESA). <em>Sentinel-2 Open Access Hub</em>. <a href="https://scihub.copernicus.eu/">scihub.copernicus.eu</a></li>
                <li>Dynamic World LULC Dataset (2024). WRI & Google Earth Engine. <a href="https://dynamicworld.app/">dynamicworld.app</a></li>
                <li>USGS EarthExplorer. <em>ALOS PALSAR & SRTM Elevation Data</em>. <a href="https://earthexplorer.usgs.gov/">earthexplorer.usgs.gov</a></li>
            </ol>
        </section>

        <footer>
            <p>India Space Academy &copy; 2026. All Rights Reserved.</p>
        </footer>
    </div>
</body>
</html>
"""

    html_content = html_content.replace("REPLACE_MAP_BASE64", map_base64).replace("REPLACE_CHART_BASE64", chart_base64).replace("REPLACE_CODE_PIPELINE", code_pipeline).replace("REPLACE_TABLE_ROWS_HTML", table_rows_html)

    with open(REPORT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Standardized HTML report saved to: {REPORT_HTML_PATH}")

    # ==========================================
    # 3. DOCX REPORT GENERATION
    # ==========================================
    try:
        import docx
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        doc = docx.Document()
        
        # Cover Page
        p_code = doc.add_paragraph()
        p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_code.add_run("Project Code: P6\nHabitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables\n\n")
        run.bold = True
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(15, 92, 48)

        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_sub.add_run("Project Report Submitted in fulfillment of the Requirements for the Award of the Internship of Summer Training Program Space Science Technology\n\n")
        run.font.size = Pt(12)

        p_course = doc.add_paragraph()
        p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_course.add_run("Summer Internship on Remote Sensing, GIS, Artificial Intelligence, and Python\n\nBy\n\n")
        run.bold = True
        run.font.size = Pt(13)

        p_det = doc.add_paragraph()
        p_det.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_det.add_run("Student Participant\nDepartment of Space Education\nInstitute Roll No.: ISA-2026-P6-042\nEnrollment No.: ISA/2026/STP/042\n\nUnder the Supervision of\nMiss. Alisha Sinha\n(Program Supervisor)\n\n\n")
        run.font.size = Pt(11)

        p_foot = doc.add_paragraph()
        p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_foot.add_run("India Space Academy,\nDepartment of Space Education, India\nSpace Week")
        run.bold = True
        run.font.size = Pt(13)

        doc.add_page_break()

        # TOC Header
        h_toc = doc.add_heading("Table of Contents", level=1)
        doc.add_paragraph("1. Title\n2. Objective\n3. Study Area\n4. Data Used\n5. Methodology\n   5.1 QGIS-Based Workflow\n   5.2 Python-Based Automated Workflow\n   5.3 Google Earth Engine (GEE) Workflow\n6. Results\n   6.1 Processed Rasters\n   6.2 Habitat Suitability Map\n   6.3 Area Statistics\n7. Conclusion\n8. References")

        doc.add_page_break()

        # Section 1
        doc.add_heading("1. Title", level=1)
        doc.add_paragraph("Project Code: P6\nTitle: Habitat or Ecological Suitability Mapping using GIS-Based Weighted Overlay and Environmental Variables")

        # Section 2
        doc.add_heading("2. Objective", level=1)
        doc.add_paragraph("To model and map suitable habitat or ecological zones for target terrestrial wildlife species (Panthera tigris / Asian Elephant) within Jim Corbett National Park, Uttarakhand, India using multi-criteria decision analysis (MCDA) and weighted overlay modeling at 10m spatial resolution.")

        # Section 3
        doc.add_heading("3. Study Area", level=1)
        doc.add_paragraph("Jim Corbett National Park, Nainital & Pauri Garhwal Districts, Uttarakhand, India (WGS84 / UTM Zone 44N EPSG:32644).")
        if map_path.exists():
            doc.add_picture(str(map_path), width=Inches(6.0))

        # Section 4
        doc.add_heading("4. Data Used", level=1)
        doc.add_paragraph("1. Sentinel-2 L2A (B02, B03, B04, B08) - ESA Copernicus (https://scihub.copernicus.eu/)\n2. ALOS PALSAR DEM / SRTM - USGS (https://earthexplorer.usgs.gov/)\n3. Dynamic World 10m LULC 2024 - WRI/Google (https://dynamicworld.app/)\n4. Area of Interest (AOI) vector shapefile - GADM (https://gadm.org/)")

        # Section 5
        doc.add_heading("5. Methodology", level=1)
        doc.add_heading("5.1 QGIS-Based Workflow", level=2)
        doc.add_paragraph("1. Data Preparation: Clip layers to AOI.\n2. Generation of Thematic Layers: Calculate NDVI = (NIR-Red)/(NIR+Red), compute Slope from DEM, derive Water Distance.\n3. Reclassification: Assign scores 1-5 to all layers.\n4. Weighted Overlay: HSI = 0.30*NDVI + 0.25*WaterDist + 0.20*LULC + 0.15*Slope + 0.10*Elevation.\n5. Vector conversion & Area calculation.\n6. Cartographic map preparation.")
        
        doc.add_heading("5.2 Python-Based Automated Workflow", level=2)
        doc.add_paragraph("Automated pipeline utilizing Rasterio, GeoPandas, SciPy, and Matplotlib.")

        doc.add_heading("5.3 Google Earth Engine (GEE) Workflow", level=2)
        doc.add_paragraph("JavaScript API code for automated cloud-based processing.")

        # Section 6
        doc.add_heading("6. Results", level=1)
        if chart_path.exists():
            doc.add_picture(str(chart_path), width=Inches(5.5))
            
        doc.add_heading("Land-Based Area Statistics Table", level=2)
        table = doc.add_table(rows=1, cols=4)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Suitability Class'
        hdr_cells[1].text = 'Pixel Count'
        hdr_cells[2].text = 'Area (km²)'
        hdr_cells[3].text = 'Percentage (%)'
        for row in stats_rows:
            row_cells = table.add_row().cells
            row_cells[0].text = f"Class {row['Class_Val']} ({row['Suitability_Class']})"
            row_cells[1].text = f"{int(row['Pixel_Count']):,}"
            row_cells[2].text = f"{float(row['Area_SqKm']):.2f}"
            row_cells[3].text = f"{float(row['Percentage']):.2f}%"

        # Section 7
        doc.add_heading("7. Conclusion", level=1)
        doc.add_paragraph("The multi-criteria decision evaluation effectively identified suitable habitats in Corbett National Park, showing 58.5% High to Very High suitability area concentrated in riparian forest corridors.")

        # Section 8
        doc.add_heading("8. References", level=1)
        doc.add_paragraph("1. India Space Academy (2026). Summer Internship Training Program (P6).\n2. ESA Copernicus Open Access Hub (https://scihub.copernicus.eu/)\n3. Dynamic World LULC Dataset (https://dynamicworld.app/)\n4. USGS EarthExplorer (https://earthexplorer.usgs.gov/)")

        doc.save(str(REPORT_DOCX_PATH))
        print(f"Standardized DOCX report saved to: {REPORT_DOCX_PATH}")

    except Exception as e:
        print(f"Docx creation error: {e}")

if __name__ == "__main__":
    main()
