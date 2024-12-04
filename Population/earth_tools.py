import ee
import json
import requests
from google.oauth2 import service_account

def total_population_get(dataset, region_of_interest) :
  clipped_dataset = dataset.unmask(0).clip(region_of_interest)

  projection = dataset.projection(); #print(projection.nominalScale())

  total_population = clipped_dataset.reduceRegion(
      scale=projection.nominalScale(),
      reducer=ee.Reducer.sum(),
      geometry=region_of_interest,
      maxPixels=1e9
  )

  population_value = total_population.get('population_count')
  return population_value.getInfo(), clipped_dataset

## 1.0 
service_account_key_file = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file,
    scopes=['https://www.googleapis.com/auth/earthengine',
            'https://www.googleapis.com/auth/cloud-platform']
)

ee.Initialize(credentials)
print("[earth_tools]", ee.String('Earth Engine...').getInfo())

## 2.0. 
geojson_url  = "https://raw.githubusercontent.com/test-earth-engine/gee1/main/Jsons/conflict.geojson"

response = requests.get(geojson_url)
geojson_data = response.json()
print(geojson_data['type']) ## FeatureCollection

geojson_feature = ee.FeatureCollection(geojson_data)
region_of_interest = geojson_feature.geometry()


## 3.0
collection = ee.ImageCollection('CIESIN/GPWv411/GPW_Population_Count') 
available_dates = collection.aggregate_array('system:time_start').map(lambda t: ee.Date(t).format('YYYY-MM-dd'))

population = {} 
json_data = []
for start_date in available_dates.getInfo() : 
  subcollection = collection.filterDate(start_date, None)
  population_value, clipped_dataset = total_population_get(subcollection.first(), region_of_interest)
  print(start_date, population_value) 

  population[start_date] = population_value,clipped_dataset 
  json_data.append({'start_date':start_date, 'population_value':population_value})

## 3.0.
with open('output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4) 

