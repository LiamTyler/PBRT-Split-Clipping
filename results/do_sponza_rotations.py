import re
import matplotlib.pyplot as plt
import numpy as np
from pyquaternion import *
from math import *
import os
import subprocess

def ToEulerAngles( q ):
    roll = 0
    pitch = 0
    yaw = 0

    # roll (x-axis rotation)
    sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
    roll = atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = 2 * (q.w * q.y - q.z * q.x)
    if (abs(sinp) >= 1):
        pitch = copysign(M_PI / 2, sinp) # use 90 deg if out of range
    else:
        pitch = asin(sinp)

    # yaw (z-axis rotation)
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    yaw = atan2(siny_cosp, cosy_cosp)

    return [ 180/pi * roll, 180/pi * pitch, 180/pi * yaw ]

q0 = Quaternion(axis=[1, 0, 0], angle=radians(0.0))
q1 = Quaternion(axis=[0, 0, 1], angle=radians(30.0)) * Quaternion(axis=[0, 1, 0], angle=radians(-20.0)) * Quaternion(axis=[1, 0, 0], angle=radians(90.0))
q2 = Quaternion(axis=[0, 0, 1], angle=radians(90.0)) * Quaternion(axis=[1, 0, 0], angle=radians(-180.0))

scene1 = """
Accelerator "bvh"
LookAt 0 0 0 -1 0 0 0 0 1
Camera "perspective" "float fov" [60 ]
Film "image"  "integer xresolution" [800 ] "integer yresolution" [800 ]
    "string filename" "sponza.exr"

Sampler "lowdiscrepancy" "integer pixelsamples" [32]

WorldBegin
"""

scene3 = """

Translate -0.00724029541 0.00148797035 -7.37331104
AttributeBegin
AreaLightSource "area" "color L" [12 12 14 ] "integer nsamples" [15]
ReverseOrientation
Material "matte" "color Kd" [0 0 0 ]
Shape "disk" "float radius" [75] "float height" [64]
AttributeEnd

Include "geometry/sponzageom.pbrt"

WorldEnd
"""

os.chdir('C:\\Users\\Liam Tyler\\Documents\\School\\5608\\HW2\\PBRT-Split-Clipping\\test_scenes')


for i in range(30, 33):
    q  = Quaternion.slerp( q0, q1, i / 32 )
    angles = ToEulerAngles( q )
    #a = q.transformation_matrix * np.array([7, 0, 0, 1])
    #camPos = a[:,0]

    scene = ""
    scene += scene1
    #scene += "LookAt " + str(camPos[0]) + " " + str(camPos[1]) + " " + str(camPos[2]) + " 0 " + str(camPos[1]) + " " + str(camPos[2]) + " 0 0 1\n"
    #scene += scene2
    scene += "Rotate " + str(angles[2]) + " 0 0 1\n"
    scene += "Rotate " + str(angles[1]) + " 0 1 0\n"
    scene += "Rotate " + str(angles[0]) + " 1 0 0\n"
    scene += scene3
    #print(scene)
    f = open( 'scene.pbrt', 'w')
    f.write( scene )
    f.close()
    cmd = "..\\build\\Release\\pbrt.exe scene.pbrt --outfile SPONZA\\sponza" + str(i) + ".png"
    os.system(cmd)


for i in range( 33, 65 ):
    q  = Quaternion.slerp( q1, q2, (i-32) / 32)
    angles = ToEulerAngles( q )
    #a = q.transformation_matrix * np.array([7, 0, 0, 1])
    #camPos = a[:,0]

    scene = ""
    scene += scene1
    #scene += "LookAt " + str(camPos[0]) + " " + str(camPos[1]) + " " + str(camPos[2]) + " 0 " + str(camPos[1]) + " " + str(camPos[2]) + " 0 0 1\n"
    #scene += scene2
    scene += "Rotate " + str(angles[2]) + " 0 0 1\n"
    scene += "Rotate " + str(angles[1]) + " 0 1 0\n"
    scene += "Rotate " + str(angles[0]) + " 1 0 0\n"
    scene += scene3
    print(scene)
    f = open( 'scene.pbrt', 'w')
    f.write( scene )
    f.close()
    cmd = "..\\build\\Release\\pbrt.exe scene.pbrt --outfile SPONZA\\sponza" + str(i) + ".png"
    os.system(cmd)
