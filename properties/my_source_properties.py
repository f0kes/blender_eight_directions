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


class AnimationSourceProperties(bpy.types.PropertyGroup):
    source_object: bpy.props.PointerProperty(type=bpy.types.Object)  # type: ignore
    animation_name: bpy.props.StringProperty()  # type: ignore
    action: bpy.props.PointerProperty(type=bpy.types.Action)  # type: ignore

    def copy(self):
        self.source_object = self.id_data.copy()
        self.name = self.source_object.name
        self.animation_name = self.source_object.animation_name
        self.action = self.source_object.action
        return self.source_object

    def add(self, ob, anim_name, action):
        self.source_object = ob
        self.name = ob.name
        self.animation_name = anim_name
        self.action = action
        return self.source_object


class SourceProperties(bpy.types.PropertyGroup):
    """Properties for the source object"""

    source_object: bpy.props.PointerProperty(
        name="Base Model", type=bpy.types.Object
    )  # type: ignore
    source_animations: bpy.props.CollectionProperty(
        name="Source Animations", type=AnimationSourceProperties
    )  # type: ignore
