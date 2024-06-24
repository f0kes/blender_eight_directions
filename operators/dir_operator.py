from typing import List
import bpy
import os
import math

node_initial_paths = {}


def record_initial_node_paths(tree: bpy.types.NodeTree):
    for node in tree.nodes:
        if isinstance(node, bpy.types.CompositorNodeOutputFile):
            node_initial_paths[node] = node.base_path


def generate_path_for_CompositorNodeOutputFile(
    node: bpy.types.CompositorNodeOutputFile, path_append
):
    if node in node_initial_paths:
        return node_initial_paths[node] + path_append
    return None


def construct_path_append(current_path: List[str]):
    # concatenate strings, separated by '\\'
    return "\\" + "\\".join(current_path)


def mutate_output_file_nodes(tree: bpy.types.NodeTree, current_path: List[str]):
    for node in tree.nodes:
        if isinstance(node, bpy.types.CompositorNodeOutputFile):
            path_append = construct_path_append(current_path)
            path = generate_path_for_CompositorNodeOutputFile(node, path_append)
            if path:
                node.base_path = path


def restore_initial_paths(tree: bpy.types.NodeTree):
    for node in tree.nodes:
        if isinstance(node, bpy.types.CompositorNodeOutputFile):
            if node in node_initial_paths:
                node.base_path = node_initial_paths[node]


def render8directions_selected_objects(context: bpy.types.Context):
    base_model = context.scene.source_properties.source_object
    if base_model is None:
        return
    selected_list = [base_model]
    bpy.context.active_object = base_model
    tree = bpy.context.scene.node_tree
    bpy.ops.object.select_all(action="TOGGLE")
    scene = bpy.context.scene
    scene.render.resolution_x = 768
    scene.render.resolution_y = 768
    record_initial_node_paths(tree)

    for object in selected_list:

        bpy.context.scene.objects[object.name].select_set(True)

        scn = bpy.context.scene
        for animation in object.animation_data.nla_tracks:
            animation = animation.strips[0]
            bpy.context.active_object.animation_data.action = bpy.data.actions.get(
                animation.name
            )

            scn.frame_end = int(
                bpy.context.active_object.animation_data.action.frame_range[1]
            )

            current_path = [animation.name]

            for angle in range(0, 360, 45):
                render_with_angle(scene, current_path, angle)
    restore_initial_paths(tree)


def render_with_angle(scene: bpy.types.Scene, current_path, angle):
    angleDir = str(angle)
    new_path = current_path + [angleDir]
    mutate_output_file_nodes(scene.node_tree, new_path)

    bpy.context.active_object.rotation_euler[2] = math.radians(angle)
    for i in range(scene.frame_start, scene.frame_end, 1):
        scene.frame_current = i

        bpy.ops.render.render(  # {'dict': "override"},
            False, animation=False, write_still=True  # undo support
        )


# render8directions_selected_objects(r'C:\Users\VALERY\Downloads\wolfanimation')
# render8directions_selected_objects()


class MultiDirOperator(bpy.types.Operator):
    bl_idname = "object.render_8_directions"
    bl_label = "Render 8 directions"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        render8directions_selected_objects(context)
        return {"FINISHED"}
