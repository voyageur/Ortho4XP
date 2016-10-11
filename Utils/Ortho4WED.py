#!/usr/bin/env python3
from Ortho4XP import *

try:
    icao_code=sys.argv[1]
except:
    print("Syntax: Ortho4WED.py ICAO_CODE ZL")
    print("Example: Ortho4WED.py LFLJ 17")
try:
    zoomlevel=int(sys.argv[2])
except:
    zoomlevel=17
website='BI'

api=overpy.Overpass()
tag='way["icao"="'+icao_code+'"]'
result=get_osm_data(-80,80,-179,179,tag)
try:
    lat=float(result.ways[0].nodes[0].lat)
    lon=float(result.ways[0].nodes[0].lon)
except:
    print("No OSM boundary info found for that airport")
    sys.exit()

latmin=lat
latmax=lat
lonmin=lon
lonmax=lon
for node in result.ways[0].nodes:
    nlat=float(node.lat)
    nlon=float(node.lon)
    if nlat>latmax:
        latmax=nlat
    if nlat<latmin:
        latmin=nlat
    if nlon>lonmax:
        lonmax=nlon
    if nlon<lonmin:
        lonmin=nlon


[til_x_min,til_y_min]=wgs84_to_gtile(latmax+0.0015,lonmin-0.002,zoomlevel)
[til_x_max,til_y_max]=wgs84_to_gtile(latmin-0.0015,lonmax+0.002,zoomlevel)
s=requests.Session()
total_x=(til_x_max+1-til_x_min)
for til_x in range(til_x_min,til_x_max+1):
    for til_y in range(til_y_min,til_y_max+1):
        successful_download=False
        while successful_download==False:
            try:
                [url,fake_headers]=http_requests_form(til_x,til_y,zoomlevel,website)
                r=s.get(url, headers=fake_headers)
                successful_download=True
            except:
                #print("Connexion avortée par le serveur, nouvelle tentative dans 1sec")
                time.sleep(1)
        filename=Ortho4XP_dir+dir_sep+'Previews'+dir_sep+'image-'\
                 +str(til_y-til_y_min).zfill(3)+'-'+\
                  str(til_x-til_x_min).zfill(3)+'.jpg'
        file=open(filename,"wb")
        if ('Response [20' in str(r)):
            file.write(r.content)
        else:
            os.system(copy_cmd+' "'+Ortho4XP_dir+dir_sep+'Utils'+\
                            dir_sep+'white.jpg'+'" "'+filename+'" '+devnull_rdir) 
        file.close()
nx=til_x_max-til_x_min+1
ny=til_y_max-til_y_min+1
os.system(montage_cmd+' -tile '+str(nx)+'x'+str(ny)+\
          ' -geometry 256x256+0+0 "'+Ortho4XP_dir+dir_sep+\
          'Previews'+dir_sep+'image-*.jpg'+'" "'+icao_code+".jpg"+'" '+devnull_rdir)
os.system(delete_cmd+' '+Ortho4XP_dir+dir_sep+'Previews'+\
           dir_sep+'image-*.jpg '+devnull_rdir)

[latmaxphoto,lonminphoto]=gtile_to_wgs84(til_x_min,til_y_min,zoomlevel)
[latminphoto,lonmaxphoto]=gtile_to_wgs84(til_x_max+1,til_y_min+1,zoomlevel)
print("Orthophoto has been saved under "+icao_code+".jpg")
print("You can open it in WED and use the following for anchoring its corners:")
print("Upper left  corner is lat="+str(latmaxphoto)+" lon="+str(lonminphoto))
print("Upper right corner is lat="+str(latmaxphoto)+" lon="+str(lonmaxphoto))
print("Lower left  corner is lat="+str(latminphoto)+" lon="+str(lonminphoto))
print("Lower right corner is lat="+str(latminphoto)+" lon="+str(lonmaxphoto))

