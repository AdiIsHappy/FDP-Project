import rospy
from geometry_msgs.msg import Point

def init_vars():
    global sensor_data, master_data, motion_data, active_mode, recording
    sensor_data = {"iRLeft":0,
                "iRRight":0,
                "uSBack":1000,
                "usFront":1000,
                }
    master_data = Point(0,0,1)
    motion_data = {
                    "JoyStick" : [0,0],
                    "Speed" : 0,   
                    }
    active_mode = [1,0,0]
    recording = False

def print_vars():
    print(sensor_data)
    print(master_data)
    print(motion_data)
    print(active_mode)
    print(recording)