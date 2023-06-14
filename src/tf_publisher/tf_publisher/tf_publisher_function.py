import math

from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener



class FrameListener(Node):

    def __init__(self):
        super().__init__('tf_publisher_function')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Call on_timer function every second
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform(
            'base_link',
            'map',
            rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(
            f'Could not transform ')
            return
        

        posx = t.transform.translation.x
        posx = round(posx,2)
        posy = t.transform.translation.y
        posy= round(posy,2)
        self.get_logger().info('current x = %s current y = %s' % (posx, posy))
        f = open("/home/sam/dev_ws/src/tf_publisher/tf_publisher/tfpublish.txt","w")
        f.write("x: %s y: %s " %(posx , posy))
        f.close()


        



def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()