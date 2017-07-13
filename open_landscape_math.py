import math
import mathutils

EARTH_RADIUS_IN_METRES = 6371000


class CoordinatePoint:
    """Defines a point on the globe"""
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


def calculate_bounding_box(origin: CoordinatePoint, radius: int) -> (float, float, float, float):
    """Calculates the Bounding Box for the Overpass API"""

    upper_right = point_from_distance_and_angle(origin, radius, 45)
    lower_left = point_from_distance_and_angle(origin, radius, 225)

    return (lower_left.latitude, lower_left.longitude, upper_right.latitude, upper_right.longitude)


def point_from_distance_and_angle(point: CoordinatePoint, distance_in_m: float,
                                  angle_in_degrees: int) -> CoordinatePoint:
    """Calculates a point with the given angle and distance meters away from the given point"""

    lat1 = math.radians(point.latitude)
    lon1 = math.radians(point.longitude)

    distance = distance_in_m / 1000 / 6371
    angle = math.radians(angle_in_degrees)

    lat2 = math.asin(math.sin(lat1) * math.cos(distance) +
                     math.cos(lat1) * math.sin(distance) * math.cos(angle))
    lon2 = lon1 + math.asin((math.sin(distance) /
                             math.cos(lat2)) * math.sin(angle))

    return CoordinatePoint(latitude=math.degrees(lat2), longitude=math.degrees(lon2))


def calculate_vector_for_coordinates(origin: CoordinatePoint, destination: CoordinatePoint) -> mathutils.Vector:
    distance = distance_between_points(origin, destination)
    angle = angle_between_points(origin, destination)

    angle = convert_angle_to_cartesian(angle)

    angle_in_radians = math.radians(angle)

    x = distance * math.cos(angle_in_radians)
    y = distance * math.sin(angle_in_radians)

    return mathutils.Vector((x, y, 0))


def distance_between_points(origin: CoordinatePoint, destination: CoordinatePoint) -> float:
    origin_lat = math.radians(origin.latitude)
    destination_lat = math.radians(destination.latitude)
    delta_lat = math.radians(destination.latitude - origin.latitude)
    delta_lon = math.radians(destination.longitude - origin.longitude)

    half_chord_length = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + \
        math.cos(origin_lat) * math.cos(destination_lat) * math.sin(delta_lon / 2) * \
        math.sin(delta_lon / 2)
    angular_distance = 2 * \
        math.atan2(math.sqrt(half_chord_length),
                   math.sqrt(1 - half_chord_length))

    return EARTH_RADIUS_IN_METRES * angular_distance


def angle_between_points(origin: CoordinatePoint, destination: CoordinatePoint) -> float:
    origin_lat = math.radians(origin.latitude)
    destination_lat = math.radians(destination.latitude)
    delta_lon = math.radians(destination.longitude - origin.longitude)

    y = math.sin(delta_lon) * math.cos(destination_lat)
    x = math.cos(origin_lat) * math.sin(destination_lat) - \
        math.sin(origin_lat) * math.cos(destination_lat) * math.cos(delta_lon)
    angle = math.atan2(y, x)

    return (math.degrees(angle) + 360) % 360

def convert_angle_to_cartesian(angle: float) -> float:
    if angle <= 90:
        return 90 - angle

    if 90 < angle <= 180:
        return 360 - (angle - 90)

    if 180 < angle <= 270:
        return 270 - (angle - 180)

    if angle > 270:
        return 180 - (angle - 270)