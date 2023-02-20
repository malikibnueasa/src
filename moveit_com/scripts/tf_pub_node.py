#!/usr/bin/env python3

import rospy
import time
import tf2_ros
# from gazebo_plugins.msg import GazeboModel
# from turtle_tf_3d.get_model_gazebo_pose import GazeboModel
import roslib
roslib.load_manifest('my_pkg')
from gazebo_msgs.msg import ModelState

def handle_turtle_pose(pose_msg, robot_name):
    br = tf2_ros.TransformBroadcaster()

    br.sendTransform((pose_msg.position.x,pose_msg.position.y,pose_msg.position.z),
                    (pose_msg.orientation.x,pose_msg.orientation.y,pose_msg.orientation.z,pose_msg.orientation.w),
                    rospy.Time.now(),
                    robot_name,
                    "/world")



def publisher_of_tf():
    rospy.init_node('tf_publisher', anonymous=True)
    robot_name_list = ['robo_com','rod']
    gazebo_model_object =  GazeboModel(robot_name_list)

    for robot_name in robot_name_list:
        pose_now = gazebo_model_object.get_model_pose(robot_name)

    time.sleep(1)
    rospy.loginfo("Ready...Starting to Publish TF data now..!")

    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        for robot_name in robot_name_list:
            pose_now = gazebo_model_object.get_model_pose(robot_name)
            if not pose_now:
                print("The pose is not yet "+ str(robot_name)+" available.. Plase try again later")
            else:
                handle_turtle_pose(pose_now, robot_name)
        rate.sleep()



if __name__ == '__main__':
    try:
        publisher_of_tf()
    except rospy.ROSInterruptException:
        pass