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
