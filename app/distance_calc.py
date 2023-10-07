import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_distance(lat, long, input_latitude, input_longitude):
    return haversine_distance(float(lat), float(long), input_latitude, input_longitude)

def producers_number(dataset, distance): 
    dict_result = {}
    dict_result[distance] = dataset[dataset.distance <= distance].__len__()
    return dict_result