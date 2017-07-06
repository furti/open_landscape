"""Defines the ui for the addon in blender"""
import bpy

print("blub")


class OpenLandscapeToolPanel:
    """Base Class for Panels inside the Tool Shelf"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = "TOOLS"
    bl_category = 'Open Landscape'


class OpenLandscapeOriginPanel(OpenLandscapeToolPanel, bpy.types.Panel):
    """Panel in the Tool Shelf"""
    bl_idname = "open_landscape_origin_panel"
    bl_label = "Origin"

    def draw(self, context):
        """Called on redraw"""
        layout = self.layout
        scene = context.scene

        layout.prop(scene.open_landscape_properties, 'origin_lat')
        layout.prop(scene.open_landscape_properties, 'origin_lon')
        layout.prop(scene.open_landscape_properties, 'origin_radius')
        layout.operator('open_landscape.create')

        if scene.open_landscape_properties.cached_openstreetmap_xml:
            layout.operator('open_landscape.clear_cache')
            layout.operator('open_landscape.show_cache')
