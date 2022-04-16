import requests
import time

def _apiCall(endpoint):
    url = "https://api.weather.gov" + endpoint
    while True:
        response = requests.get(url)
        try:
            if response.json().get("status") == 500:
                time.sleep(6)
                continue
            else:
                print("got successful response from api")
                break
        except:
            print("no json")
            break
    try:
        return response.json()
    except:
        print("no json")
        return None

def getPoints(lat, lon):
    endpoint = f"/points/{lat},{lon}"
    response = _apiCall(endpoint)
    if response:
        gridId = response.get("properties").get("gridId")
        gridX = response.get("properties").get("gridX")
        gridY = response.get("properties").get("gridY")
        zoneId = response.get("properties").get("forecastZone").split("/")[-1]
        return gridId, gridX, gridY, zoneId
    return None, None, None, None

def getForecast(gridId, gridX, gridY):
    endpoint = f"/gridpoints/{gridId}/{gridX},{gridY}/forecast"
    response = _apiCall(endpoint)
    if response:
        periods = response.get("properties").get("periods")
        return periods
    return None

def getAlerts(zoneId):
    endpoint = f"/alerts/active/zone/{zoneId}"
    response = _apiCall(endpoint)
    if response:
        alerts = [x.get("properties") for x in response.get("features")]
        return alerts
    return None



