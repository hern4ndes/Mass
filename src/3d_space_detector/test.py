import basic_movement as basis

zed_robot = basis.essentials(0)

while 1:
    zed_robot.set_ang_and_vel([], [0, 0], 90)