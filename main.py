import subprocess as sb
import os
import geopandas as gpd
from geopandas_postgis import PostGIS
import sqlalchemy

data_dir = './'
target_dir = 'ext'
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)

    if file_name.split('.')[-1]=='zip':
        print(sb.run(['unzip', '-o', file_path, '-d', target_dir], stdout=sb.PIPE, stderr=sb.PIPE))
        
lu_shps = [filename for filename in os.listdir(target_dir) if filename.split('.')[-1]=='shp']

os.chdir(target_dir)
for shp_name in lu_shps:
    print(sb.call(' '.join(['SHAPE_RESTORE_SHX=YES', 'fio', 'info', '"%s"'%shp_name]), shell=True))
os.chdir('..')

seoul_lu = {}
for shp_name in lu_shps:
    data = gpd.read_file(os.path.join(target_dir, shp_name), encoding = 'ms949')
    seoul_lu[shp_name.split('.')[0]] = data.to_crs(epsg=4326)

con = sqlalchemy.create_engine('postgresql://postgres:3096@172.17.0.3:5432/postgres')

for df in seoul_lu.values():
    df.postgis.to_postgis(con, 'seoul_lu', 'geometry', index=False, if_exists='append')