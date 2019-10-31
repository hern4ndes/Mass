import math
import numpy
import lidar
import serial
import rrtBezier
import conection
import graphic_representation

from time import sleep
from scipy.spatial import distance

class essentials():
    def __init__(self, debug):
        self.debug = debug
        self.rot_max = 100
        self.vel_max = 150

        self.last_ang_error = 0
        self.last_dist_error = 0

        self.path = []
        self.obstructed = False  # indicador de caminho obstruido por obstaculo móvel

        self.X = 800  # comprimento em cm do eixo x da área de cobertura
        self.Y = 1500  # comprimento em cm do eixo y da área de cobertura
        self.rrt = rrtBezier.bezier(self.X, self.Y)
        self.rplidar = lidar.m_lidar()
        self.py_graph = graphic_representation.graphic()
        
        self.first = []
        self.obs_avoid = []
        self.counter = 0

        if self.debug == '1':
            self.arduino = conection.open()

    def calculate_angle_error(self, pos, target, orientation):
        x_dif = target[0] - pos[0]  # diferença entre as posições em x
        y_dif = target[1] - pos[1]  # diferença entre as posições em y

        actual_angle = orientation

        # Correção do ângulo atual
        while actual_angle > 360:
            actual_angle -= 360
        while actual_angle < 0:
            actual_angle += 360
        
        # Cálculo do ângulo ideal
        if x_dif != 0 and y_dif != 0:
            ideal_angle = (180/math.pi)*numpy.arctan(y_dif/x_dif)
            ideal_angle = round(ideal_angle, 2)

            sig_x = x_dif/abs(x_dif)
            sig_y = y_dif/abs(y_dif)

            if (sig_x == -1 and sig_y == -1) or (sig_x == -1 and sig_y == 1):
                ideal_angle += 180
            else:
                ideal_angle += sig_x*(180) + sig_y*(-180)
        
        else:
            ideal_angle = 0

        # Correção do ângulo ideal
        while ideal_angle > 360:
            ideal_angle -= 360
        while ideal_angle < 0:
            ideal_angle += 360

        # Cálculo do erro do ângulo
        rot = (ideal_angle - actual_angle)

        if actual_angle > 270 and ideal_angle < actual_angle - 180:
            rot = ideal_angle + (360 - actual_angle)
        if actual_angle < ideal_angle - 180 and ideal_angle > 270:
            rot = -actual_angle - (360 - ideal_angle) 

        # Correção do rot baseado no real eixo de rotação (eixo do robô, não da zed)
        if abs(rot) < 60:
            d1 = (x_dif**2 + y_dif**2)**(1/2)
            tan_real = (numpy.tan(orientation)*d1*numpy.cos(rot))/(0.24 + d1*numpy.cos(rot))
            rot = numpy.arctan(tan_real)*abs(rot)/rot
        
        return rot

    def calculate_path(self, targets, pos, orientation):
        if targets != []:
            # Cálculo e gravação da posição absoluta de novos alvos
            theta = numpy.radians(-(orientation-90))
            cos_t, sin_t = numpy.cos(theta), numpy.sin(theta)
            r_mat = [[cos_t,-sin_t], [sin_t, cos_t]]
            abs_targets = []
            
            for target in targets:
                x_target, y_target = numpy.dot([target[0], target[1]], r_mat)
                x_target, y_target = x_target + pos[0], y_target + pos[1]

                abs_targets.append([round(x_target, 2), round(y_target, 2)])

            # "Tracking" dos alvos
            for detected in abs_targets:
                for point in self.path:
                    if distance.euclidean(point, detected) < 0.8:
                        self.path.pop(self.path.index(point))
                        break

            # Gravação de alvos conferidos
            for detected in abs_targets:
                self.path.append(detected)

            # Ordenação dos alvos salvos
            if len(self.path) > 1:
                ref = pos
                saved_targets = []
                
                for k in range(len(self.path)):
                    minimum = 10000
                    for point in self.path:
                        dist = distance.euclidean(ref, point)
                        if ref != point:
                            if dist < minimum:
                                if point not in saved_targets:
                                    minimum = dist
                                    aux = point
                    
                    ref = aux
                    saved_targets.append(ref)

                self.path = saved_targets

        # Verificação de "coleta"
        # if self.path != []:
        #     for point in self.path:
        #         if distance.euclidean(pos, point) < 0.15:
        #             self.path.pop(self.path.index(point))
        #             break

        # Adição de alvos por clique
        if self.py_graph.click != []:
            self.path.append([(self.py_graph.click[1]-self.X/2)/100, (self.py_graph.click[0]-self.Y/2)/100])

    def rot_pid(self, rot):
        a_kp = 2 #1.8
        a_ki = 0*1/200
        a_kd = 3.8 #3.5

        ang_error = (rot)
        ang_error_sum = (ang_error + self.last_ang_error)
        ang_error_dif = (ang_error - self.last_ang_error)
        self.last_ang_error = ang_error

        rot = ang_error*a_kp + ang_error_sum*a_ki + ang_error_dif*a_kd

        # Estabelecimento do limite de velocidade
        if rot > self.rot_max:
            rot = self.rot_max
        if rot < -self.rot_max:
            rot = -self.rot_max
        
        # Estabelecimento de condições de parada
        lim = 0.5
        if rot > lim:
            rot += 40
        elif rot < -lim:
            rot -= 40
        elif rot <= lim and rot >= -lim:
            rot = 0

        # Filtro
        if not math.isnan(rot):
            r_rot = int(rot*(2/3))
            l_rot = -int(rot)
        else:    
            r_rot = 0
            l_rot = 0

        return l_rot, r_rot

    def walk_pid(self, dist):
        w_kp = 4
        w_ki = 0*1/200
        w_kd = 0*3.5

        dist_error = dist
        dist_error_sum = (dist_error + self.last_dist_error)
        dist_error_dif = (dist_error - self.last_dist_error)
        self.last_dist_error = dist_error

        vel = dist_error*w_kp + dist_error_sum*w_ki + dist_error_dif*w_kd

        # estabelecimento do limite de velocidade
        if vel > self.vel_max:
            vel = self.vel_max
        if vel < -self.vel_max:
            vel = -self.vel_max
        
        # estabelecimento de condições de parada
        lim = 0.5
        if vel > lim:
            vel += 50
        elif vel < -lim:
            vel -= 50
        elif vel <= lim and vel >= -lim:
            vel = 0

        # Filtro
        if not math.isnan(vel):
            r_walk = int(vel*(0.8))
            l_walk = int(vel)
        else:
            r_walk = 0
            l_walk = 0

        return l_walk, r_walk

    def obstacle_avoidance(self, obstacles, pos):
        escaled = []
        correction = []

        x_ = self.X/2
        y_ = self.Y/2

        # Mudança de escala
        for absl in obstacles:
            x = int(absl[0]*100+x_)
            y = int(absl[1]*100+y_)

            escaled.append([x, y])
        
        # Calcular o RRT usando os pontos como obstáculos
        posx = int((pos[0]*100)+x_)
        posy = int((pos[1]*100)+y_)
        tx = int((self.first[0]*100)+x_)
        ty = int((self.first[1]*100)+y_)
        
        correction = self.rrt.main(escaled, [posx, posy], [tx, ty])

        # Retomada de escala
        for point in correction:
            point[0] = (point[0]-x_)/100
            point[1] = (point[1]-y_)/100

        # O primeiro da lista é a posição atual do robô
        correction.pop(0)

        return correction

    def get_lidar_points(self, pos, orientation):
        self.rplidar.listener()
        raw_points = []
        lidar_points = []
        near_obstacles = []

        r_orientation = orientation*math.pi/180
        d_min_ang = self.rplidar.ang_var[0] + 2*math.pi  # parcela para evitar ângulos negativos
        d_max_ang = self.rplidar.ang_var[1] + 2*math.pi  # parcela para evitar ângulos negativos
        
        if len(self.rplidar.m_ranges) > 0:
            ang_range = d_max_ang - d_min_ang
            ang_var = ang_range/len(self.rplidar.m_ranges)
            
            for i in range(len(self.rplidar.m_ranges)):
                # Retirada de ranges infinitos do lidar
                if self.rplidar.m_ranges[i] == math.inf:
                    continue
                else:
                    # Parcelas adicionadas a ang_var*i para manter os pontos do lidar estáticos enquanto ele gira
                    raw_points.append([self.rplidar.m_ranges[i], ang_var*i - math.pi/2 + r_orientation - math.pi/2])

            # Adição dos pontos relativos
            for point in raw_points:
                x = point[0]*numpy.cos(point[1])
                y = point[0]*numpy.sin(point[1])
                
                lidar_points.append([x, y])

            # Transformar coordenadas relativas em absolutas
            for rel in lidar_points:
                rel[0] += pos[0] # rel[0] = round(rel[0] + pos[0], 2)
                rel[1] += pos[1] # rel[1] = round(rel[1] + pos[1], 2)

                # Adição de obstáculos próximos ao robô
                if distance.euclidean(rel, pos) < 1.5:
                    near_obstacles.append(rel)

        return lidar_points, near_obstacles

    def verify_obstruction(self, near_points, path, obst_radius):
        dist = obst_radius + 2
        for obstacle in near_points:
            for i in range(0, len(path), int(len(path)/5)):
                dist = distance.euclidean(obstacle, path[i])
                if (dist < obst_radius):
                    return True
        return False

    def set_ang_and_vel(self, detected_targets, pos, orientation):
        lidar_points, near_obs = self.get_lidar_points(pos, orientation)
        # lidar_points = []
        # near_obs = []
        # Ordenação dos alvos vistos e cálculo de trajetória (atualização de self.path)
        self.calculate_path(detected_targets, pos, orientation)

        if self.path == []:
            l_wheel = 0
            r_wheel = 0
        
        else:
            # Cálculo do desvio de obstáculos considerando como end point o primeiro alvo
            if self.first != self.path[0] or self.obstructed == True:
                self.first = self.path[0]
                self.obs_avoid = self.obstacle_avoidance(lidar_points, pos)
                # self.obs_avoid.pop(0)
                self.obstructed = False

            # Escolher entre seguir para o alvo ou seguir o desvio de obstáculos
            if self.obs_avoid != []:
                def_path = self.obs_avoid
            else:
                def_path = self.path

            # Verificação de obstrução do caminho
            self.obstructed = self.verify_obstruction(near_obs, def_path, obst_radius=0.3)

            # Verificação de "coleta"
            for point in def_path:
                if distance.euclidean(pos, point) < 0.40:
                    def_path.pop(def_path.index(point))
                    break

            # Cálculo dos erros de ângulo e distância em relação so primeiro alvo da lista
            angle_error = self.calculate_angle_error(pos, [def_path[0][0], def_path[0][1]], orientation)
            pos_error = distance.euclidean(pos, [def_path[0][0], def_path[0][1]])

            # Algoritmos de PID e composição das velocidades
            l_rot, r_rot = self.rot_pid(angle_error)
            l_walk, r_walk = self.walk_pid(pos_error)

            l_wheel = l_rot + l_walk
            r_wheel = r_rot + r_walk

        self.py_graph.graph_op(pos, orientation, self.path, lidar_points, self.obs_avoid)
        
        if self.debug == '1':
            self.arduino.send(l_wheel, r_wheel)