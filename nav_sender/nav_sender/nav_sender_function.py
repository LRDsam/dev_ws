#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by AutomaticAddison.com
 
import time  # Time library
 
from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2
from rclpy.node import Node
 
from robot_navigator import BasicNavigator, NavigationResult # Helper module
 
class NavSender(Node):
    
    

    def __init__(self):
        super().__init__('nav_sender_function')
        self.navigator = BasicNavigator()
        self.status = "WAIT"
        self.xDoel = 0
        self.yDoel = 0
        self.timer = self.create_timer(0.5, self.on_timer)

    def check_for_new_data(self):
        f = open("/home/sam/dev_ws/Expo4-main/CoordinatesDestination.txt","r")
        lines = f.readlines()
        fileX = float(lines[0])
        fileY = float(lines[1])
        if not fileX == self.xDoel:
            self.xDoel = fileX
            self.yDoel = fileY
            self.status = "SET_GOAL"

    
    def on_timer(self):
        if self.status == "WAIT":
            # Read the file and check if the data has changed 
            self.check_for_new_data()
        elif self.status == "SET_GOAL":
            #if value has changed sent the goal pose to the navigation stack
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x = self.xDoel
            goal_pose.pose.position.y = self.yDoel
            goal_pose.pose.position.z = 0.0
            goal_pose.pose.orientation.x = 0.0
            goal_pose.pose.orientation.y = 0.0
            goal_pose.pose.orientation.z = 0.0
            goal_pose.pose.orientation.w = 1.0
            self.navigator.goToPose(goal_pose)
            self.status =="NAVIGATING"
        elif self.status == "NAVIGATING":
            if not self.navigator.isNavComplete():
                #check if the value has changed and if so set status to SET_GOAL
                self.check_for_new_data()
            else:
                result = self.navigator.getResult()
                if result == NavigationResult.SUCCEEDED:
                    print('Goal succeeded!')
                elif result == NavigationResult.CANCELED:
                    print('Goal was canceled!')
                elif result == NavigationResult.FAILED:
                    print('Goal failed!')
                else:
                    print('Goal has an invalid return status!')
                self.status = "WAIT"

            



def main():
    rclpy.init()
    node = NavSender()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
            

