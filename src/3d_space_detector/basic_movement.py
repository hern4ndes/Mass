import math
import numpy
import serial

from time import sleep

conexao = serial.Serial('/dev/ttyACM0', 115200)

class essentials():
    def __init__(self):
        self.rot_max = 100
        self.vel_max = 150

        self.last_ang_error = 0
        self.last_vel_error = 0
        
        sleep(2)
        
    def ardu_serial(self, r_vel, l_vel):  # parte do arduino
        if (math.isnan(r_vel) or  math.isnan(l_vel)):
            pass

        else:
            l_vel = int(l_vel)
            r_vel = int(r_vel)
            # print(r_vel, l_vel)
            
            conexao.write(str.encode(str(l_vel) + ':' +  str(r_vel) + ';'))
            

    def set_ang_and_vel(self, targets, pos, orientation):
        # levando que o angulo do robô não ultrapasse 360 e seja maior que 0
        # levando em conta a lente direita como eixo e centróide

        if targets == []:
            self.ardu_serial(0, 0)
            pass
            
        else:
            # antigo
            x_target = targets[0][0]
            y_target = targets[0][1]

            # novo
            # y_target = targets[0][0]
            # x_target = -targets[0][1]

            x_zed = pos[0]
            y_zed = pos[1]
            actual_angle = orientation

            # Correção do ângulo atual
            while actual_angle > 360:
                actual_angle -= 360

            while actual_angle < 0:
                actual_angle += 360

            # Obtenção do ângulo ideal
            x_dif = x_target #- x_zed  # diferença entre as posições em x
            y_dif = y_target #- y_zed  # diferença entre as posições em y

            if x_dif != 0:
                ideal_angle = (180/math.pi) * numpy.arctan(y_dif/x_dif)  # ângulo ideal para o robô
                ideal_angle = round(ideal_angle, 2)  # arrendondar o valor do ângulo ideal
            else:
                ideal_angle = 0

            try:
                sig_x = x_dif/abs(x_dif)
                sig_y = y_dif/abs(y_dif)
            except ZeroDivisionError:
                sig_x = 0
                sig_y = 0

            if (sig_x == -1 and sig_y == -1) or (sig_x == -1 and sig_y == 1):
                ideal_angle += 180
            else:
                ideal_angle += sig_x*180 + sig_y*(-180)

            ideal_angle -= 90

            # Correção do ângulo ideal
            while ideal_angle > 360:
                ideal_angle -= 360

            while ideal_angle < 0:
                ideal_angle += 360

            # Cálculo do erro
            rot = (ideal_angle - actual_angle)

            if actual_angle > 270 and ideal_angle < actual_angle - 180:
                rot = ideal_angle + (360 - actual_angle)

            if actual_angle < ideal_angle - 180 and ideal_angle > 270:
                rot = -actual_angle - (360 - ideal_angle)

            # Algoritmo de PID
            a_kp = 0.1
            a_ki = 0*1/1000
            a_kd = 0*1/1000

            ang_error = (rot)
            ang_error_sum = (ang_error + self.last_ang_error)
            ang_error_dif = (ang_error - self.last_ang_error)
            self.last_ang_error = ang_error

            rot = ang_error*a_kp + ang_error_sum*a_ki + ang_error_dif*a_kd

            # estabelecimento do limite de velocidade
            if rot > self.rot_max:
                rot = self.rot_max
            
            if rot < -self.rot_max:
                rot = -self.rot_max
            
            if rot < 50 and rot > 0:
                rot = 50

            if rot > -50 and rot < 0:
                rot = -50

            rot = round(rot, 2)

            r_wheel =  rot*(2/3)
            l_wheel = -rot

            # print("velocidades: ", l_wheel, r_wheel, "/ angulo atual: ", actual_angle, "/ angulo ideal", ideal_angle)

            self.ardu_serial(r_wheel, l_wheel)