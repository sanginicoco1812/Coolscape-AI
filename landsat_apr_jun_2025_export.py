"""
Export April-June 2025 Landsat 8/9 NDVI and LST samples for HEATSHIELD INDIA.

This script uses Google Earth Engine. Before running it:

1. Install the dependency:
   pip install earthengine-api

2. Authenticate once:
   earthengine authenticate

3. Export to Google Drive:
   python3 landsat_apr_jun_2025_export.py

   Or download local CSVs directly into datasets/:
   python3 landsat_apr_jun_2025_export.py --local

Exports are sent to Google Drive as CSV files. Download the finished CSVs
from Drive into datasets/ if you want to retrain models or regenerate maps.
"""

import argparse
from pathlib import Path

import ee
import requests


START_DATE = "2025-04-01"
END_DATE = "2025-07-01"  # exclusive, so this includes all of June 2025
SCALE_METERS = 30
SAMPLE_POINTS_PER_CITY = 1200
DRIVE_FOLDER = "heatshield_landsat_apr_jun_2025"
DATASETS_DIR = Path("datasets")
SELECTORS = [
    "City",
    "Source",
    "StartDate",
    "EndDate",
    "Latitude",
    "Longitude",
    "NDVI",
    "LST",
]


CITY_BOUNDS = {
    "Delhi": [76.75, 28.20, 77.65, 29.10],
    "Mumbai": [72.75, 18.85, 73.10, 19.35],
    "Hyderabad": [78.20, 17.20, 78.70, 17.60],
    "Bengaluru": [77.35, 12.75, 77.85, 13.20],
}


def mask_landsat_clouds(image):
    """Mask cloud, cloud shadow, snow, and cirrus using QA_PIXEL bits."""
    qa = image.select("QA_PIXEL")
    fill = qa.bitwiseAnd(1 << 0).eq(0)
    cirrus = qa.bitwiseAnd(1 << 2).eq(0)
    cloud = qa.bitwiseAnd(1 << 3).eq(0)
    shadow = qa.bitwiseAnd(1 << 4).eq(0)
    snow = qa.bitwiseAnd(1 << 5).eq(0)
    return image.updateMask(fill.And(cirrus).And(cloud).And(shadow).And(snow))


def add_indices(image):
    """Add NDVI and land surface temperature in Celsius."""
    optical = image.select(["SR_B4", "SR_B5"]).multiply(0.0000275).add(-0.2)
    red = optical.select("SR_B4")
    nir = optical.select("SR_B5")
    ndvi = nir.subtract(red).divide(nir.add(red)).rename("NDVI")

    lst_celsius = image.select("ST_B10").multiply(0.00341802).add(149.0).subtract(273.15)
    lst_celsius = lst_celsius.rename("LST")

    return image.addBands([ndvi, lst_celsius])


def landsat_collection(region):
    landsat_8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    landsat_9 = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")

    return (
        landsat_8.merge(landsat_9)
        .filterBounds(region)
        .filterDate(START_DATE, END_DATE)
        .map(mask_landsat_clouds)
        .map(add_indices)
    )


def export_city_samples(city, region):
    collection = landsat_collection(region)

    composite = (
        collection.select(["NDVI", "LST"])
        .median()
        .clip(region)
        .set(
            {
                "city": city,
                "source": "Landsat 8/9 Collection 2 Level 2",
                "start_date": START_DATE,
                "end_date": "2025-06-30",
            }
        )
    )

    lon_lat = ee.Image.pixelLonLat().rename(["Longitude", "Latitude"])
    export_image = composite.addBands(lon_lat)

    samples = export_image.sample(
        region=region,
        scale=SCALE_METERS,
        numPixels=SAMPLE_POINTS_PER_CITY,
        seed=404,
        geometries=True,
        tileScale=4,
    ).map(
        lambda feature: feature.set(
            {
                "City": city,
                "Source": "Landsat 8/9 Collection 2 Level 2",
                "StartDate": START_DATE,
                "EndDate": "2025-06-30",
            }
        )
    )

    task = ee.batch.Export.table.toDrive(
        collection=samples,
        description=f"{city}_Landsat_Apr_Jun_2025_NDVI_LST",
        folder=DRIVE_FOLDER,
        fileNamePrefix=f"{city}_Landsat_Apr_Jun_2025_NDVI_LST",
        fileFormat="CSV",
    )
    task.start()
    print(f"Started export for {city}: {task.id}")


def download_city_samples(city, region):
    collection = landsat_collection(region)

    composite = (
        collection.select(["NDVI", "LST"])
        .median()
        .clip(region)
    )
    lon_lat = ee.Image.pixelLonLat().rename(["Longitude", "Latitude"])
    export_image = composite.addBands(lon_lat)

    samples = export_image.sample(
        region=region,
        scale=SCALE_METERS,
        numPixels=SAMPLE_POINTS_PER_CITY,
        seed=404,
        geometries=False,
        tileScale=4,
    ).map(
        lambda feature: feature.set(
            {
                "City": city,
                "Source": "Landsat 8/9 Collection 2 Level 2",
                "StartDate": START_DATE,
                "EndDate": "2025-06-30",
            }
        )
    )

    download_url = samples.getDownloadURL(
        filetype="csv",
        selectors=SELECTORS,
        filename=f"{city}_Landsat_Apr_Jun_2025_NDVI_LST",
    )

    response = requests.get(download_url, timeout=120)
    response.raise_for_status()

    DATASETS_DIR.mkdir(exist_ok=True)
    output_path = DATASETS_DIR / f"{city}_Landsat_Apr_Jun_2025_NDVI_LST.csv"
    output_path.write_bytes(response.content)
    print(f"Downloaded {city}: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Export April-June 2025 Landsat NDVI/LST samples."
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Download CSV files directly into datasets/ instead of starting Drive export tasks.",
    )
    args = parser.parse_args()

    ee.Initialize()

    for city, bounds in CITY_BOUNDS.items():
        region = ee.Geometry.Rectangle(bounds)
        if args.local:
            download_city_samples(city, region)
        else:
            export_city_samples(city, region)

    if args.local:
        print("\nLocal Landsat CSV downloads completed.")
    else:
        print("\nExports started.")
        print(f"Check Google Drive folder: {DRIVE_FOLDER}")
        print("Then download the CSV files into datasets/.")


if __name__ == "__main__":
    main()
