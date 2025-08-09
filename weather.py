import requests

# Updated to use the new API endpoint
NOAA_BASE_URL = "https://aviationweather.gov/api/data/metar"
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

    resp = requests.get(NOAA_BASE_URL, params=params, headers=HEADERS, timeout=15)
    print(resp.url)
    resp.raise_for_status()
    data = resp.json()

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

if __name__ == "__main__":
    print(get_metar("KMBT"))