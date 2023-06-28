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
        self.xmax = 3.47
        self.ymax = 0.67
        self.xmin = -2.19
        self.ymin = -3.92

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform(
            'map',
            'base_link',
            rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(
            f'Could not transform ')
            return
        

        posx = t.transform.translation.x
        posx = round(posx,2)
        calcx = posx - self.xmin
        normx = calcx/(self.xmax - self.xmin)
        pixx = normx*580
        pixx = int(pixx)
        posy = t.transform.translation.y
        posy= round(posy,2)
        calcy = posy - self.ymax
        normy = calcy/(self.ymax - self.ymin)
        pixy = normy*-475
        pixy = int(pixy)
        
        
        self.get_logger().info('current x = %s current y = %s' % (posx, posy))
        self.get_logger().info('calc pixx: %s calc pixy: %s' % (pixx,pixy))
        f = open("/home/sam/dev_ws/src/tf_publisher/tf_publisher/tfpublish.txt","w")
        f.write("%s \n%s" %(posx , posy))
        f.close()


        



def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
