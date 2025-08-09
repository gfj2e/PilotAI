import requests

# Updated to use the new API endpoint
METAR_URL = "https://aviationweather.gov/api/data/metar"
TAF_URL = "https://aviationweather.gov/api/data/taf"
HEADERS = {
    "User-Agent": "PilotAI/1.0 (contact: gfj2e@outlook.com)",
    "Accept": "application/json",
}

def get_metar(icao_id: str) -> dict[str, any]:
    params = {
        "ids": icao_id,
        "format": "json",
        "hours": 2,
    }

    response = requests.get(METAR_URL, params=params, headers=HEADERS, timeout=10)
    print(response.url)
    response.raise_for_status()
    data = response.json()

    if not data:
        return f"No METAR for {icao_id}"

    metar = data[0]
    wind = (
        f"{metar.get('wgst', metar.get('wspd'))}kt @ {metar.get('wdir')}"
        if metar.get('wspd') is not None and metar.get('wdir') is not None
        else "null"
    )
    
    cloud_layers = []
    if 'clouds' in metar and metar['clouds']:
        for cloud in metar['clouds']:
            cover = cloud.get('cover', '')
            base = cloud.get('base', '')
            if cover and base: 
                cloud_layers.append(f"{cover}{base}")
                
    cloud_str = " ".join(cloud_layers) if cloud_layers else "SKC"
                
    parsed_data: dict[str, any] = {
        "raw_metar": metar.get("rawOb", "null"),
        "wind": wind,
        "visibility": f"{metar.get('visib', "null")}sm",
        "temperature": f"{metar.get("temp", "null")}",
        "dew_point": f"{metar.get("dewp", "null")}",
        "altimeter": metar.get("altim", "null"),
        "flight_category": metar.get('flight_category', "null"),
        "cloud_coverage": cloud_str,
        "ceiling": get_ceiling(metar)
    }
    
    return parsed_data

def get_ceiling(metar: dict[str, any]) -> str:
    if not metar.get('clouds'):
        return "unlimited"
    
    for cloud in metar['clouds']:
        if cloud.get('cover') in ['BKN', 'OVC'] and cloud.get('base'):
            return f"{cloud['base']}ft"

    return "unlimited"

def get_taf(icao_id: str) -> dict[str, any]:
    params = {
        "ids": icao_id,
        "format": "json",
        "hours": 24,
    }
    
    response = requests.get(TAF_URL, params=params, headers=HEADERS, timeout=10)
    print(response.url)
    response.raise_for_status()
    data = response.json()
    
    if not data:
        return f"No TAF for {icao_id}"

    taf = data[0]
    
    forecasts = []
    if 'fcsts' in taf and taf['fcsts']:
        for period in taf['fcsts']:
            fcst_period = {
                "time_from": period.get("timeFrom"),
                "time_to": period.get("timeFrom"),
                "change_indicator": period.get("fcstChange", "null"),
                "wind": f"{period.get("wspd", "null")}kt @ {period.get("wdir", "null")}",
                "visibility": f"{period.get("visib", "null")}sm",
                "wx_string": period.get("wxString", "null")
            }
            
            cloud_layers = []
            if 'clouds' in period and period['clouds']:
                for cloud in period['clouds']:
                    cover = cloud.get('cover', '')
                    base = cloud.get('base', '')
                    if cover and base: 
                        cloud_layers.append(f"{cover}{base}")
                        
            fcst_period["cloud"] = " ".join(cloud_layers) if cloud_layers else "SKC"
            forecasts.append(fcst_period)
            
        parsed_data = {
            "raw_taf": taf.get("rawTAF", "null"),
            "station": taf.get("icaoId", icao_id),
            "issue_time": taf.get("issueTime", "null"),
            "bulletin_time": taf.get("bulletinTime", "null"),
            "valid_time_from": taf.get("validTimeFrom", "null"),
            "valid_time_to": taf.get("validTimeTo", "null"),
            "forecast_periods": forecasts
        }
        
        return parsed_data

if __name__ == "__main__":
    print(get_taf("KBNA"))