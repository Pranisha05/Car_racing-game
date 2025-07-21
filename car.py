import pygame
import math
from game_important import scale_image, blit_rotate_center

RED_CAR = scale_image(pygame.image.load('imgs/red-car.png'), 0.4)
GREEN_CAR = scale_image(pygame.image.load('imgs/green-car.png'), 0.4)

class AbstractCar:
    def __init__(self, max_vel, resolution_vel):
        self.vel = 0
        self.max_vel = max_vel
        self.angle = 270
        self.resolution_vel = resolution_vel
        self.img = self.IMG
        self.x, self.y = self.START_POS
        self.acceleration = 0.2
        self.laps = 0
        self.crossed_finish = False  # Helps avoid counting multiple times in one crossing

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.resolution_vel
        elif right:
            self.angle -= self.resolution_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backword(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        theta = math.radians(self.angle)
        vertical = math.cos(theta) * self.vel
        horizontal = math.sin(theta) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        point = mask.overlap(car_mask, offset)
        return point
    
    def collide_with_car(self, other_car):
        car_mask = pygame.mask.from_surface(self.img)
        other_mask = pygame.mask.from_surface(other_car.img)
        
        offset = (int(other_car.x - self.x), int(other_car.y - self.y))
        overlap = car_mask.overlap(other_mask, offset)
    
        return overlap is not None


    def reset(self):
        self.vel = 0
        self.angle = 270
        self.x, self.y = self.START_POS
        self.laps = 0
        self.crossed_finish = False

    def bounce(self):
        self.vel = -self.vel/1.2 
        self.move()

class Player_car1(AbstractCar):
    IMG = RED_CAR
    def __init__(self, max_vel, resolution_vel, start_pos):
        self.START_POS = start_pos
        super().__init__(max_vel, resolution_vel)

class Player_car2(AbstractCar):
    IMG = GREEN_CAR
    def __init__(self, max_vel, resolution_vel, start_pos):
        self.START_POS = start_pos
        super().__init__(max_vel, resolution_vel)

