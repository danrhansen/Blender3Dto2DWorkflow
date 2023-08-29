import bpy
import os
import math

# get the scene
scn = bpy.context.scene

# get the output path
output_path = scn.render.filepath

# https://blender.stackexchange.com/questions/28159/how-to-rotate-a-bone-using-python

ob = bpy.data.objects['rig_boy']

#bpy.context.scene.objects.active = ob
ob.select_set( state = True, view_layer = bpy.context.view_layer )
bpy.context.view_layer.objects.active = ob

bpy.ops.object.mode_set(mode='POSE')

pbone = ob.pose.bones['boy_control']

# Set rotation mode to Euler XYZ, easier to understand than default quaternions
pbone.rotation_mode = 'XYZ'
# select axis in ['X','Y','Z']  <--bone local
axis = 'Z'
angle = 45

for i in range(8):
    if(i == 0):
        dir = 'D'
    elif(i == 1):
        dir = 'DR'
    elif(i == 2):
        dir = 'R'
    elif(i == 3):
        dir = 'UR'
    elif(i == 4):
        dir = 'U'
    elif(i == 5):
        dir = 'UL'    
    elif(i == 6):
        dir = 'L'
    elif(i == 7):
        dir = 'DL'

    # iterate through markers and render
    for k, m in scn.timeline_markers.items():  
        frame = m.frame
        marker_name = m.name
        scn.frame_set(frame)
        scn.render.filepath = os.path.join(output_path, marker_name.replace('X',dir) + ".png")
        bpy.ops.render.render( write_still=True )
        pbone.rotation_euler.rotate_axis(axis, math.radians(angle))
        pbone.keyframe_insert(data_path="rotation_euler", frame=frame)
       
bpy.context.scene.render.filepath = output_path