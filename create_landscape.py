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
    if props.cached_openstreetmap_xml:
        return False

    if props.origin_lat != props.cached_origin_lat:
        return True

    if props.origin_lon != props.cached_origin_lon:
        return True

    if props.origin_radius != props.cached_origin_radius:
        return True

    return False


def loadFromServer(props) -> overpy.Result:
    overpass = overpy.Overpass()

    if mustReload(props):
        print('loading from server');

        origin = open_landscape_math.CoordinatePoint(
            props.origin_lat, props.origin_lon)

        bounding_box = open_landscape_math.calculate_bounding_box(
            origin, props.origin_radius)

        query = """
        (
            node
                {bounding_box};
            way
                {bounding_box};
            rel
                {bounding_box};
            );
            (._;>;);
            out;""".format(bounding_box = bounding_box)

        url = 'http://overpass-api.de/api/interpreter'
        with urllib.request.urlopen(url, query.encode("utf-8")) as response:
            overpass_xml = response.read().decode('utf-8')

        print(overpass_xml)

        props.cached_origin_lat = props.origin_lat
        props.cached_origin_lon = props.origin_lon
        props.cached_origin_radius = props.origin_radius
        props.cached_openstreetmap_xml = overpass_xml

        return overpass.parse_xml(overpass_xml)
    else:
        print('using from cache')

        return overpass.parse_xml(props.cached_openstreetmap_xml)


class CreateLandscape(bpy.types.Operator):
    """Create Mesh from OpenStreetmap data"""
    bl_idname = "open_landscape.create"
    bl_label = "Create Landscape"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def execute(self, context: bpy.types.Context):
        scene = context.scene

        overpy_result = loadFromServer(scene.open_landscape_properties)

        object_utils.buildObjects([
            object_utils.OpenLandscapeObject(
                name="Wiese", vertices=[(1, 1, 0), (1, -1, 0), (1, -2, 0), (-1, -2, 0), (-1, -1, 0),
                                        (-1, 1, 0)]),

            object_utils.OpenLandscapeObject(
                name="Wald", vertices=[(4, 4, 0), (4, 2, 0), (2, 2, 0), (2, 4, 0)])
        ])

        return {'FINISHED'}

    def invoke(self, context, event):
        if checkForObjects(context):
            windowManager = context.window_manager

            return windowManager.invoke_popup(self)
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