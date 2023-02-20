#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

class DeliveryNode:
    def __init__(self):
        # Initialize node and create publisher for delivery confirmation
        rospy.init_node('delivery_node')
        self.delivery_pub = rospy.Publisher('/delivery_confirmation', String, queue_size=10)
        
        # Subscribe to order topic
        rospy.Subscriber('/order', String, self.delivery_callback)
        
    def delivery_callback(self, order):
        # Receive order and extract table number
        order_info = order.data.split(',')
        table_num = order_info[0].split(' ')[-1]
        
        # Deliver food to table and publish confirmation
        rospy.loginfo(f"Delivering food to table {table_num}")
        confirmation_msg = f"Delivery to table {table_num} complete."
        self.delivery_pub.publish(confirmation_msg)
        
if __name__ == '__main__':
    try:
        DeliveryNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
