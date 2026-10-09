import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Check if we are using ros2_control
    use_ros2_control = LaunchConfiguration('use_ros2_control')


    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'lemower_package'
    file_subpath = 'description/lemower.xacro'


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    # robot_description_raw = xacro.process_file(xacro_file).toxml()
    robot_description_config = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control, ' sim_mode:=', use_sim_time])


    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
    #    parameters=[{'robot_description': robot_description_raw, 'use_sim_time': use_sim_time}] # add other parameters here if required
        parameters=[{'robot_description': robot_description_config, 'use_sim_time': use_sim_time}] 
    )


    # Run the node
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'),
        node_robot_state_publisher
    ])
