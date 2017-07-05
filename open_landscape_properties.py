"""Define and register all properties used by OpenLandscape"""

import bpy

class OpenLandscapeProperties(bpy.types.PropertyGroup):
    """Define all properties used by OpenLandscape"""

    origin_lat = bpy.props.FloatProperty(
        name="Latitude",
        description="Enter the origins Latitude",
        default=48.422954,
        min=-90,
        max=90,
        precision=6)

    origin_lon = bpy.props.FloatProperty(
        name="Longitude",
        description="Enter the origins Longitude",
        default=14.828898,
        min=-180,
        max=180,
        precision=6)

    origin_radius = bpy.props.IntProperty(
        name="Radius",
        description="Enter the radius around the origin in meters",
        default=50,
        min=10,
        max=500)

    cached_origin_lat = bpy.props.FloatProperty(
        name="CachedLatitude",
        min=-90,
        max=90,
        precision=6)

    cached_origin_lon = bpy.props.FloatProperty(
        name="CachedLongitude",
        min=-180,
        max=180,
        precision=6)

    cached_origin_radius = bpy.props.IntProperty(
        name="CachedRadius",
        min=10,
        max=500)

    cached_openstreetmap_xml = bpy.props.StringProperty(
        name="CachedOpenstreetmapData")
