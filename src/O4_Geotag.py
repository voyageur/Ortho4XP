import os
from osgeo import gdal
from pyproj import Transformer
from math import pi, exp, atan

geographic='4326'
webmercator='3857'
transformer = Transformer.from_crs("epsg:" +transformer, "epsg:" + webmercator, always_xy=True)

def gtile_to_wgs84(til_x,til_y,zoomlevel):
    rat_x=(til_x/(2**(zoomlevel-1))-1)
    rat_y=(1-til_y/(2**(zoomlevel-1)))
    lon=rat_x*180
    lat=360/pi*atan(exp(pi*rat_y))-90
    return (lat,lon)

for f in os.listdir():
    if not f[-4:]=='.jpg': continue
    items=f.split('_')
    til_y_top=int(items[0])
    til_x_left=int(items[1])
    zoomlevel=int(items[-1][-6:-4])
    (latmax,lonmin)=gtile_to_wgs84(til_x_left,til_y_top,zoomlevel)
    (latmin,lonmax)=gtile_to_wgs84(til_x_left+16,til_y_top+16,zoomlevel)
    (xmin,ymin)=transformer.transform(lonmin,latmin)
    (xmax,ymax)=transformer.transform(lonmax,latmax)
    gdal.Translate(f.replace(".jpg","_tmp.tif"), f, format="GTiff", creationOptions=["COMPRESS=JPEG"], outputBounds=[xmin, ymax, xmax, ymin], outputSRS="epsg:3857")
    gdal.Warp(f.replace(".jpg",".tif"), f.replace(".jpg","_tmp.tif"), format="GTiff", creationOptions=["COMPRESS=JPEG"], srcSRS="epsg:3857", dstSRS="epsg:4326", width=4096, height=4096, resampleAlg=gdal.GRA_Bilinear)
