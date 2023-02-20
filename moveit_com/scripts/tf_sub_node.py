#!/usr/bin/env python3

from curses.ascii import ctrl
import sys
import turtle
import rospy
import math
import tf2_ros
import geometry_msgs.msg


if __name__ == '__main__':
    rospy.init_node('tf_sub')
    listener = tf2_ros.TransformListener()
    
    if len(sys.argv) < 3:
        print("usage: tf_pub_node.py follower_model_name model_to_be_followed_name")
    else:
        follower_model_name = 'rod'
        model_to_be_followed_name = "robo_com"

        turtle_vel = rospy.Publisher(follower_model_name+'/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)

        rate = rospy.Rate(10.0)
        ctrl_c = False

        follower_model_frame = '/'+follower_model_name
        model_to_be_followed_frame = '/'+model_to_be_followed_name

        def shutdownhook():
            global ctrl_c
            print("Shutdown time! Stop the robot")
            cmd = geometry_msgs.Twist()
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            turtle_vel.publish(cmd)
            ctrl_c = True

        rospy.on_shutdown(shutdownhook)

        while not ctrl_c:
            try:
                (trans,rot) = listener.LookupTransform(follower_model_frame, model_to_be_followed_frame, rospy.Time(0))
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.Extrapolation):
                continue
            
            angular = 4 * math.atan2(trans[1], trans[0])
            linear = 0.5 * math.sqrt(trans[0]**2 + trans[1]**2)
            cmd = geometry_msgs.msg.Twist()
            cmd.linear.x = linear
            cmd.angular.z = angular
            turtle_vel.publish(cmd)

            rate.sleep()



