from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.get_logger().info("StatePublisher started")

        self.loop_rate = self.create_rate(30)

        self.angle = 0.0  
        self.degree = pi / 180.0

        self.wheel_rotation_left = 0.0
        self.wheel_rotation_right = 0.0
        self.wheel_radius = 0.041275  
        self.track_width = 0.2658  
        self.joint_names = [
            'front_left_wheel_joint',
            'front_right_wheel_joint',
            'back_left_wheel_joint',
            'back_right_wheel_joint'
        ]

        self.run()

    def run(self):
        joint_state = JointState()
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'base_link'

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = self.joint_names

                
                radius = 2.0 
                angular_velocity = self.degree  
                linear_speed = radius * angular_velocity  

                v_left = linear_speed - (angular_velocity * self.track_width / 2) 
                v_right = linear_speed + (angular_velocity * self.track_width / 2) 

               
                angular_velocity_left = v_left / self.wheel_radius
                angular_velocity_right = v_right / self.wheel_radius

                delta_time = 1.0 / 30.0 
                self.wheel_rotation_left += angular_velocity_left * delta_time  
                self.wheel_rotation_right += angular_velocity_right * delta_time  

                joint_state.position = [
                    self.wheel_rotation_left,  
                    self.wheel_rotation_right,  
                    self.wheel_rotation_left,  
                    self.wheel_rotation_right  
                ]

                odom_trans.header.stamp = now.to_msg()
                odom_trans.transform.translation.x = cos(self.angle) * radius
                odom_trans.transform.translation.y = sin(self.angle) * radius
                odom_trans.transform.translation.z = 0.0
                odom_trans.transform.rotation = euler_to_quaternion(0, 0, self.angle + pi/2)

                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(odom_trans)

                
                self.angle += angular_velocity
                self.loop_rate.sleep()

        except KeyboardInterrupt:
            pass

def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()