import csv
from geographiclib.geodesic import Geodesic

AIRPORTS = {}

with open("airports.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        AIRPORTS [row["ident"]] = {
        "type": row["type"],
        "name": row["name"],
        "latitude": float(row["latitude_deg"]),
        "longitude": float(row["longitude_deg"]),
        "elevation": int(row["elevation_ft"]) if row["elevation_ft"] else 0,
        "continenent": row["continent"],
        "iso_country": row["iso_country"],
        "iso_region": row["iso_region"],
        "municipality": row["municipality"],
        "scheduled_service": row["scheduled_service"],
        "icao_code": row["icao_code"],
        "iata_code": row["iata_code"],
        "gps_code": row["gps_code"],
        "local_code": row["local_code"],
        "link": row["home_link"],
        "wikipedia": row["wikipedia_link"],
        "keywords": row["keywords"]
    }

def calculate_route(airports: list[str]):
    if len(airports) < 2:
        return "Must have at least 2 airports"
    
    legs = []
    total_distance = 0
    
    for i in range(len(airports) - 1):
        dep = AIRPORTS[airports[i]]
        arr = AIRPORTS[airports[i + 1]]
        g = Geodesic.WGS84.Inverse(dep["latitude"], dep["longitude"], arr["latitude"], arr["longitude"])
        dist_nm = g["s12"] / 1852
        bearing = g["azi1"]
        
        legs.append({
            "from": airports[i],
            "to": airports[i + 1],
            "distance_nm": round(dist_nm, 1),
            "bearing": round(bearing, 1)
        })
        
        total_distance += dist_nm
        
    return {
        "route": airports,
        "leg": legs,
        "total_distance_nm": round(total_distance, 1)
    }
    
if __name__ == "__main__":
    print(calculate_route(["KMBT", "KBNA", "KMEM"]))