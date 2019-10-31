import math
import pygame

class graphic():
    def __init__(self):
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.SIZE = (1500, 800)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.RAND1 = (46, 3, 27)
        
        self.click = []
        self.path = []

        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)

    def draw_targets(self, targets):
        size = [26, 26]
        for i in range(len(targets)):
            pygame.draw.rect(self.screen, self.RED, [targets[i][1]*100+self.SIZE[0]/2 - size[0]/2, targets[i][0]*100+self.SIZE[1]/2 - size[1]/2, size[0], size[1]])

    def draw_robot(self, point, orientation):
        size = [50, 50]
        robot_icon = pygame.draw.rect(self.screen, self.BLACK, [point[1]*100+self.SIZE[0]/2 - size[0]/2, point[0]*100+self.SIZE[1]/2 - size[1]/2, size[0], size[1]])
        
        icon = pygame.image.load("icon.jpg")
        icon = pygame.transform.scale(icon, [50, 50])
        icon = pygame.transform.rotate(icon, orientation)

        self.screen.blit(icon, robot_icon)

    def draw_obstacles(self, obstacles, correction):
        corrected = []
        for obstacle in obstacles:
            pygame.draw.circle(self.screen, self.RAND1, [int(obstacle[1]*100+self.SIZE[0]/2), int(obstacle[0]*100+self.SIZE[1]/2)], 30)
        
        for element in correction:
            x, y = element[1]*100+self.SIZE[0]/2, element[0]*100+self.SIZE[1]/2
            corrected.append([x, y])

        if len(correction) > 1:
            pygame.draw.lines(self.screen, self.GREEN, False, corrected)

    def graph_op(self, point, orientation, targets, obstacles, correction):
        self.screen.fill(self.BLACK)

        self.draw_targets(targets)
        self.draw_obstacles(obstacles, correction)
        self.draw_robot([point[0], point[1]], orientation - 90)

        self.path.append([point[1] + 25 + 1500, point[0] + 25 + 400])

        # isso deve ser corrigido self.path não está na escala certa
        if len(self.path) > 2:
            pygame.draw.lines(self.screen, self.GREEN, False, self.path)

        self.click = []
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.click == []:
                self.click = pygame.mouse.get_pos()
                break

        pygame.display.update()