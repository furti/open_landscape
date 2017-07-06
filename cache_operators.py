"""Operators that handle the cached Open Landscape Data"""

import bpy

DATA_FILE_NAME = 'OpenLandscapeData.xml'


class ClearCacheOperator(bpy.types.Operator):
    """Clear the Open Landscape Cached Data"""
    bl_idname = "open_landscape.clear_cache"
    bl_label = "Clear Cached Data"
    bl_options = {"REGISTER"}

    def execute(self, context: bpy.types.Context):
        """Actually clear the cached data"""

        props = context.scene.open_landscape_properties

        props.cached_origin_lat = 0.0
        props.cached_origin_lon = 0.0
        props.cached_origin_radius = 0
        props.cached_openstreetmap_xml = ''

        print('OpenLandscape: Cleared Cached Data')

        return {'FINISHED'}


class ShowCacheOperator(bpy.types.Operator):
    """Clear the Open Landscape Cached Data"""
    bl_idname = "open_landscape.show_cache"
    bl_label = "Show Cached Data"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context: bpy.types.Context):
        xml_data = context.scene.open_landscape_properties.cached_openstreetmap_xml

        if xml_data:
            if bpy.data.texts.find(DATA_FILE_NAME) == -1:
                bpy.ops.text.new()

                bpy.data.texts[-1].name = DATA_FILE_NAME

            bpy.data.texts[DATA_FILE_NAME].from_string(xml_data)
            print('OpenLandscape: See Text Editor for Data')
        else:
            print('OpenLandscape: No Data found in Cache')

        return {'FINISHED'}
