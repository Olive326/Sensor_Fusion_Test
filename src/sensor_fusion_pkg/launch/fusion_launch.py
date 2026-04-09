from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # Fake IMU — publishes simulated /imu/data at 100Hz

        Node(
            package    = 'sensor_fusion_pkg',
            executable = 'fake_imu',
            name       = 'fake_imu',
            output     = 'screen',         # print logs to terminal
        ),

        Node(
            package    = 'sensor_fusion_pkg',
            executable = 'fake_depth',
            name       = 'fake_depth',
            output     = 'screen',       
        ),

        Node(
            package    = 'sensor_fusion_pkg',
            executable = 'fused_data',
            name       = 'fused_data',
            output     = 'screen',       
        ),

    ])