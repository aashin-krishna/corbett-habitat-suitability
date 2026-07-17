# Habitat Suitability Index (HSI) Modelling for Jim Corbett National Park

This repository contains an end-to-end remote sensing and Geographic Information System (GIS) pipeline to model habitat suitability for target terrestrial wildlife (e.g., *Panthera tigris* / Asian Elephant) within **Jim Corbett National Park, Uttarakhand, India**.

The model is built at a **10-meter spatial resolution** by integrating multi-spectral Sentinel-2 imagery, ALOS PALSAR Digital Elevation Models (DEM), and Google/WRI's Dynamic World Land Use/Land Cover (LULC) dataset.

---

## 1. Project Overview & Methodology

The Habitat Suitability Index (HSI) is computed using a **Weighted Linear Combination Overlay** of five environmental and geophysical parameters. All layers are reprojected to UTM Zone 44N (EPSG:32644), clipped to the park's Administrative Boundary (AOI), and reclassified into suitability scores from **1 (Unsuitable)** to **5 (Very High Suitability)**.

### Environmental Criteria & Reclassification Bins
1. **NDVI (Vegetation Index)** (Weight: **30%**): Derived from Sentinel-2 Red (B04) and NIR (B08) bands. Higher values indicate dense canopy/forage.
   - $\le$ 0.20 $\rightarrow$ 1 | 0.20 - 0.35 $\rightarrow$ 2 | 0.35 - 0.45 $\rightarrow$ 3 | 0.45 - 0.55 $\rightarrow$ 4 | > 0.55 $\rightarrow$ 5
2. **Distance to Waterbody** (Weight: **25%**): Computed via Euclidean Distance Transform on LULC waterbodies. Proximity is critical.
   - $\le$ 250m $\rightarrow$ 5 | 250m - 500m $\rightarrow$ 4 | 500m - 1000m $\rightarrow$ 3 | 1000m - 2000m $\rightarrow$ 2 | > 2000m $\rightarrow$ 1
3. **LULC Classes** (Weight: **20%**): Reclassified from Dynamic World categories:
   - Trees $\rightarrow$ 5 | Grass/Shrub $\rightarrow$ 4 | Water/Flooded Veg $\rightarrow$ 3 | Crops $\rightarrow$ 2 | Built/Bare/Snow $\rightarrow$ 1
4. **Slope** (Weight: **15%**): Calculated in degrees from the DEM. Gentler terrain is favored.
   - $\le$ 5° $\rightarrow$ 5 | 5° - 15° $\rightarrow$ 4 | 15° - 25° $\rightarrow$ 3 | 25° - 35° $\rightarrow$ 2 | > 35° $\rightarrow$ 1
5. **Elevation (DEM)** (Weight: **10%**): Vertical elevation limits access.
   - $\le$ 300m $\rightarrow$ 5 | 300m - 500m $\rightarrow$ 4 | 500m - 700m $\rightarrow$ 3 | 700m - 900m $\rightarrow$ 2 | > 900m $\rightarrow$ 1

### Weighted Overlay Equation:
$$\text{HSI} = 0.30 \times \text{NDVI} + 0.25 \times \text{DistanceToWater} + 0.20 \times \text{LULC} + 0.15 \times \text{Slope} + 0.10 \times \text{Elevation}$$

The final continuous index is classified into 5 categories: **Unsuitable** ([1.0, 1.8)), **Low** ([1.8, 2.6)), **Moderate** ([2.6, 3.4)), **High** ([3.4, 4.2)), and **Very High** ($\ge$ 4.2).

---

## 2. Repository Structure

This repository is organized as a clean, production-ready Python package:

```text
corbett-habitat-suitability/
│
├── data/
│   ├── raw/
│   │   ├── AOI/                # Jim Corbett boundary Shapefile (tracked in Git)
│   │   ├── Sentinel/           # Place raw Sentinel-2 *.jp2 band files here
│   │   ├── DEM/                # Place raw DEM_30m.tif here
│   │   └── DynamicWorld/       # Place raw DynamicWorld_2024.tif here
│   │
│   └── processed/              # (Git Ignored) Intermediate and output rasters
│       ├── Cleaned/            # Clipped and reprojected input layers
│       ├── Reclassified/       # Score layers (1 to 5)
│       └── Output/             # Final HSI GeoTIFFs and PNG maps
│
├── notebooks/                  # Chronological walkthrough notebooks
│   ├── 01_data_preprocessing.ipynb
│   ├── 02_raster_cleaning_distance.ipynb
│   ├── 03_reclassification.ipynb
│   └── 04_hsi_overlay_statistics.ipynb
│
├── src/                        # Modular source code package
│   ├── __init__.py
│   ├── preprocessing.py        # Raster clipping, NDVI, DEM, Slope calculations
│   ├── distance.py             # Water mask EDT calculation
│   ├── reclassification.py     # Continuous/discrete scoring logic
│   ├── suitability.py          # Weighted overlay & classification
│   └── visualization.py        # Publication-grade mapping layout
│
├── scripts/
│   ├── create_notebooks.py     # Notebook helper generator
│   └── generate_report.py      # Report compiler (MD/HTML)
│
├── run_pipeline.py             # End-to-end execution runner script
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── REPORT.md                   # Markdown Project Report
└── REPORT.html                 # Self-contained HTML report with maps
```

---

## 3. Getting Started & Installation

### Prerequisite Data Placement
Since remote sensing files exceed GitHub's 100MB file limit, they are ignored by `.gitignore`. You must obtain the source data and place it inside the `data/raw/` directories:
1. **AOI Shapefiles**: Already provided in `data/raw/AOI/`.
2. **Sentinel-2 Bands**: Download Sentinel-2 L2A tile covering Corbett (UTM Zone 44N) and place the `B02_10m.jp2`, `B03_10m.jp2`, `B04_10m.jp2`, and `B08_10m.jp2` bands under `data/raw/Sentinel/`.
3. **DEM**: Download ALOS PALSAR 30m DEM and place it as `DEM_30m.tif` in `data/raw/DEM/`.
4. **LULC**: Download the 10m Dynamic World annual composite for 2024 and place it as `DynamicWorld_2024.tif` in `data/raw/DynamicWorld/`.

### Installation
Clone the repository and install dependencies inside a virtual environment:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required spatial packages
pip install -r requirements.txt
```

---

## 4. Usage

### Option 1: Run the End-to-End Pipeline
To execute the entire GIS preprocessing, model calculation, map rendering, and statistical compilation in a single run:

```bash
python run_pipeline.py
```
This saves all intermediate rasters, outputs, publication PNG maps, and CSV statistics in `data/processed/`.

### Option 2: Run Jupyter Notebooks
If you want an interactive step-by-step walkthrough:

```bash
jupyter lab
```
Open and run the notebooks in sequence from the `notebooks/` directory.

### Option 3: Compile Project Reports
To compile the final Markdown report and the beautifully styled, self-contained HTML report (with embedded base64 maps/charts):

```bash
python scripts/generate_report.py
```

---

## 5. Results & Statistics Summary

| Suitability Class | Area ($km^2$) | Percentage (%) | Eco-Geographical Characterization |
| :--- | :--- | :--- | :--- |
| **Class 1 (Unsuitable)** | 0.93 | 0.07% | Settlement areas, steep rocky cliffs, bare soil |
| **Class 2 (Low)** | 20.31 | 1.51% | High-altitude mountainous terrain, crop zones |
| **Class 3 (Moderate)** | 770.09 | 57.21% | Central canopy core forests, distant from river systems |
| **Class 4 (High)** | 507.58 | 37.71% | Grasslands (Chaurs), open woodland cover, near water sources |
| **Class 5 (Very High)** | 47.08 | 3.50% | River basins, riparian vegetation, perennial streams |

---

## 6. License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
