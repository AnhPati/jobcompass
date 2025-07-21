import requests
import time

USER_AGENT = "YourStreamlitApp/1.0 (anhpati@gmail.com)"

def geocode_location(location_name: str, cache: dict) -> tuple[float | None, float | None]:
    if not isinstance(location_name, str) or not location_name.strip():
        return None, None

    if location_name in cache:
        return cache[location_name]['lat'], cache[location_name]['lon']

    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 0
    }
    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
        else:
            lat = lon = None
    except requests.RequestException:
        lat = lon = None

    cache[location_name] = {'lat': lat, 'lon': lon}
    time.sleep(1)  # Respect API rate limiting
    return lat, lon