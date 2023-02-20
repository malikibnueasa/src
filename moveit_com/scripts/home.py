#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

class HomeNode:
    def __init__(self):
        rospy.init_node('home_node')

        self.home_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.result_callback)

    def start(self):
        rospy.loginfo("Starting home node...")

        while not rospy.is_shutdown():
            self.send_goal()
            rospy.sleep(1)

    def send_goal(self):
        home_goal = PoseStamped()
        home_goal.header.frame_id = "map"
        home_goal.pose.position.x = 0.0
        home_goal.pose.position.y = 0.0
        home_goal.pose.orientation.w = 1.0

        self.home_pub.publish(home_goal)
        rospy.loginfo("Sending robot to home position...")

    def result_callback(self, data):
        if data.status.status == 3:
            rospy.loginfo("Robot reached home position.")

if __name__ == '__main__':
    try:
        home = HomeNode()
        home.start()
    except rospy.ROSInterruptException:
        pass
