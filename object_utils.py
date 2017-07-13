import bpy
from . import overpy
from . import tag_mapping
from . import open_landscape_math


class OpenLandscapeObject:

    def __init__(self, name="", vertices=None, draw_as_mesh=False):
        self.name = name
        self.vertices = vertices
        self.draw_as_mesh = draw_as_mesh


def buildObjects(objects: [OpenLandscapeObject]):
    for object in objects:
        blender_mesh = createMesh(object)
        blender_object = createObject(object, blender_mesh)


def createMesh(object: OpenLandscapeObject):
    mesh = bpy.data.meshes.new(object.name + 'Mesh')

    mesh.from_pydata(object.vertices, calculateEdges(object.vertices), [])
    mesh.validate()
    mesh.update()

    return mesh


def createObject(object: OpenLandscapeObject, blender_mesh: bpy.types.Mesh):
    blender_object = bpy.data.objects.new(object.name, blender_mesh)
    blender_object.location = (0, 0, 0)

    scene = bpy.context.scene

    scene.objects.link(blender_object)
    scene.objects.active = blender_object
    blender_object.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.fill()
    bpy.ops.object.mode_set(mode='OBJECT')

    return blender_object


def calculateEdges(vertices):
    vertexCount = len(vertices)
    zeroBasedVertexIndex = range(vertexCount)
    oneBasedVertexIndex = iter(list(range(1, vertexCount)) + [0])

    # We have two iterators and create tuples out of them
    # [0, 1, 2]
    # [1, 2, 0]
    # Result: First element of iter1 builds tuple with first element of iter2,...
    # [(0,1), (1,2), (2,0)]

    edges = zip(zeroBasedVertexIndex, oneBasedVertexIndex)

    return list(edges)


def calculate_vertex_data(nodes, origin: open_landscape_math.CoordinatePoint):
    node_coordinates = [open_landscape_math.CoordinatePoint(
        float(node.lat), float(node.lon)) for node in nodes]

    vertices = [open_landscape_math.calculate_vector_for_coordinates(
        origin, node_coordinate) for node_coordinate in node_coordinates]

    print(vertices)

    return vertices


def build_objects_from_overpass(overpy_result: overpy.Result, origin: open_landscape_math.CoordinatePoint) -> [OpenLandscapeObject]:
    objects = []

    for way in overpy_result.ways:
        types = tag_mapping.find_type(way.tags)

        if not types:
            print('OpenLandscape: No type mapping found for tags {tags} for object {object_id}'.format(
                tags=way.tags, object_id=way.id))
        else:
            type_to_use = types[0]

            object_name = "{type}-{id}".format(
                type=type_to_use["TYPE"], id=way.id)
            object_vertex = calculate_vertex_data(way.nodes, origin)

            objects.append(OpenLandscapeObject(
                name=object_name, vertices=object_vertex, draw_as_mesh=type_to_use["DRAW_TYPE"] == "plane"))

    return objects
