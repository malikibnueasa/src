#!/usr/bin/env python3
import rospy
import actionlib  #http://wiki.ros.org/actionlib
import sys
import copy
import moveit_commander
import moveit_msgs.msg
from geometry_msgs.msg import Pose,Quaternion
import rospkg
import geometry_msgs.msg
from math import pi 
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from math import radians
from tf.transformations import quaternion_from_euler,euler_from_quaternion
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  #http://wiki.ros.org/move_base_msgs
from time import sleep
from std_msgs.msg import Int16, Float64,String
from inputimeout import inputimeout, TimeoutOccurred



def movebase_client(pose):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
   # Move forward along the x and y axis of the "map" coordinate frame(in meter)
    goal.target_pose.pose.position.x = pose.position.x
    
    goal.target_pose.pose.position.y = pose.position.y
   # No rotation of the mobile base frame w.r.t. map frame
    goal.target_pose.pose.orientation.x = pose.orientation.x
    goal.target_pose.pose.orientation.y = pose.orientation.y
    goal.target_pose.pose.orientation.z = pose.orientation.z
    goal.target_pose.pose.orientation.w = pose.orientation.w
    
   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available

    if wait:
        sleep(2)
        # moveit_poses()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()

# def moveit_poses():
#     moveit_commander.roscpp_initialize(sys.argv)
#     # rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
#     robot = moveit_commander.RobotCommander()

#     arm_group = moveit_commander.MoveGroupCommander("arm")
#     arm_group.set_named_target("home")
#     plan1 = arm_group.go()

#     gripper_group = moveit_commander.MoveGroupCommander("gripper")
#     gripper_group.set_named_target("gripper_open")
#     plan3 = gripper_group.go()

#     arm_group = moveit_commander.MoveGroupCommander("arm")
#     arm_group.set_named_target("before_pick")
#     plan5 = arm_group.go()
    

#     gripper_group = moveit_commander.MoveGroupCommander("gripper")
#     gripper_group.set_named_target("gripper_close")
#     plan6 = gripper_group.go()

#     rospy.sleep(1)
locations = ['home.txt','table1.txt','table2.txt','table3.txt','kitchen.txt',]

def callbackfun(data):
	print(data.data)
	return data.data


def inp():
    desti = int(input('Enter the table No : '))
    return desti

# def confor():
#     com_me = input("Please Confirm your order with y or n")
#     if (com_me == 'y'):
#         return True
#     else :
#         return False


def timerr():
    try:
        c = inputimeout(prompt='Please Confirm your order with y or n :  ', timeout=10)
        if (c == 'y'):
            return True
        else :
            return False
    except TimeoutOccurred:
        c = 'timeout'
        return False
    




def algo(desi):
    movv = movee(4)
    print("reached "+ locations[4])
    if (movv == True):
        movv_v = movee(desi)
        print("reached "+ locations[desi])
        if(movv_v == True):
            movee(0)
        else:
            movee(4)
        movee(0)
    else:
        movee(0)

    print("reached "+ locations[0])



def movee(loc):
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')

        
        # data = rospy.wait_for_message("/moveit_com/command", Int16)
        # rospy.Subscriber("/moveit_com/command", Int16,callbackfun)
        # places = rospy.Subscriber('/moveit_com/command',Int16)
        # print(places)
        # sub1 = rospy.Subscriber("/moveit_com/command", Int16)
        # pubb = rospy.Publisher('/moveit_com/commandret',Int16, queue_size = 1)
        # print(data)
        # subs = callbackfun()
        # print(subs)



        #get the location of saved text file using ros argument
        rospack = rospkg.RosPack()
        file_path = rospack.get_path('waypoints')
        print(file_path)
        f = open(file_path+"/waypoints/"+locations[loc], "r")
        # iterate through points in file and save as (long,lat) tuple in list points
        points = []
        for lines in f :
            points.append(tuple(map(float,lines.split())))

        print(points)
        n = -1
        rate = rospy.Rate(1)
        while n < len(points) -1:
            n+=1
            x = points[n][0]
            y = points[n][1]
            Y = points[n][2]
            
            pose = Pose()
            pose.position.x= x
            pose.position.y= y
            (qx,qy,qz,qw)= quaternion_from_euler(0,0,Y)
            pose.orientation.x= qx
            pose.orientation.y= qy
            pose.orientation.z= qz
            pose.orientation.w= qw
            q =Quaternion()
            q.x=qx
            q.y=qy
            q.z=qz
            q.w=qw
            pose.orientation = q
            result = movebase_client(pose)
            
               
        moveit_commander.roscpp_shutdown()
        result = movebase_client(pose)
        
        if result:
            print("Goal execution done!")
            print(loc)
            if(loc!=0):
                des = timerr()
                return des
            else:
                return False
        
            
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
        return False
        






if __name__ == "__main__":
    while not rospy.is_shutdown():
        place = inp()
        algo(place)
        # rospy.spin()
    # except rospy.ROSInterruptException:
    #     pass
    