import VariableManager
import rospy
from SensorData.msg import sensorData

class SensorManager:
    def __init__(self):
        self.recived_data ={"iRLeft":0,
                            "iRRight":0,
                            "uSBack":1000,
                            "uSFront":1000,
                            }
        self.subscriber = rospy.Subscriber("sensor_data", sensorData, self.recive_sensor_data)
        print("subscirbed")
    
    def recive_sensor_data(self,data):
        self.recived_data["iRLeft"] = data.leftIR
        self.recived_data["iRRight"] = data.rightIR
        self.recived_data["uSFront"] = data.frontUS
        self.recived_data["uSBack"] = data.backUS
    
    def main(self):
        VariableManager.sensor_data = self.recived_data
    

