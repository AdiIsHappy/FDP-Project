import rospy
from geometry_msgs.msg import Point
import VariableManager

class MasterRecorder:

    def __init__(self):
        self.recording = VariableManager.recording
        self.file = None
        self.data_to_write = VariableManager.master_data
        
    def main(self):
        
        if(not self.recording and VariableManager.recording):
            self.clear_recorded_data()
        self.recording = VariableManager.recording
        if(self.recording):
            self.record_data()
        
    def clear_recorded_data(self):
        print("clearing")
        self.file = open("recorded_data.txt", "w")
        self.file.write("")
        self.file.close()
    
    def record_data(self):
        try:
            self.file = open("recorded_data.txt", "a")
        except:
            self.file = open("recorded_data.txt", "w")
        self.data_to_write = VariableManager.master_data
        print("recording : " + f"{self.data_to_write.x},{self.data_to_write.y},{self.data_to_write.z}")
        self.file.write(f"{self.data_to_write.x},{self.data_to_write.y},{self.data_to_write.z}\n")
        self.file.close()
        
        