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
from marley.utils.ipstartup import *
from marley import *
from marley.tif import getdf
from marley.pandas import *
import rasterio
import plotly.express as px
import geopandas as gpd
from geopy.distance import EARTH_RADIUS, geodesic
from sklearn.cluster import DBSCAN
os.chdir(c.localpath)
popfile = "grid3/GRID3_NGA_PopEst_v1_1_mean_float.tif"
lightsfile = "grid3/lights.tif"
f = rasterio.open(popfile)

# %% [markdown]
# # archive and todo

# %%
# latlon model. takes 10+ times longer
eps = 1.5 / EARTH_RADIUS
x = unlit[["lat", "lon"]].values
m = DBSCAN(eps=eps, min_samples=4000, algorithm='ball_tree', metric='haversine', n_jobs=-1)
label = m.fit_predict(np.radians(x), sample_weight=weights)
df.label.update(pd.Series(label, index=unlit.index))
df.label = df.label.astype(int)

# %%
# colors for different clusters (now use bounds instead)
dfc["color"] = np.random.randint(1,12,len(dfc))
# setting unlit first is faster
unlit["color"] = unlit.label.map(dfc.color)
df["label"] = unlit["label"]
df["color"] = unlit["color"]
out = df["color"].values.reshape(f.shape).astype(np.int32)
profile=rasterio.open(popfile).profile
profile["dtype"] = "int32"
del profile["nodata"]
with rasterio.open("popcolors.tif", "w", **profile) as f:
    f.write(out,1)

# %%
# %%s
# 4 colors clear sepration but slow and memory issues
get_color(unlit, inplace=True)

# %%
from shapely.geometry import Point, Polygon, MultiPoint
c = unlit[unlit.label==0]

# %%
unlit = unlit[unlit.label>=0]

# %%
dfc.apply()

# %%
dfc.apply(lambda x: gpd.GeoSeries(MultiPoint(list(zip(x.lon, x.lat))).convex_hull), axis=1)

# %%

# %%
gpd.GeoSeries(hull)

# %%
7.91666660299415e-05*(6371/360)**2

# %%
0.9789229598633893/7.91666660299415e-05

# %%
px.scatter(x=c0.col, y=-c0.row)

# %%
px.scatter(x=c0.lon, y=c0.lat)

# %%
mp.convex_hull.area

# %%
points = [Point(row, col) for row,col in rawpoints]
mp = MultiPoint(points)
d(mp.convex_hull, mp.envelope)

# %%
## add envelopes to dfc
#unlit = unlit[unlit.label>=0]
#geom = unlit.groupby("label").apply(lambda x: gpd.GeoSeries(gpd.points_from_xy(x.lon,x.lat).envelope)).values
gdf = gpd.GeoDataFrame(dfc)
#gdf["geometry"] = geom
gdf

# %%
# add points
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

# %%
# get outer border. 
gdf[gdf.label==3]

# %%
#points = [Point(r.row, r.col) for i, r in gdf[gdf.label==3].iterrows()]
points = [Point(row, col) for row,col in [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]]
coords = sum(map(list, (p.coords for p in points)), [])
poly = Polygon(coords)
poly.

# %%
