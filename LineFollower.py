import rospy
import VariableManager
from geometry_msgs.msg import Point

class LineFollower:
    def __init__(self):
        self.high = 1
        self.motion_data = Point(0,0,0.8)
        VariableManager.master_data = self.motion_data

        self.right_turn = Point(0,1,0.8)
        self.left_turn = Point(0,-1,0.8)
        self.move_straight = Point(1,0,0.8)
        self.stop = Point(0,0,0.8)

    def main(self):
        lir = VariableManager.sensor_data["iRLeft"]
        rir = VariableManager.sensor_data["iRRight"]
        # print(lir)
        if( lir == self.high and rir == self.high):
            self.motion_data = self.stop
        elif(lir != self.high and rir == self.high):
            self.motion_data = self.left_turn
        elif(lir == self.high and rir != self.high):
            self.motion_data = self.right_turn
        else:
            self.motion_data = self.move_straight
        VariableManager.master_data = self.motion_data
