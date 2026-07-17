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
