import rospy
import serial
from threading import Thread
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from serial_receiver import serialReceiver
from std_msgs.msg import UInt16
from file_manager import fileManager


class DataInterface:
    def __init__(self, file_name):
        # Only argument stuff
        self.file_name = file_name
        self.running = False
        port = '/dev/ttyACM0'
        baud = 115200
        self.ser_receiver = serialReceiver(port, baud, debug = True)
        self.file_manager = fileManager(self.file_name)
        self.cmd = 500

    def initialize(self):
        # Get params and allocate msgs
        self.state_update_rate = rospy.get_param('/rate', 50)
        self.ser_receiver.initialize()
        self.file_manager.init()

    def start(self):
        # Create subs, services, publishers, threads
        self.running = True
        #publishers
        self.data1_pub = rospy.Publisher('/a1x', Float32, queue_size=70)
        self.data2_pub = rospy.Publisher('/a1y', Float32, queue_size=70)
        self.data3_pub = rospy.Publisher('/a1z', Float32, queue_size=70)
        self.data4_pub = rospy.Publisher('/a2x', Float32, queue_size=70)
        self.data5_pub = rospy.Publisher('/a2y', Float32, queue_size=70)
        self.data6_pub = rospy.Publisher('/a2z', Float32, queue_size=70)
        self.data7_pub = rospy.Publisher('/time', Float32, queue_size=70)
        Thread(target=self.update_state).start()
        #subscribers
        self.cmd_sub = rospy.Subscriber('/cmd', UInt16, self.cmd)

    def stop(self):
        self.running = False
        self.data1_pub.unregister()
        self.cmd_sub.unregister()

    def cmd(self, msg):
        self.cmd = msg.data
        self.ser_receiver.write(self.cmd)

    def update_state(self):
        rate = rospy.Rate(self.state_update_rate)
        while self.running and not rospy.is_shutdown():
            if(self.ser_receiver.read()):
                data = self.ser_receiver.struct 
                a1x = data[0]
                a1y = data[1]
                a1z = data[2]
                a2x = data[3]
                a2y = data[4]
                a2z = data[5]
                time = data[6]
                self.data1_pub.publish(a1x)
                self.data2_pub.publish(a1y)
                self.data3_pub.publish(a1z)
                self.data4_pub.publish(a2x)
                self.data5_pub.publish(a2y)
                self.data6_pub.publish(a2z)
                self.data7_pub.publish(time)

                self.file_manager.to_file(data, len(data))
            rate.sleep()
                           
           

if __name__ == '__main__':
    rospy.init_node('ros_bt_interface')
    file_name = raw_input("file_name: ")
    rwbt = DataInterface(file_name)
    rwbt.initialize()
    rwbt.start()
    rospy.spin()
    rwbt.stop()