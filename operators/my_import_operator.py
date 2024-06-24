from typing import Optional
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
        for model in models:
            if model.animation_data is not None:
                bpy.data.actions.remove(model.animation_data.action)
                context.scene.source_properties.source_object = model
        return {"FINISHED"}

    def execute(self, context):
        return self.import_fbx(context, self.filepath)


class ImportAnimationOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.import_animation"
    bl_label = "Import Animation"
    bl_options = {"REGISTER", "UNDO"}

    import_ext = ".fbx"
    filter_glob: StringProperty(
        default="*.fbx",
        options={"HIDDEN"},
    )  # type: ignore

    def import_fbx(self, context, filepath):
        # models: set[bpy.types.Object] = bpy.ops.import_scene.fbx(filepath=filepath)
        models: set[bpy.types.Object] = set_diff(
            context, lambda: bpy.ops.import_scene.fbx(filepath=filepath, use_anim=True)
        )
        animation_name = filepath.split("/")[-1].split(".")[0]
        for model in models:
            action = rename_action(model, animation_name)
            if action is None:
                continue
            """ context.scene.source_properties.source_animations.add().add(
                model, animation_name, action
            ) """
            # push down action on base model
            base_model = context.scene.source_properties.source_object
            if base_model is not None:
                push_down_action(base_model, action)
        for model in models:
            bpy.data.objects.remove(model)

        return {"FINISHED"}

    def execute(self, context):
        return self.import_fbx(context, self.filepath)


def set_diff(context, import_fn) -> set[bpy.types.Object]:
    initial_objects = set(context.scene.objects)
    import_fn()
    return set(context.scene.objects) - initial_objects


def rename_action(
    object: bpy.types.Object, new_name: str
) -> Optional[bpy.types.Action]:
    if object.animation_data is None:
        return None
    action = object.animation_data.action
    action.name = new_name
    return action


def push_down_action(object: bpy.types.Object, action: bpy.types.Action):
    object.animation_data.action = action

    # def work_fn():
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.area.type = "DOPESHEET_EDITOR"
    bpy.context.space_data.ui_mode = "ACTION"
    bpy.context.view_layer.objects.active = object
    bpy.ops.action.push_down()

    # do_work_in_context(work_fn)


def do_work_in_context(work_fn):
    save_area = bpy.context.area.type
    saved_space = bpy.context.space_data.ui_mode
    saved_object = bpy.context.view_layer.objects.active
    work_fn()
    bpy.context.area.type = save_area
    bpy.context.space_data.ui_mode = saved_space
    bpy.context.view_layer.objects.active = saved_object
