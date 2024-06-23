if "bpy" in locals():
    import importlib

    if "dir_operator" in locals():
        importlib.reload(dir_operator)
    if "dir_panel" in locals():
        importlib.reload(dir_panel)
    if "my_import_operator" in locals():
        importlib.reload(my_import_operator)
    if "my_source_properties" in locals():
        importlib.reload(my_source_properties)

else:
    from .operators import dir_operator
    from .operators import my_import_operator
    from .panels import dir_panel
    from .properties import my_source_properties


import bpy


bl_info = {
    "name": "8 Directions Render",
    "author": "f0kes",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Scene > 8 Directions Panel",
    "description": "Render 8 directions of selected objects",
    "warning": "",
    "doc_url": "",
    "category": "Render",
}


def register():
    bpy.utils.register_class(dir_operator.MultiDirOperator)
    bpy.utils.register_class(dir_panel.MultiDirPanel)
    bpy.utils.register_class(my_import_operator.ImportBaseOperator)
    bpy.utils.register_class(my_source_properties.ObjectPointerProperty)
    bpy.utils.register_class(my_source_properties.SourceProperties)
    bpy.types.Scene.source_properties = bpy.props.PointerProperty(
        type=my_source_properties.SourceProperties
    )


def unregister():
    bpy.utils.unregister_class(dir_operator.MultiDirOperator)
    bpy.utils.unregister_class(dir_panel.MultiDirPanel)
    bpy.utils.unregister_class(my_import_operator.ImportBaseOperator)
    bpy.utils.unregister_class(my_source_properties.ObjectPointerProperty)
    bpy.utils.unregister_class(my_source_properties.SourceProperties)


if __name__ == "__main__":
    register()
    print("8 Directions Render addon loaded")
