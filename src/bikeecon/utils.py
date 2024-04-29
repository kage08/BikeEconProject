import pickle

from geopy.geocoders import Nominatim


def get_boroughs(file="data/Boroughs.txt") -> list[str]:
    with open(file) as f:
        return f.read().splitlines()


def get_lat_long_from_address(address):
    geolocator = Nominatim(user_agent="get_lat_long1")
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None, None


def get_borough_from_location(latitude, longitude) -> str:
    geolocator = Nominatim(user_agent="get_borough1")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw["address"]
    print(address)
    if "city_district" in address:
        borough = address["city_district"]
    elif "quarter" in address:
        borough = address["quarter"]
    elif "borough" in address:
        borough = address["borough"]
    elif "suburb" in address:
        borough = address["suburb"]
    else:
        borough = address["city"]
    if borough.startswith("London Borough of "):
        borough = borough.replace("London Borough of ", "")
    return borough


def get_borough_from_address(address):
    with open("data/borough_cache.pkl", "rb") as f:
        cache = pickle.load(f)
    if address in cache:
        return cache[address]
    latitude, longitude = get_lat_long_from_address(address)
    borough = get_borough_from_location(latitude, longitude)
    cache[address] = borough
    with open("data/borough_cache.pkl", "wb") as f:
        pickle.dump(cache, f)
    return borough


if __name__ == "__main__":
    # Example usage
    address = "Pancras Road, King's Cross"
    latitude, longitude = get_lat_long_from_address(address)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    borough = get_borough_from_location(latitude, longitude)
    print("Borough:", borough)
    with open("data/borough_cache.pkl", "wb") as f:
        pickle.dump({address: borough}, f)
