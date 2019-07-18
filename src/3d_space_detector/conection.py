import serial
import time
import math

class open():
    def __init__(self):
        self.conexao = serial.Serial('/dev/ttyACM0', 115200)

        time.sleep(2)

    def send(self, r_vel, l_vel):  # parte do arduino
        if (math.isnan(r_vel) or  math.isnan(l_vel)):
            pass

        else:
            l_vel = int(l_vel)
            r_vel = int(r_vel)
            # print(r_vel, l_vel)
            
            self.conexao.write(str.encode(str(l_vel) + ':' +  str(r_vel) + ';'))