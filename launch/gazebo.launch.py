import os
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument

def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    package_name='lemower_package'

    world_subpath='description/monde_olivier.sdf'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    world = LaunchConfiguration('world')
    world_file = os.path.join(get_package_share_directory(package_name),world_subpath)

    world_arg = DeclareLaunchArgument(
        name='world', default_value=world_file,
        description='World to load'
    )

    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo_server = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
                    launch_arguments={'gz_args': ['-r -s -v1 ', world], 'on_exit_shutdown': 'true'}.items()
             )
    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo_client = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
                    launch_arguments={'gz_args': '-g '}.items()
             )

    # Run the spawner node from the ros_gz_sim package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'lemower',
                                   '-z', '0.1'],
                        output='screen')



    bridge_params = os.path.join(get_package_share_directory(package_name),'config','gz_bridge.yaml')

    gz_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
	arguments=[
		'--ros-args',
		'-p',
		f'config_file:={bridge_params}',]
    )


    # Run the node
    return LaunchDescription([
        world_arg,
        rsp,
        gazebo_server,
	gazebo_client,
	gz_bridge_node,
	spawn_entity
    ])



