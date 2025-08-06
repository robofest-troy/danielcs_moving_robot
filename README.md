# danielcs_moving_robot

download

first you have to download the package by clicking the green Code button at the top right corner of the screen in github, then press Download ZIP. Then extract the second_ros2 folder from the zip file into your home. Build Open terminal and enter the second_ros2 folder. finally colcon build the urdf_robot package.

```bash
colcon build --packages-select urdf_robot
```

source install

```bash
source install/setup/bash
```

launch the ros2 state publisher

```bash
ros2 launch urdf_robot launch.py
```

finally, make a new terminal, keep the old one then run the rviz

```bash
rviz2 -d install/urdf_robot/share/urdf_robot/urdf/my_robot.rviz
```
you are now done
