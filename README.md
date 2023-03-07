# PySimbot

PySimbot is a software for simple robot simulation. In the simulation map, robots with a set of sensors and movements try to reach the food. PySimbot let you program the robot logic and take the food as much as possible.

## Installation

- Install Python3 (The supported version currently are [3.6-3.9](https://www.python.org/downloads/))
- If needed, you may create [virtualenv](https://virtualenv.pypa.io/en/latest/) before installing the libraries.
- To install the libraries, use the program such as cmd, powershell, or terminal. The command will be based on your OS.
- for Windows, `pip install -r requirements_windows.txt`
- for macOS, `pip3 install -r requirements_macos.txt`
- for Linux, `pip3 install -r requirements_linux.txt`

## Getting Start

- Run an example code to understand how PySimbot works. There are many example codes for different use cases.
```Shell
python example1_wasd_robot.py
python example2_sensors.py
python example3_randomwalk_robot.py
...
```
- You can see the messages in the command window while running an example. It will describe the current simulation.
- The coding logic of the simulation is wrapped in the library. You mostly do nothing on handling the UI and Physics of the simulation.
- Keep focusing on the robot logic.

> See more in [Example1](/example1_wasd_robot.py)

## Robot
`pysimbotlib.core.Robot` defines the basic functions of the robot. 
We can control the robot programmatically and see how it moves on the map.

### Robot sensors
In simulation, two kinds of sensors are defined.

- **8 distance sensors** measure the distance from the edge of the robot to the obstacle and wall. The sensor are located around the robots in 8 directions (+45 degrees for every sensor starting from the robot front edge). These sensors has operational length of 100 pixels. If there is no obstacle and wall in the operation range, the sensors will return 100.

- **1 smell sensor** measures the angle in degree (-180 to 180) from the robot center position to the specified food. If the food is on the left of robot the angle will be negative. If the food is on the right of the robot the angle will be positive.

> See more in [Example2](/example2_sensors.py)

### Robot movements
To move the robot, two operations are allowed.

- **turn(degree)** to turn the robot around its center for `degree` degree. The negative degree means turn left. On the other hand, the positive degree means turn right.

- **move(step)** to go forward or backward for `step` pixels. Use positive value to go forward and negative value to go backward. 

### Extending the Robot class
You can create your own Robot code by extends the pysimbotlib.core.Robot class. The `update()` method should make a robot move based on the sensor.
```
class CircularRobot(Robot):
    def update(self):
        self.move(5)
        self.turn(15)
```
By passing your own class as a parameter of PySimbotApp constructor, the simulation will replace the default robot with your robot.
```
app = PySimbotApp(robot_cls=CircularRobot)
```

> See more in [Example3](/example3_randomwalk_robot.py)

### Robot Class
The robot class contains following properties and methods.

|     Property      |        Type       |                             Description                             |
|:------------------|:-----------------:|:--------------------------------------------------------------------|
| `color`           | Tuple[r,g,b,a]    | color of the robot                                                  |
| `eat_count`       | int               | number of foods that robot has eaten                                |
| `collision_count` | int               | number of collisions that the robot made                            |
| `just_eat`        | bool              | flag that would be True if the robot ate food in the last iteration |
| `stuck`           | bool              | flag that would be True when the robot is stuck to the wall         |

|     Method             | Return Type |                                    Description                                                      |
|:-----------------------|:-----------:|:----------------------------------------------------------------------------------------------------|
| `update()`             | None        | update the robot state for each simbot's iteration                                                  |
| `set_color(r,g,b,a)`   | None        | color the robot. The values of (r, g, b, a) are between 0 to 1. (a is optional, default to 1)       |
| `turn(degree)`         | None        | turn the robot by the specifying degree (floating point number)                                     |
| `move(step)`           | None        | move the robot forward by the specified step (integer number). The robot will not move if collides. |
| `distance()`           | Tuple[float,...,float]| get the 8 sensor distances in pixels from the sensors around the robot side               |
| `smell(index)`         | float       | get the turning angle to the food corresponding to the food index. (index is optional, default to 0)|
| `smell_nearest()`      | float       | get the turning angle to the nearest food                                                           |


## Advanced usages

You can configure the PySimbotApp in several ways by passing the parameters to the PySimbotApp's constructor.

|  parameter                   |Type               |  description                                                                            |
|:-----------------------------|-------------------|:----------------------------------------------------------------------------------------|
| `robot_cls`                  | Robot-based Class | Class of the robot for initializing all robots in the simulation                        |
| `num_robots`                 | int               | Number of robots created in the simulation                                              |
| `num_objectives`             | int               | Number of foods created in the simuation (index of food start by 0)                     |
| `robot_default_start_pos`    | Tuple[int,int]    | Starting position of the robot in XY pixels unit.                                       |
| `obj_default_start_pos`      | Tuple[int,int]    | Starting position of the food in XY pixels unit.                                        |
| `interval`                   | float             | Minimum time interval in seconds between each frame of simulation                       |
| `max_tick`                   | int               | Maximum number of frame for a simulation                                                |
| `map`                        | str               | Map name as defined in pysimbotlib/maps folder. Default value is 'default'              |
| `theme`                      | str               | Theme as defined pysimbotlib/themes folder. Default value is 'default'                  |
| `customfn_create_robots`     | function          | Function that returns a list of robots. PySimbotApp will override the robots initialization process by this function  |
| `simulation_forever`         | bool              | Enable/Disable simulation in the infinite loop. If `True`, you can test your robots multiple times or you can try algorithm that based on the iterative improvement. |
| `customfn_before_simulation` | function          | Task to runs before each simulation. You can do things such as managing map, or writing a log file. |
| `customfn_after_simulation`  | function          | Task to runs after each simulation. You can do things such as writing a log file.       |
| `enable_wasd_control`        | bool              | Enable/Disable the WASD control using keyboard.                                         |
| `food_move_after_eat`        | bool              | Enable/Disable changing position of food after the robot eat.                           |
| `save_wasd_history`          | bool              | Enable/Disable the WASD history. In each simulation, the values of `distance()`, `smell()`, `move` and `turn` when user control the robots would be recorded to file. |
| `robot_see_each_other`       | bool              | Enable/Disable the robot to see the other robots. This also related to distance calculation and robot-to-robot collision. |
