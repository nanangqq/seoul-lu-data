import subprocess as sb
import os
import geopandas as gpd
from geopandas_postgis import PostGIS

data_dir = './'
target_dir = 'ext'
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

logs = []
for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)

    if file_name.split('.')[-1]=='zip':
        logs.append(sb.run(['unzip', '-o', file_path, '-d', target_dir], stdout=sb.PIPE, stderr=sb.PIPE))
        
lu_shps = [filename for filename in os.listdir(target_dir) if filename.split('.')[-1]=='shp']

seoul_lu = {}
for shp_name in lu_shps:
    data = gpd.read_file(os.path.join(target_dir, shp_name), encoding = 'ms949')
    print(data.crs)
    seoul_lu[shp_name.split('.')[0]] = data

