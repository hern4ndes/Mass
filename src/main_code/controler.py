# from rplidar import RPLidar
# lidar = RPLidar('/dev/ttyUSB0')
import inputs
import serial

conexao = serial.Serial('/dev/ttyUSB0', 9600)

print(inputs.devices.gamepads)
while conexao.isOpen():
    events = inputs.get_gamepad()
    for event in events:

        # if(event.code == "ABS_Z"):
        #     print("ABS_Z = {}".format(event.state))
        # if( event.code=="ABS_RZ"):
        #     print("ABS_RZ = {}".format(event.state))
        if event.code == 'ABS_HAT0Y' and event.state == -1:
            print('frente!')
            conexao.write('2')
        elif event.code == 'ABS_HAT0Y' and event.state == 1:
            print('traz!')
            conexao.write('3')
        elif event.code == 'ABS_HAT0Y' and event.state == 0:
            print('parar Y')
            conexao.write('1')
        if event.code == 'ABS_HAT0X' and event.state == -1:
            print('esquerda!')
            conexao.write('4')
        elif event.code == 'ABS_HAT0X' and event.state == 1:
            print('direita!')
            conexao.write('5')
        elif event.code == 'ABS_HAT0X' and event.state == 0:
            print('parar  X')
            conexao.write('1')
