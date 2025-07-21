import pygame
import time

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def control_of_player1(player_car1):
    moved = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moved = True
        player_car1.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car1.move_backword()
    if keys[pygame.K_a]:
        player_car1.rotate(left=True)
    if keys[pygame.K_d]:
        player_car1.rotate(right = True)

    if not moved:
        player_car1.reduce_speed()

def control_of_player2(player_car2):
    moved = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        moved = True
        player_car2.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car2.move_backword()
    if keys[pygame.K_LEFT]:
        player_car2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car2.rotate(right = True)

    if not moved:
        player_car2.reduce_speed()

def blit_text_center(win, font, text, y_offset=0):
    render = font.render(text, True, (255, 255, 255))
    rect = render.get_rect(center=(win.get_width() // 2, win.get_height() // 2 + y_offset))
    win.blit(render, rect)

class Game_info:

    def __init__(self):
        self.started = False
        self.level_start_time = 0

    def reset(self):
        self.started = False
        self.level_start_time = 0

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def game_level_time(self):
        if not self.started:
            return 0
        return time.time() - self.level_start_time
