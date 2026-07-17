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
