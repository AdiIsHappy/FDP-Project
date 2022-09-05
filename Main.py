import rospy
import MobileInputManager
import VariableManager
import MasterDataRecorder
import RecordingPlayer
import SensorManager
import LineFollower
from geometry_msgs.msg import Point

def play_active_mode():
    global mode
    if(mode != VariableManager.active_mode):
        recording_player.stop_playing()
    mode = VariableManager.active_mode
    if (mode == [1,0,0]):
        mob_manager.update_master_data()
    elif(mode == [0,1,0]):
        recording_player.main()
    else :
        line_follower.main()
mode = None
VariableManager.init_vars()
rospy.init_node("Master")
rate = rospy.Rate(20)

master_publisher = rospy.Publisher("master_data", Point, queue_size=1)
master_recorder = MasterDataRecorder.MasterRecorder()
line_follower = LineFollower.LineFollower()
mob_manager = MobileInputManager.MobileManager()
recording_player = RecordingPlayer.RecordingPlayer()
sensor_manager = SensorManager.SensorManager()

while (not rospy.is_shutdown()):
    sensor_manager.main()
    master_recorder.main()
    mob_manager.main()
    play_active_mode()
    # VariableManager.print_vars()
    rate.sleep()
    master_publisher.publish(VariableManager.master_data)

