import rospy
import MobileInputManager
import VariableManager
import MasterDataRecorder
import RecordingPlayer

def play_active_mode():
    global mode
    if(mode != VariableManager.active_mode):
        recording_player.stop_playing()

    mode = VariableManager.active_mode
    if (mode == [1,0,0]):
        mob_manager.main()
    elif(mode == [0,1,0]):
        recording_player.main()

mode = None
VariableManager.init_vars()
rospy.init_node("Master")
rate = rospy.Rate(10)

master_recorder = MasterDataRecorder.MasterRecorder()
mob_manager = MobileInputManager.MobileManager()
recording_player = RecordingPlayer.RecordingPlayer()

while (not rospy.is_shutdown()):
    master_recorder.main()
    play_active_mode()
    rate.sleep()
