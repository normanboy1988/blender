bl_info = {
    "name": "Randomize keyframes",
    "author": "Tal Hershkovich ",
    "version": (0, 1),
    "blender": (2, 72, 0),
    "location": "View3D > Tool Shelf > Animation > Randomize keyframes",
    "description": "Randomize selected keyframes, useful for giving cycle animations some variations",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Animation/Randomize_Keyframes",
    "category": "Animation"}

import bpy
import random

def randomize(self, context):
    
    threshold = bpy.context.scene.threshold
    
    action = bpy.context.object.animation_data.action
    for fcu in action.fcurves:
        value_list = []
        
        #create an average value from selected keyframes
        for key in fcu.keyframe_points: 
            if key.select_control_point == True: #and fcu.data_path.find('rotation') == -1:
                value_list.append(key.co[1])
                
        if len(value_list) > 0:
            avg_value = max(value_list)- min(value_list)
            #avg_value = sum(value_list) / len(value_list)
     
        for key in fcu.keyframe_points:
            if key.select_control_point == True:
                #store handle_type 
                handle_r_type = key.handle_right_type
                handle_l_type = key.handle_left_type               
                
                key.co[1] += avg_value * random.uniform(-threshold, threshold)
                key.handle_right_type = handle_r_type
                key.handle_left_type = handle_l_type
                
        fcu.update()

class RandomizeKeys(bpy.types.Operator):
    """Create Random Keys"""
    bl_label = "Randomize keyframes"
    bl_idname = "fcurves.random"
    bl_options = {'REGISTER', 'UNDO'}  
    
    bpy.types.Scene.threshold = bpy.props.FloatProperty(name="threshold", description="Threshold of keyframes", default=0.1, min=0.0, max = 1.0)
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.animation_data and context.active_object.animation_data.action is not None
      
    def execute(self, context):
        randomize(self, context)
        return {'FINISHED'} 
    
class RandomizeKeys_Panel(bpy.types.Panel):
    """Add random value to selected keyframes"""
    bl_label = "Randomize keyframes"
    bl_idname = "fcurves.panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animation"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Randomize selected keyframes")
        layout.operator("fcurves.random")
        layout.prop(context.scene, 'threshold', slider = True)        

def register():
    bpy.utils.register_class(RandomizeKeys)
    bpy.utils.register_class(RandomizeKeys_Panel)

def unregister():
    bpy.utils.unregister_class(RandomizeKeys)
    bpy.utils.unregister_class(RandomizeKeys_Panel)

if __name__ == "__main__":
    register()                               