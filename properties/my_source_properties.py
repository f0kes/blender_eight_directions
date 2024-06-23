import bpy


class ObjectPointerProperty(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(type=bpy.types.Object)  # type: ignore

    def copy(self):
        self.object = self.id_data.copy()
        self.name = self.object.name
        return self.object

    def add(self, ob):
        self.object = ob
        self.name = ob.name
        return self.object


class SourceProperties(bpy.types.PropertyGroup):
    """Properties for the source object"""

    source_object: bpy.props.PointerProperty(
        name="Base Model", type=bpy.types.Object
    )  # type: ignore
    source_animations: bpy.props.CollectionProperty(
        name="Source Animations", type=ObjectPointerProperty
    )  # type: ignore
