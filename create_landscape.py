"""Operator to parse the openstreetmap data and create the actual mesh"""
import bpy
import urllib.request
from . import overpy
from . import open_landscape_math
from . import object_utils


def getObjectsInLayer(context: bpy.types.Context):
    activeLayer = context.scene.active_layer
    objectsInLayer = [
        obj for obj in context.scene.objects if obj.layers[activeLayer] and obj.type == 'MESH']

    return objectsInLayer


def checkForObjects(context: bpy.types.Context):
    return len(getObjectsInLayer(context)) > 0


def mustReload(props):
    if props.origin_lat != props.cached_origin_lat:
        return True

    if props.origin_lon != props.cached_origin_lon:
        return True

    if props.origin_radius != props.cached_origin_radius:
        return True

    if props.cached_openstreetmap_xml:
        return False

    return False


def loadFromServer(props) -> overpy.Result:
    overpass = overpy.Overpass()

    if mustReload(props):
        print('OpenLandscape: loading from server...')

        origin = open_landscape_math.CoordinatePoint(
            props.origin_lat, props.origin_lon)

        bounding_box = open_landscape_math.calculate_bounding_box(
            origin, props.origin_radius)

        query = """
        (
            node{bounding_box};
            rel(bn)->.x;
            way{bounding_box};
            node(w)->.x;
        );
        out meta;""".format(bounding_box=bounding_box)

        print('OpenLandscape: Executing query {query}'.format(query=query))

        # rel(bw); We can add this in the join of the query at the end to get all relations

        url = 'http://overpass-api.de/api/interpreter'
        with urllib.request.urlopen(url, query.encode("utf-8")) as response:
            overpass_xml = response.read().decode('utf-8')

        props.cached_origin_lat = props.origin_lat
        props.cached_origin_lon = props.origin_lon
        props.cached_origin_radius = props.origin_radius
        props.cached_openstreetmap_xml = overpass_xml

        print('OpenLandscape: Finished loading from server')

        return overpass.parse_xml(overpass_xml)
    else:
        print('OpenLandscape: Using Data From Cache')

        return overpass.parse_xml(props.cached_openstreetmap_xml)


class CreateLandscape(bpy.types.Operator):
    """Create Mesh from OpenStreetmap data"""
    bl_idname = "open_landscape.create"
    bl_label = "Create Landscape"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context: bpy.types.Context):
        scene = context.scene
        props = scene.open_landscape_properties

        overpy_result = loadFromServer(props)
        origin = open_landscape_math.CoordinatePoint(
            props.origin_lat, props.origin_lon)

        objects = object_utils.build_objects_from_overpass(overpy_result, origin)

        object_utils.buildObjects([o for o in objects if o.draw_as_mesh])

        return {'FINISHED'}

    def invoke(self, context, event):
        if checkForObjects(context):
            window_manager = context.window_manager

            return window_manager.invoke_popup(self)
        else:
            return self.execute(context)

    def draw(self, context):
        layout = self.layout

        layout.label(text="There are object on the active layer.")

        layout.operator('open_landscape.deleteobjects')
        layout.operator('open_landscape.proceedanyway')


class DeleteObjects(bpy.types.Operator):
    """Delete Objects and start creating meshes"""
    bl_idname = "open_landscape.deleteobjects"
    bl_label = "Delete Objects and proceed"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        objectsInLayer = getObjectsInLayer(context)

        bpy.ops.object.select_all(action='DESELECT')

        for obj in objectsInLayer:
            obj.select = True

        bpy.ops.object.delete()
        bpy.ops.open_landscape.create()

        return {'FINISHED'}


class ProceedAnyway(bpy.types.Operator):
    """Don't care about objects and create mesh anyway"""
    bl_idname = "open_landscape.proceedanyway"
    bl_label = "Proceed anyway"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context):
        bpy.ops.open_landscape.create('EXEC_DEFAULT')

        return {'FINISHED'}
