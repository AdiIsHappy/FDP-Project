import rospy
import MobileInputManager
import VariableManager
import MasterDataRecorder

VariableManager.init_vars()
rospy.init_node("Master")
rate = rospy.Rate(10)
master_recorder = MasterDataRecorder.MasterRecorder()
mob_manager = MobileInputManager.MobileManager()
while (not rospy.is_shutdown()):
    master_recorder.main()
    mob_manager.main()
    rate.sleep()
