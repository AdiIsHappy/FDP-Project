import rospy
import VariableManager
from geometry_msgs.msg import Point

class RecordingPlayer :
    def __init__(self):
        self.recording = None
        self.active_pointer = 0
        self.playing_forward = -1
        

    def load_recording(self):
        with open("recorded_data.txt", "r") as f:
            d = f.readlines()
            data = [
                Point(
                    float(i.split(",")[0]),
                    float(i.split(",")[1]),
                    float(i.split(",")[2]))
                for i in d]
        self.recording = data
        self.active_pointer = len(self.recording) - 1
        self.playing_forward = -1
    
    
    def stop_playing(self):
        self.recording = None
        self.active_pointer = 0
        self.playing_forward = -1     

    def update_counter(self):
        if(self.active_pointer < len(self.recording)-1 and self.playing_forward == 1):
            self.active_pointer += 1
        elif(self.active_pointer > 1 and not self.playing_forward == 1):
            self.active_pointer -= 1

        if(self.active_pointer == 1):
            self.playing_forward = 1
        elif(self.active_pointer == len(self.recording) - 2):
            self.playing_forward = -1

    def main(self):
        if(self.recording == None):
            self.load_recording()
        if(len(self.recording) == 0 ):
            return
        if(self.recording[self.active_pointer].y != 0):
            VariableManager.master_data = Point(self.recording[self.active_pointer].x ,
                                                self.recording[self.active_pointer].y * self.playing_forward,
                                                self.recording[self.active_pointer].z 
                                                )
        else :
                        VariableManager.master_data = Point(self.recording[self.active_pointer].x * self.playing_forward,
                                                self.recording[self.active_pointer].y * self.playing_forward,
                                                self.recording[self.active_pointer].z 
                                                )
        print(VariableManager.master_data)
        self.update_counter()

