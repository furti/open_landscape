import bpy


class OpenLandscapeObject:

    def __init__(self, name="", vertices=None):
        self.name = name
        self.vertices = vertices


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
    bpy.ops.mesh.fill_grid()
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
