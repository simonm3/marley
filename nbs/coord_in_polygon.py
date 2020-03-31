# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import gdrive
#install googledrivedownloader if gdrive error
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon
shapely.speedups.enable()
import geopandas
from geopandas import GeoDataFrame

# %%
from marley.creds import *
import fs
gd = fs.open_fs(f"googledrive://{gdrive()}")
link = "https://drive.google.com/open?id=1KT0eZvx3ila1_H0W5rzEocY7UJJPwsIE"

# %%
#download cluster file from gdrve https://drive.google.com/file/d/1KT0eZvx3ila1_H0W5rzEocY7UJJPwsIE/view?usp=sharing
gdrive.download_drive(file_id='1TBqz1x1qQEZGazwOPu0BnLgoo_G4j736',
                   dest_path = 'data/clusters_priority.xlsx')

# %%
#download LGA shape file from https://drive.google.com/file/d/1vq22_NO2yXB57MB4hUYcN4wXqFiygvqw/view?usp=sharing
gdrive.download_drive(file_id = '1vq22_NO2yXB57MB4hUYcN4wXqFiygvqw',
                     dest_path = 'data/nga_adm_osgof_20190417_shp.zip',
                     unzip=True)

# %%

# %%
clusters = pd.read_excel("data/clusters_priority.xlsx")
clusters.tail()

# %%
points = []
for lat, lon in zip(clusters['lat'],clusters['lon']):
    p = Point(lon,lat)
    points.append(p)

# %%
poly = geopandas.GeoDataFrame.from_file('data/nga_adm_osgof_20190417_shp/nga_admbnda_adm2_osgof_20190417.shp')
poly = poly[['ADM1_EN','ADM2_EN','geometry']]
poly

# %%
location = []
for point in points:
    for adm1,adm2,po in zip(poly['ADM1_EN'],poly['ADM2_EN'],poly['geometry']):
        if po.contains(point)==True:
            adm = adm2+','+adm1
            location.append(adm)

# %%
location = pd.DataFrame(location)
location.columns = ['adm']

# %%
clusters = clusters.merge(location, left_index=True, right_index=True, how='inner')

# %%
clusters.head()

# %%
clusters.to_excel("data/clusters_priority_adm2.xlsx",index=False)

# %%
clusterbyadm = clusters.groupby(['adm'])[['population']].sum().reset_index()
clusterbyadm.sort_values(by='population',ascending=False)

# %%
clusters[['population','area','density']].describe()

# %%
