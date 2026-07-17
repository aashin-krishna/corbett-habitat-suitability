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
