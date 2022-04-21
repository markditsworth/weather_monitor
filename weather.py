import nws
import os
import json
from datetime import datetime

class Weather:
    def __init__(self, latitude, longitude, location_file="location.json"):
        self.lat = latitude
        self.lon = longitude
        self.location_file = location_file
        self.gridId, self.gridX, self.gridY, self.zoneId = self.getLocationInfo()
        self.DAYS = [
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday"
        ]
    
    def getLocationInfo(self):
        files = os.listdir(".")
        if self.location_file in files:
            lat, lon, gridId, gridX, gridY, zoneId = self.read_location()
            if lat == self.lat and lon == self.lon:
                return gridId, gridX, gridY, zoneId
        
        # get from API
        gridId, gridX, gridY, zoneId = nws.getPoints(self.lat, self.lon)
        self.store_location(gridId, gridX, gridY, zoneId)
        return gridId, gridX, gridY, zoneId

    def store_location(self, gridId, gridX, gridY, zoneId):
        data = {
            "latitude": self.lat,
            "longitude": self.lon,
            "gridId": gridId,
            "gridX": gridX,
            "gridY": gridY,
            "zoneId":zoneId
        }
        with open(self.location_file, "w") as fObj:
            json.dump(data, fObj)
    
    def read_location(self):
        with open(self.location_file, "r") as fObj:
            data = json.load(fObj)

        return (
            data["latitude"],
            data["longitude"],
            data["gridId"],
            data["gridX"],
            data["gridY"],
            data["zoneId"]
        )

    def getForecast(self):
        forecasts = []
        today = None
        forecast_periods = nws.getForecast(self.gridId, self.gridX, self.gridY)
        if forecast_periods:
            for period in forecast_periods:
                name = period.get("name").lower().split(" ")[0]
                if today is None:
                    if name in self.DAYS:
                        today = name
                    else:
                        continue
                else:
                    if name != today:
                        break
                    
                forecast = {
                    "@timestamp": str(datetime.utcnow()),
                    "name": period.get("name"),
                    "temp": period.get("temperature"),
                    "windSpeed": period.get("windSpeed"),
                    "windDirection": period.get("windDirection"),
                    "shortForecast": period.get("shortForecast"),
                }
                forecasts.append(forecast)
        return forecasts
    
    def getAlerts(self):
        alerts = []
        _alerts = nws.getAlerts(self.zoneId)
        if _alerts:
            for alert in _alerts:
                info = {
                    "event": alert.get("event"),
                    "severity": alert.get("severity"),
                    "certainty": alert.get("certainty"),
                    "urgency": alert.get("urgency"),
                    "response": alert.get("response"),
                    "@timestamp": str(datetime.utcnow())
                }
                alerts.append(info)
        print(f"alerts: {alerts}")
        return alerts


    
                
                
        


