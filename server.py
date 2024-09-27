from flask import Flask, request, jsonify, Response
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
import pandas as pd
import os
import json

app = Flask(__name__)

transformer = Transformer.from_crs("EPSG:4326", "EPSG:5186", always_xy=True)


def load_all_shp():
    shapefile_directory = "gis" 
    gdf_list = []
    for folder_name in os.listdir(shapefile_directory):
        folder_path = os.path.join(shapefile_directory, folder_name)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".shp"):
                    filepath = os.path.join(folder_path, file)
                    gdf = gpd.read_file(filepath)
                    gdf_list.append(gdf)
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    merged_gdf = merged_gdf.rename(columns={'SGG_NM': 'region_name'}) 
    return merged_gdf
def load_region_info():
    df = pd.read_csv('region.csv')
    name_id_dict = pd.Series(df.id.values, index=df.name).to_dict()
    print('[성공] 지역 정보 불러오기 성공')
    return name_id_dict

merged_gdf = load_all_shp()
region_dict = load_region_info()

def find_district(lon, lat):
    transformed_x, transformed_y = transformer.transform(lon, lat)
    point = Point(transformed_x, transformed_y)

    matched_area = merged_gdf[merged_gdf.contains(point)]
    if not matched_area.empty:
        district_name = matched_area.iloc[0]['region_name']
        return district_name
    else:
        return None

@app.route('/find_district', methods=['GET'])
def find_district_api():
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))

    region_name = find_district(lon, lat)
    if region_name:
        region_id = region_dict[region_name]
    else:
        region_id = None
    response_data = {'region': region_name, "region_id": region_id}
    response_json = json.dumps(response_data, ensure_ascii=False)
    return Response(response=response_json, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3030)