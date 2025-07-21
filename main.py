import pygame 
from car import Player_car1, Player_car2
from game_important import scale_image, blit_text_center, control_of_player1, control_of_player2, Game_info

MAPS = {
    "Easy":{
        "track": "imgs/track1.png",
        "border": "imgs/track1_border.png",
        "car1_start": (442, 400),
        "car2_start": (442, 435),
        "finish_pos": (400, 384)

    },
    "Hard":{
        "track": "imgs/track2.png",
        "border": "imgs/track2_border.png",
        "car1_start": (440, 535),
        "car2_start": (440, 558),
        "finish_pos": (415, 531)
    }
}

pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((1162,678))
BACKGROUND = pygame.image.load('imgs/background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (1162, 678))
MENU_BG = pygame.image.load('imgs/menu_bg.png')
MENU_BG = pygame.transform.scale(MENU_BG, (1162, 678))
FINISH = pygame.image.load('imgs/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)

MAIN_FONT = pygame.font.SysFont("comicsans", 30)

BUTTONS1 = pygame.image.load("imgs/easy.png") 
BUTTONS2 = pygame.image.load("imgs/hard.png")

class Button:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.draw()
        self.rect=self.img.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
    def draw(self):
        WIN.blit(self.img,(self.x,self.y))

    def check_click(self):
        mouse_pos=pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if left_click and self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

def show_splash_screen(win, bg_img, duration=3):
    win.blit(bg_img, (0, 0))
    pygame.display.update()
    pygame.time.delay(duration * 1000)  # 3 seconds

def show_main_menu(win):
    run = True
    selected_level = None  # To store chosen level
    
    while run:
        win.blit(MENU_BG, (0, 0))
        easy_button = Button(110,395,BUTTONS1) 
        hard_button = Button(710, 395, BUTTONS2)
        pygame.display.update()
        # print(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.check_click():
                    selected_level = "Easy"
                    run = False
                    break
                elif hard_button.check_click():
                    selected_level = "Hard"
                    run = False
                    break

    return selected_level

def load_map(map_info):
    map_data = MAPS[map_info]

    track_img = scale_image(pygame.image.load(map_data["track"]), 0.9)
    border_img = scale_image(pygame.image.load(map_data["border"]), 0.9)
    border_mask = pygame.mask.from_surface(border_img)

    car1_start = map_data["car1_start"]
    car2_start = map_data["car2_start"]
    finish_pos = map_data["finish_pos"]

    return track_img, border_img, border_mask, car1_start, car2_start, finish_pos

def draw(win, images, player_car1, player_car2, game_info):
    for img, pos in images:
        win.blit(img, pos)

    time_text = MAIN_FONT.render(f'Time - {round(game_info.game_level_time(), 1)}', 1, (255, 255, 255))
    win.blit(time_text, (500, win.get_height() - 50))

    player1_vel_text = MAIN_FONT.render(f'Red car -vel {round(player_car1.vel,1)}', 1, (255,255,255))
    win.blit(player1_vel_text, (10, win.get_height() - 80))
    player2_vel_text = MAIN_FONT.render(f'Green car -vel {round(player_car2.vel, 1)}', 1, (255,255,255))
    win.blit(player2_vel_text, (910, win.get_height() - 80))
    
    
    player1_lap_text = MAIN_FONT.render(f'Laps: {player_car1.laps}', 1, (255, 255, 255))
    win.blit(player1_lap_text, (10, win.get_height() - 50))
    player2_lap_text = MAIN_FONT.render(f'Laps: {player_car2.laps}', 1, (255, 255, 255))
    win.blit(player2_lap_text, (910, win.get_height() - 50))
    player_car1.draw(win)
    player_car2.draw(win)

    pygame.display.update()

def handle_collision(player_car1, player_car2, game_info):
    for car in [player_car1, player_car2]:
        if car.collide(TRACK_BORDER_MASK) != None:
            car.bounce()

    #handle collision between cars
    if player_car1.collide_with_car(player_car2):
        player_car1.bounce()
        player_car2.bounce()
    if player_car2.collide_with_car(player_car1):
        player_car2.bounce()
        player_car1.bounce()

    #Handle red car
    finish_1 = player_car1.collide(FINISH_MASK, *FINISH_POS)
    
    if finish_1 != None:
        if player_car1.vel < 0:
            player_car1.bounce()
    
    if finish_1:
        if finish_1[0] == 0 and not player_car1.crossed_finish:
            player_car1.laps += 1
            player_car1.crossed_finish = True
    else:
        player_car1.crossed_finish = False

    # Handle green car
    finish_2 = player_car2.collide(FINISH_MASK, *FINISH_POS)

    if finish_2 != None:
        if player_car2.vel < 0:
            player_car2.bounce()
    
    if finish_2:
        if finish_2[0] == 0 and not player_car2.crossed_finish:
            player_car2.laps += 1
            player_car2.crossed_finish = True
    else:
        player_car2.crossed_finish = False
 
    # Check for winner after 2 laps
    if player_car1.laps >= 2:
        blit_text_center(WIN, MAIN_FONT, 'Red car Wins after 2 laps!')
        pygame.display.update()
        pygame.time.wait(3000)
        player_car1.reset()
        player_car2.reset()
        game_info.reset()
        return

    if player_car2.laps >= 2:
        blit_text_center(WIN, MAIN_FONT, 'Green car Wins after 2 laps!')
        pygame.display.update()
        pygame.time.wait(3000)
        player_car1.reset()
        player_car2.reset()
        game_info.reset()
        return

def main():
    global TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH_POS
    pygame.display.set_caption("2 Player Racing Game")

    show_splash_screen(WIN, BACKGROUND)

    selected_difficulty = show_main_menu(WIN)
    TRACK, TRACK_BORDER, TRACK_BORDER_MASK, car1_pos, car2_pos, FINISH_POS = load_map(selected_difficulty)

    images = [(TRACK, (0, 0)), (TRACK_BORDER, (0, 0))]
    if selected_difficulty == "Easy":
        images = [(TRACK, (0, 0)), (FINISH, FINISH_POS), (TRACK_BORDER, (0, 0))]
        
    running = True
    player_car1 = Player_car1(4, 4, car1_pos)
    player_car2 = Player_car2(4, 4, car2_pos)
    game_info = Game_info()
    FPS = 60
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(FPS)
        draw(WIN, images, player_car1, player_car2, game_info)
        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f'Press any key to start')
            # print(pygame.mouse.get_pos())
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selected_difficulty = show_main_menu(WIN)
                        game_info.reset()
                        player_car1.reset()
                        player_car2.reset()
                        TRACK, TRACK_BORDER, TRACK_BORDER_MASK, car1_pos, car2_pos, FINISH_POS = load_map(selected_difficulty)
                        images = [(TRACK, (0, 0)), (TRACK_BORDER, (0, 0))]
                        if selected_difficulty == "Easy":
                            images = [(TRACK, (0, 0)), (FINISH, FINISH_POS), (TRACK_BORDER, (0, 0))]
                        player_car1 = Player_car1(4, 4, car1_pos)
                        player_car2 = Player_car2(4, 4, car2_pos) 
                        draw(WIN, images, player_car1, player_car2, game_info)

                    else:
                        game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selected_difficulty = show_main_menu(WIN)
                    game_info.reset()
                    player_car1.reset()
                    player_car2.reset()
                    TRACK, TRACK_BORDER, TRACK_BORDER_MASK, car1_pos, car2_pos, FINISH_POS = load_map(selected_difficulty)
                    images = [(TRACK, (0, 0)), (TRACK_BORDER, (0, 0))]
                    if selected_difficulty == "Easy":
                        images.append((FINISH, FINISH_POS))
                    player_car1 = Player_car1(4, 4, car1_pos)
                    player_car2 = Player_car2(4, 4, car2_pos)   
                    
        control_of_player1(player_car1)
        control_of_player2(player_car2)

        handle_collision(player_car1, player_car2, game_info)

if __name__ == "__main__":
    main()

pygame.quit()
