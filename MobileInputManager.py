import VariableManager
import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist

class MobileManager:

    ACCLERATION = 0.05

    def __init__(self):
        self.init_vars()
        self.create_subscribers()
        
    def init_vars(self):
        self.stop_distance = 20
        self.joystick = [0,0]
        self.speed_add_factor = 0
        self.recording = False
        self.record_play_mode = False
        self.line_follow_mode = False
        self.mob_controll_mode = True
        self.mode = [1,0,0]
        
    def create_subscribers(self):
        rospy.Subscriber("/Joystick", Twist, self.callback_joystick)
        rospy.Subscriber("/CtrlSpeedU", Bool, self.callback_speed_up)
        rospy.Subscriber("/CtrlSpeedD", Bool, self.callback_speed_down)
        rospy.Subscriber("/PlayRec", Bool, self.callback_play_recording)
        rospy.Subscriber("/RecMotion", Bool, self.callback_record_motion)
        rospy.Subscriber("/UseIR", Bool, self.callback_activte_ir)

    def callback_joystick(self, data):
        self.joystick =  [
            -1 if data.linear.x < -0.4 else (0 if data.linear.x < 0.4 else 1), 
            -1 if data.linear.y < -0.4 else (0 if data.linear.y < 0.4 else 1),
            ]
        

    def callback_speed_up(self, data):
        if(data.data == True):
            self.speed_add_factor += MobileManager.ACCLERATION
            self.speed_add_factor = round(self.speed_add_factor,2)

    def callback_speed_down(self, data):
        if(data.data == True):
            self.speed_add_factor -= MobileManager.ACCLERATION
            self.speed_add_factor = round(self.speed_add_factor,2)
    
    def callback_record_motion(self,data):
        if (data.data == True):
            self.recording = not self.recording
    def callback_play_recording(self,data):
        if (data.data == True ):

            if(not self.record_play_mode):
                self.mob_controll_mode = False
                self.record_play_mode = True
                self.line_follow_mode = False
                self.recording = False
                self.mode = [0,1,0] 
            else:
                self.mob_controll_mode = True
                self.record_play_mode = False
                self.line_follow_mode = False
                self.mode = [1,0,0]
            
    def callback_activte_ir(self,data):
        if (data.data == True ):
            if(not self.line_follow_mode ):
                self.mob_controll_mode = False
                self.record_play_mode = False
                self.line_follow_mode = True
                self.mode = [0,0,1] 

            else:
                self.mob_controll_mode = True
                self.record_play_mode = False
                self.line_follow_mode = False
                self.mode = [1,0,0]

    def main(self):
        VariableManager.recording = self.recording
        VariableManager.active_mode = self.mode

    def update_master_data(self):
        
        if(VariableManager.sensor_data["uSFront"] < 20 and self.joystick[1] == -1):
            self.joystick[1] = 0
        if(VariableManager.sensor_data["uSBack"] < 20 and self.joystick[1] == 1):
            self.joystick[1] = 0
        # VariableManager.motion_data["JoyStick"] = self.joystick
        VariableManager.master_data.x = self.joystick[0]
        VariableManager.master_data.y = self.joystick[1]
        # t = VariableManager.motion_data["Speed"]
        t = VariableManager.master_data.z
        t += self.speed_add_factor
        self.speed_add_factor = 0
        if(t >= 1): 
            t = 1
        elif (t<= 0.6):
            t = 0.6
        t = round(t,2)
        # VariableManager.motion_data["Speed"] = t
        VariableManager.master_data.z = t



