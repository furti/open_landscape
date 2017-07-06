"""Register Addon in Blender"""

bl_info = {
    "name": "Open Landscape",
    "description": "Create Landscapes from OpenStreetMap data",
    "author": "Daniel Furtlehner",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "location": "View3D > Tool Shelf > Open Landscape",
    "category": "Add Mesh"
}

import sys
from . import create_landscape
from . import open_landscape_properties
from . import open_landscape_ui
from . import open_landscape_math
from . import cache_operators

if 'bpy' in sys.modules:
    import importlib

    importlib.reload(create_landscape)
    importlib.reload(open_landscape_properties)
    importlib.reload(open_landscape_ui)
    importlib.reload(open_landscape_math)

    print("OpenLandscape: Reloaded modules")

import bpy

def register():
    """Register the addon"""
    bpy.utils.register_class(create_landscape.ProceedAnyway)
    bpy.utils.register_class(create_landscape.DeleteObjects)
    bpy.utils.register_class(cache_operators.ClearCacheOperator)
    bpy.utils.register_class(cache_operators.ShowCacheOperator)
    bpy.utils.register_class(create_landscape.CreateLandscape)
    bpy.utils.register_class(open_landscape_properties.OpenLandscapeProperties)
    bpy.utils.register_class(open_landscape_ui.OpenLandscapeOriginPanel)

    bpy.types.Scene.open_landscape_properties = bpy.props.PointerProperty(
        type=open_landscape_properties.OpenLandscapeProperties)


def unregister():
    """Remove the addon"""
    del bpy.types.Scene.open_landscape_properties

    bpy.utils.unregister_class(open_landscape_ui.OpenLandscapeOriginPanel)
    bpy.utils.unregister_class(
        open_landscape_properties.OpenLandscapeProperties)
    bpy.utils.unregister_class(create_landscape.CreateLandscape)
    bpy.utils.unregister_class(cache_operators.ClearCacheOperator)
    bpy.utils.unregister_class(cache_operators.ShowCacheOperator)
    bpy.utils.unregister_class(create_landscape.DeleteObjects)
    bpy.utils.unregister_class(create_landscape.ProceedAnyway)


if __name__ == "__main__":
    register()
