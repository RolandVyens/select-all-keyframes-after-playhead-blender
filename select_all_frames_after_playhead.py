bl_info = {
    "name": "select all keyframes after playhead",
    "author": "GPT 3.5, Roland Vyens",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "Animation",
}

import bpy


def select_all_after_playhead():
    # Select all armatures and bones
    for obj in bpy.context.scene.objects:
        if obj.type == "ARMATURE":
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="POSE")
            bpy.ops.pose.select_all(action="SELECT")
            bpy.ops.object.mode_set(mode="OBJECT")

            # Select the armature in the viewport
            if obj.name in bpy.context.view_layer.objects:
                obj.select_set(True)

    # Select all objects in viewport
    for obj in bpy.context.scene.objects:
        if obj.name in bpy.context.view_layer.objects:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

    # Define current frame as the current frame in the timeline
    current_frame = bpy.context.scene.frame_current

    # Deselect all keyframes on objects
    for obj in bpy.context.scene.objects:
        if obj.name in bpy.context.view_layer.objects:
            animation_data = getattr(obj, "animation_data", None)
            if animation_data and animation_data.action:
                for fcurve in animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.select_control_point = False

    # Select all keyframes after the current frame on objects
    for obj in bpy.context.scene.objects:
        if obj.name in bpy.context.view_layer.objects:
            animation_data = getattr(obj, "animation_data", None)
            if animation_data and animation_data.action:
                for fcurve in animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        if keyframe.co[0] > current_frame:
                            keyframe.select_control_point = True

    # Deselect all keyframes on bones
    for armature in bpy.context.scene.objects:
        if armature.type == "ARMATURE":
            animation_data = getattr(armature, "animation_data", None)
            if animation_data and animation_data.action:
                for bone in armature.data.bones:
                    animation_data_bone = getattr(bone, "animation_data", None)
                    if animation_data_bone and animation_data_bone.action:
                        for fcurve in animation_data_bone.action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                keyframe.select_control_point = False

    # Select all keyframes after the current frame on bones
    for armature in bpy.context.scene.objects:
        if armature.type == "ARMATURE":
            animation_data = getattr(armature, "animation_data", None)
            if animation_data and animation_data.action:
                for bone in armature.data.bones:
                    animation_data_bone = getattr(bone, "animation_data", None)
                    if animation_data_bone and animation_data_bone.action:
                        for fcurve in animation_data_bone.action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                if keyframe.co[0] > current_frame:
                                    keyframe.select_control_point = True


class select_all_key_frames_OT_(bpy.types.Operator):
    bl_idname = "anim.select_all_keyframes_after_playhead"
    bl_label = "select all"
    bl_description = "select_all_keyframes_after_playhead"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        select_all_after_playhead()
        return {"FINISHED"}


class TimelinePanel(bpy.types.Header):
    bl_label = "Timeline Panel"
    bl_idname = "PT_TimelinePanel"
    bl_space_type = "DOPESHEET_EDITOR"

    def draw(self, context):
        layout = self.layout

        # Add your operator button to the timeline header
        layout.operator(
            select_all_key_frames_OT_.bl_idname, icon="TRACKING_FORWARDS_SINGLE"
        )


def register():
    bpy.utils.register_class(select_all_key_frames_OT_)
    bpy.utils.register_class(TimelinePanel)
    bpy.types.DOPESHEET_HT_header.append(TimelinePanel.draw)


def unregister():
    bpy.utils.unregister_class(select_all_key_frames_OT_)
    bpy.utils.unregister_class(TimelinePanel)
    bpy.types.DOPESHEET_HT_header.remove(TimelinePanel.draw)


if __name__ == "__main__":
    register()
