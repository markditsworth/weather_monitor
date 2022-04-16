from weather import Weather
import emailer
import json
import os
import sys

def createForecastMessage(forecasts):
    message = "Weather Forecast\n"
    for forecast in forecasts:
        m = f"""
        {forecast['name']}
        {forecast['shortForecast']}
        Temperature: {forecast['temp']}F
        Wind: {forecast['windSpeed']} {forecast['windDirection']}
        """
        message += m
    return message

def createAlertMessage(alerts):
    message = ""
    for alert in alerts:
        m = f"""WEATHER ALERT - {alert['severity']}
        {alert['event']}
        Urgency: {alert['urgency']}
        Certainty: {alert['certainty']}
        Recommended Action: {alert['response']}

        """
        message += m
    return message

def dedupeAlerts(alerts):
    deduped_alerts = []
    local_files = os.listdir("./ALERTS")
    keep_list = []
    for alert in alerts:
        name = alert["event"]
        if name in local_files:
            keep_list.append(name)
        else:
            deduped_alerts.append(alert)
            # create file
            f = open(f"ALERTS/{name}")
            f.close()

    for f in local_files:
        if f not in keep_list:
            # delete file
            os.remove(f"ALERTS/{f}")
    print(deduped_alerts)
    return deduped_alerts
    
def main(config_file, action):
    assert action in ["forecast", "alerts"]

    with open(config_file) as fObj:
        configs = json.load(fObj)
    
    lat, lon = configs["lat_lon"].split(",")
    notification_address = configs["contact"]
    email = configs["email"]
    password = configs["password"]

    weather = Weather(lat, lon)
    if action == "forecast":
        forecasts = weather.getForecast()
        message = createForecastMessage(forecasts)
    
    else:
        try:
            os.mkdir("ALERTS")
        except FileExistsError:
            pass
        alerts = weather.getAlerts()
        message = createAlertMessage(dedupeAlerts(alerts))
    
    if message:
        result = emailer.sendMail(
            to_addr=notification_address,
            from_addr=email,
            auth_password=password,
            body=message
        )
        assert not result
    else:
        print("empty message. no notification.")

if __name__ == "__main__":
    config_file = None
    action = None
    args = sys.argv
    while args:
        if args[0] == "--config":
            config_file = args[1]
        elif args[0] == "--alerts":
            action = "alerts"
        elif args[0] == "--forecast":
            action = "forecast"
        args = args[1:]
    
    main(config_file, action)
