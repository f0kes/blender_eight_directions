import bpy


class MultiDirPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""

    bl_label = "8 Directions Panel"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text="Import base model:")
        row = layout.row()
        row.operator("object.import_base_model")

        layout.label(text="Import animation:")
        row = layout.row()
        row.operator("object.import_animation")

        # Create a simple row.
        layout.label(text=" Render:")
        row = layout.row()
        row.operator("object.render_8_directions")
