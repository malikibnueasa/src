#!/usr/bin/env python3

import rospy

from std_msgs.msg import String

class OrderNode:

    def __init__(self):
        self.table_orders = {}
        self.table_confirmations = {}
        self.order_sub = rospy.Subscriber('order', String, self.order_callback)
        self.confirmation_sub = rospy.Subscriber('confirmation', String, self.confirmation_callback)
        self.delivery_pub = rospy.Publisher('delivery', String, queue_size=10)

    def order_callback(self, msg):
        order = msg.data
        table = order.split(',')[0]
        item = order.split(',')[1]

        if table in self.table_orders:
            self.table_orders[table].append(item)
        else:
            self.table_orders[table] = [item]

        rospy.loginfo('Order received for Table %s: %s', table, item)

    def confirmation_callback(self, msg):
        confirmation = msg.data
        table = confirmation.split(',')[0]
        item = confirmation.split(',')[1]

        if table in self.table_confirmations:
            self.table_confirmations[table].append(item)
        else:
            self.table_confirmations[table] = [item]

        rospy.loginfo('Confirmation received for Table %s: %s', table, item)

    def deliver_orders(self):
        for table in self.table_orders:
            if table not in self.table_confirmations:
                self.delivery_pub.publish(table + ',None')
            else:
                for item in self.table_orders[table]:
                    if item not in self.table_confirmations[table]:
                        self.delivery_pub.publish(table + ',' + item)
        self.table_orders = {}
        self.table_confirmations = {}

    def start_node(self):
        rospy.init_node('order_node', anonymous=True)
        rate = rospy.Rate(1)

        while not rospy.is_shutdown():
            self.deliver_orders()
            rate.sleep()

if __name__ == '__main__':
    order_node = OrderNode()
    order_node.start_node()
