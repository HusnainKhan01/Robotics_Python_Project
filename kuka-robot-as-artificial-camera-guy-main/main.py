from robot_integration import RemoteControlKUKA
from kinect_openni import FixedPositionCamera
from konftel_cam20 import face_detection, face_detection_without_Queue
import time
import cv2
import math
import sys

# c2=a2+b2−2 a b cos(γ)
def calcAngle(a, b, c):
    if a != 0 and b != 0 and c != 0:
        length3 = (math.pow(a, 2) + math.pow(b,2) - math.pow(c, 2))/(2*a*b)
        angle = math.acos(length3)
        #print("Angle in Radians:", angle)
        angleInDegrees = convertRadiansIntoDegrees(angle)
        #print("Angle in Degrees:", angleInDegrees)
        return angleInDegrees
        
def convertRadiansIntoDegrees(x):
    pi=math.pi
    degree=(x*180)/pi
    return degree

if __name__ == '__main__':
    key = None
    rck = RemoteControlKUKA()
    home = '{E6AXIS: A1 0, A2 -90.0, A3 90.0, A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
    A1 = 0.0
    A2 = -90.0
    A3 = 90.0
    rck.moveTo(home,True)
    if sys.argv[1] == '1':
        camera = FixedPositionCamera() 
        distanceRtoC = 260 # int(sys.argv[1]) // 230, 200
        distanceCtoP = 180 # int(sys.argv[2]) # This value is depth from camera
        distanceRtoP = 200 # int(sys.argv[3])
        cameraAngle = calcAngle(distanceCtoP, distanceRtoC, distanceRtoP)
        # in centimeters
        realworld_dimensions = { 
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
        height_cm_to_px_ratio = realworld_dimensions['height'] / camera_dimensions['height']
        width_cm_to_px_ratio = realworld_dimensions['width'] / camera_dimensions['width']
        
        
        height_scaling_factor = int(height_cm_to_px_ratio * 10)
        width_scaling_factor = int(width_cm_to_px_ratio * 5)
        
        
        while key != ord('q'):
            for info in camera.get_face_and_depth_info():
                #print('info = ', info)
                key = cv2.waitKey(1) & 0xFF
                if len(info) == 3 and rck.is_idle():
                    if(info[2]<500 and info[2]>30):
                        new_depth = (info[2] - distanceCtoP) / width_scaling_factor
                    # else: 
                    #    new_depth = distanceCtoP
                    new_width = ((info[1]- camera_center[1]) * width_cm_to_px_ratio) / height_scaling_factor
                    new_height = (info[0] - camera_center[0]) * height_cm_to_px_ratio
                    
                    A3 = (A2 + new_width)*(-1)
                    #print('new height: ',new_height)
                    # when camera is at angle 40 degree, depth is A1, width is A2, height is A3                    
                    e6axis3 = '{E6AXIS: A1 '+ "{0:.1f}".format(A1 + new_depth) +', A2 '+ "{0:.1f}".format(A2 + new_width) +', A3 '+"{0:.1f}".format(A3)+', A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
                    print(e6axis3)
                    rck.moveTo(e6axis3)
        camera.close_frames()
    if sys.argv[1] == '2':    
        x=0
        z=100
        while True:
            for position in face_detection():
                #print("main")
                #print(position)
                #print('x '+str(x)+' z '+str(z))
                #print('idle '+str(rck.is_idle()))
                if(rck.is_idle()):
                    #print('entered loop')
                    # x = x+(position[0]-320)/12
                    x = x+((position[0] - 320)/12)
                    z = z+((position[1]-240)/8.75)
                    # z = max(min(100-((position[1]-225)/8.75), 120), 70)
                    e6axis2 = '{E6AXIS: A1 '+str(x)+', A2 -90.0, A3 '+str("{:.2f}".format(z))+', A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
                    #print(e6axis2)
                    rck.moveTo(e6axis2)

    if sys.argv[1] == '3':    
        x=0
        z=100
        while True:
            for position in face_detection_without_Queue():
                #print("main")
                #print(position)
                #print('x '+str(x)+' z '+str(z))
                #print('idle '+str(rck.is_idle()))
                if(rck.is_idle()):
                    #print('entered loop')
                    # x = x+(position[0]-320)/12
                    x = x+((position[0] - 320)/12)
                    z = z+((position[1]-240)/8.75)
                    # z = max(min(100-((position[1]-225)/8.75), 120), 70)
                    e6axis2 = '{E6AXIS: A1 '+str(x)+', A2 -90.0, A3 '+str("{:.2f}".format(z))+', A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
                    #print(e6axis2)
                    rck.moveTo(e6axis2)
    if sys.argv[1] == '4':
        camera = FixedPositionCamera() 
        min_distance = 210
        realworld_dimensions = { 
            "height": 200,
            "width" : 600,
            "depth_max" : 320,
            "depth_min" : 100
        }

        # in px
        camera_dimensions = { 
            "height": 345,
            "width" : 640
        }

        camera_center = (((camera_dimensions['height']/2)), camera_dimensions['width']/2)
        # converting camera resolution (in px) to real world co-ordinates
        height_cm_to_px_ratio = realworld_dimensions['height'] / camera_dimensions['height']
        width_cm_to_px_ratio = realworld_dimensions['width'] / camera_dimensions['width']
        
        depth_scaling_factor = (realworld_dimensions['depth_max'] - realworld_dimensions['depth_min'])/100
        height_scaling_factor = int(height_cm_to_px_ratio * 15)
        width_scaling_factor = int(width_cm_to_px_ratio * 10)
        
        while key != ord('q'):
            for info in camera.get_face_and_depth_info():
                print('info = ', info)
                key = cv2.waitKey(1) & 0xFF
                if len(info) == 3 and rck.is_idle():
                    new_width = ((info[1] - camera_center[1]) / width_scaling_factor)*(-1)
                    new_depth = (info[2]- min_distance)/depth_scaling_factor
                    new_height = (info[0]- camera_center[0])/ height_scaling_factor
                    
                    A3 = (A2 + new_depth)*(-1)
                    #print('new height: ',new_height)
                    # when camera is at angle 40 degree, depth is A1, width is A2, height is A3                    
                    e6axis3 = '{E6AXIS: A1 '+ "{0:.1f}".format(A1 + new_width) +', A2 '+ "{0:.1f}".format(A2 + new_depth) +', A3 '+"{0:.1f}".format(A3+new_height)+', A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
                    print(e6axis3)
                    rck.moveTo(e6axis3)
        camera.close_frames()


