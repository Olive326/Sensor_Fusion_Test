# Sensor_Fusion_test-ROV Vertoical velocity Estimation

## Topic Overview
- /imu/data
- /depth
- vertical_velocity

## Code structure
Sensor_Fusion_Test/
|-Dockerfile
|-README
|-src/
|     |-sensor_fusion_pkg/
|     |  -launch/
|     |       -fusion_launch.py
|     |  -sensor_fusion_pkg/
|     |       -__init__.py
|     |       -fused_data.py
|     |       -fake_imu.py # test unitity
|     |       -fake_depth.py  # test unitity
|     |-package.xml
|     |-setup.cfg
|     |-setup.py
    

## How to run the node
### Step1 - Buid
cd /src
colcon build
### Step2 - Source
source install/setup.bash
### Step3 - Launch
ros2 launch ~/ros2/src/sensor_fusion_pkg/launch/fusion_launch.py

## Run in Docker
### Step1 - Build the image
sudo docker build -t rov_fusion .
### Step2 - Run the container
sudo docker run -it --network host -e ROS_DOMAIN_ID=0 rov_fusion
### Step3 - Verify from inside container
sudo docker exec -it $(sudo docker ps -q) /bin/bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 topic echo /vertical_velocity

