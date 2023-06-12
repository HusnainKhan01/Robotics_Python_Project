from konftel_cam20 import face_detection
from robot_integration import RemoteControlKUKA
import time

   
if __name__ == '__main__':
    rck = RemoteControlKUKA()
    x=0
    z=90
    home = '{E6AXIS: A1 0, A2 -90.0, A3 90.0, A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
    rck.moveTo(home,True)
    flag = True
    while True:
        for position in face_detection():
            print("main")
            print(position)
            print('x '+str(x)+' z '+str(z))
            print('idle '+str(rck.is_idle()))
            if(rck.is_idle()):
                print('entered loop')
                # x = x+(position[0]-320)/12
                x = x+((position[0] - 320)/12)
                z = z+((position[1]-240)/8.75)
                # z = max(min(100-((position[1]-225)/8.75), 120), 70)
                e6axis2 = '{E6AXIS: A1 '+str(x)+', A2 -90.0, A3 '+str("{:.2f}".format(z))+', A4 0.0, A5 -90.0, A6 270.0, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}'
                print(e6axis2)
                rck.moveTo(e6axis2)
