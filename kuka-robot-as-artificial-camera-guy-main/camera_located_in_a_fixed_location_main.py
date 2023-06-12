from robot_integration import RemoteControlKUKA
from kinect_openni import FixedPositionCamera
import time
import cv2
import math
import sys

# c2=a2+b2−2 a b cos(γ)
def calcAngle(a, b, c):
    if a != 0 and b != 0 and c != 0:
        length3 = (math.pow(a, 2) + math.pow(b,2) - math.pow(c, 2))/(2*a*b)
        angle = math.acos(length3)
        #print(("Angle in Radians:", angle)
        angleInDegrees = convertRadiansIntoDegrees(angle)
        #print(("Angle in Degrees:", angleInDegrees)
        return angleInDegrees
        
def convertRadiansIntoDegrees(x):
    pi=math.pi
    degree=(x*180)/pi
    return degree

if __name__ == '__main__':
    distanceRtoC = 160 # int(sys.argv[1]) // 230, 200
    distanceCtoP = 200 # int(sys.argv[2]) # This value is depth from camera
    distanceRtoP = 200 # int(sys.argv[3])
    cameraAngle = calcAngle(distanceCtoP, distanceRtoC, distanceRtoP)
    # in centimeters
    realword_dimensions = { 
        "height": 200,
        "width" : 400
    }

    # in px
    camera_dimensions = { 
        "height": 480,
        "width" : 640
    }

    camera_center = (camera_dimensions['height']/2, camera_dimensions['width']/2)
    # converting camera resolution (in px) to real world co-ordinates
    height_cm_to_px_ratio = realword_dimensions['height'] / camera_dimensions['height']
    width_cm_to_px_ratio = realword_dimensions['width'] / camera_dimensions['width']
    height_scaling_factor = int(height_cm_to_px_ratio * 10)
    width_scaling_factor = int(width_cm_to_px_ratio * 10)
    key = None
    rck = RemoteControlKUKA()
    home = '{E6AXIS: A1 0, A2 -90.0, A3 90.0, A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
    A1 = 0
    A2 = -90
    # A3 = 90
    rck.moveTo(home)    
    camera = FixedPositionCamera()    
    # calculate distance between camera and personX
    # calculate camera angle
    # start program
    # calculate angle between camera and person as angle 2
    # calculate difference of angle2 and angle1 and increase decrease angle of the robot respectively     
    while key != ord('q'):
        for info in camera.get_face_and_depth_info():
            #print(('info = ', info)
            key = cv2.waitKey(1) & 0xFF
            if len(info) == 3:
                new_height = (info[0] - camera_center[0]) * height_cm_to_px_ratio
                new_width = ((info[1]- camera_center[1]) * width_cm_to_px_ratio) / height_scaling_factor
                new_depth = (float(info[2]) - distanceCtoP) / width_scaling_factor
                # when camera is at angle 40 degree, depth is A1, width is A2, height is A3
                e6axis2 = '{E6AXIS: A1 '+ str("{:.2f}".format(A1+new_depth)) +', A2 '+ str("{:.2f}".format(A2+new_width)) +', A3 90, A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
                #print(('e6axis2: ',e6axis2)
                rck.moveTo(e6axis2)        
    camera.close_frames()

