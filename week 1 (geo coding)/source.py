import requests
import json

base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="

print("장소 검색 : " , end=' ')
location = str(input())
key = "please type your api key"
url = base_url+location+key
resp = requests.get(url)


content =  resp.json()

address =  content["results"][0]["formatted_address"]
latitude = float (content["results"][0]["geometry"]["location"]["lat"])
lng = float(content["results"][0]["geometry"]["location"]["lng"])

print(f"장소 검색 {location} 입니다.")
print(f"위도는 {latitude} 입니다.")
print(f"경도는 {lng} 입니다.")
print(f"주소는 {address} 입니다.")

