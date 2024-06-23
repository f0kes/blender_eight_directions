import bpy
import bpy_extras
from bpy.props import StringProperty, BoolProperty, EnumProperty


# ImportHelper
class ImportBaseOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.import_base_model"
    bl_label = "Import Base Model"
    bl_options = {"REGISTER", "UNDO"}

    import_ext = ".fbx"
    filter_glob: StringProperty(
        default="*.fbx",
        options={"HIDDEN"},
    )  # type: ignore

    def import_fbx(self, context, filepath):
        models: set[bpy.types.Object] = set_diff(
            context, lambda: bpy.ops.import_scene.fbx(filepath=filepath)
        )
        context.scene.source_properties.source_object = models.pop()
        return {"FINISHED"}

    def execute(self, context):
        return self.import_fbx(context, self.filepath)


class ImportAnimationOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.import_animation"
    bl_label = "Import Base Model"
    bl_options = {"REGISTER", "UNDO"}

    import_ext = ".fbx"
    filter_glob: StringProperty(
        default="*.fbx",
        options={"HIDDEN"},
    )  # type: ignore

    def import_fbx(self, context, filepath):
        # models: set[bpy.types.Object] = bpy.ops.import_scene.fbx(filepath=filepath)
        models: set[bpy.types.Object] = set_diff(
            context, lambda: bpy.ops.import_scene.fbx(filepath=filepath)
        )
        for model in models:
            context.scene.source_properties.source_animations.add().add(model)
        return {"FINISHED"}

    def execute(self, context):
        return self.import_fbx(context, self.filepath)


def set_diff(context, import_fn) -> set[bpy.types.Object]:
    initial_objects = set(context.scene.objects)
    import_fn()
    return set(context.scene.objects) - initial_objects
