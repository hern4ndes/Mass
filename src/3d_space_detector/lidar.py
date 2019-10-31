#!/usr/bin/env python
import rospy
from std_msgs.msg import *
from sensor_msgs.msg import *

class m_lidar():
    def __init__(self):
        rospy.init_node('simple_sub', anonymous=True)
        self.ang_var = [0, 0]
        self.m_ranges = []

    def callback(self, data):
        self.ang_var[0] = data.angle_min
        self.ang_var[1] = data.angle_max
        self.m_ranges = data.ranges

        # print(data.ranges)
        
    def listener(self):        
        rospy.Subscriber("scan", LaserScan, self.callback)
        # if rospy.is_shutdown():
        #     print('shutdown')
        #     break

        # spin() simply keeps python from exiting until this node is stopped
        # rospy.spin()  # dispensável 