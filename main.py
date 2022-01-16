import pygame.mixer

from classes import *
pygame.init()


def load_image(name):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


# def choose_planet():
#     background = pygame.transform.scale(load_image('assets/start_back.jpg'), (WIDTH, HEIGHT))
#     screen.blit(background, (0, 0))
#     names = ['assets/plim/earth.png', 'assets/plim/mars.png', 'assets/plim/arctic.png']
#     fir = 0
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 pygame.quit()
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
#                 planets = pygame.sprite.Group()
#                 if fir + 1 <= 2:
#                     fir += 1
#                     plan = Planet(load_image(names[fir]), 60, 4, 380, 400)
#                 else:
#                     fir = 0
#                     plan = Planet(load_image(names[fir]), 60, 4, 380, 400)
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#                 k = choose_planet()
#                 return k
#
#         planets.draw(screen)
#         planets.update()
#         pygame.display.flip()
#         clock.tick(FPS)


def start_screen():
    pygame.mixer.music.play()
    background = pygame.transform.scale(load_image('assets/start_back.jpg'), (WIDTH, HEIGHT))

    #---------------------MAIN MENU---------------------------------------------------#
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (27, 24, 32), [200, 200, 500, 370])
    text = l_font.render('MEGA KRUTOI DVISH', True, (255, 255, 255))
    s_text = s_font.render('Start: Enter', True, (255, 255, 255))
    h_text = s_font.render('How to play: Z', True, (255, 255, 255))
    e_text = s_font.render('Close: Esc', True, (255, 255, 255))
    scoretextrect = text.get_rect()
    scoretextrect.center = (120, 80)
    s_pos = s_text.get_rect()
    s_pos.center = (210, 250)
    h_pos = h_text.get_rect()
    h_pos.center = (210, 350)
    e_pos = e_text.get_rect()
    e_pos.center = (210, 450)
    screen.blit(text, scoretextrect.center)
    screen.blit(s_text, s_pos.center)
    screen.blit(h_text, h_pos.center)
    screen.blit(e_text, e_pos.center)
    #------------------------------------------------------------------------#

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        pygame.display.flip()
        clock.tick(FPS)


bullets = []
astr = []

if __name__ == '__main__':
    while True:
        game_lose = False
        while not game_lose:
            #-------------FONTS AND MUSIC/SOUND----------------------------#

            cursor = pygame.transform.scale(pygame.image.load('assets/crosshair.png'), (32, 32))
            l_font = pygame.font.Font('fon/menu.ttf', 40)
            s_font = pygame.font.Font('fon/menu.ttf', 30)
            pygame.mixer.music.load('Moonlancer Menu.mp3')

            #-----------------------------------------#

            pygame.mouse.set_visible(False)
            screen = pygame.display.set_mode(SIZE)
            clock = pygame.time.Clock()
            shoot_delay = 0
            ast_delay = 0
            space_map = GameSpace(70)
            player = Player()
            c = start_screen()
            planet = Planet(load_image(f'assets/plim/earth.png'), 60, 4, 380, 400)
            w1 = Wall(2, 2, 2, HEIGHT - 2)
            w2 = Wall(WIDTH - 2, 2, WIDTH - 2, HEIGHT - 2)
            w3 = Wall(2, 2, WIDTH - 2, 2)
            w4 = Wall(2, HEIGHT - 2, WIDTH - 2, HEIGHT - 2)

            while True:
                screen.fill((0, 0, 0))
                # space_map.draw(screen)
                rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850],
                       [rd.randrange(0, 800), 0]]
                background = pygame.transform.scale(load_image('assets/back.png'), (WIDTH, HEIGHT))
                screen.blit(background, (0, 0))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                screen.blit(cursor, (mouse_x, mouse_y))
                if shoot_delay < 20:
                    shoot_delay += 1
                if ast_delay < 40:
                    ast_delay += 1
                if ast_delay == 40:
                    choice = rd.choice(rand_spawns)
                    astr.append(Asteroids(choice[0], choice[1], planet))
                    ast_delay = 0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT) and shoot_delay == 20:
                        bullets.append(Bullet(player.rect.centerx, player.rect.centery, *pygame.mouse.get_pos()))
                        shoot_delay = 0
                player.move()
                player.rotate(*pygame.mouse.get_pos())
                for bul in bullets:
                    bul.move()
                for ast in astr:
                    ast.move(screen)

                all_sprites.draw(screen)
                all_sprites.update()
                pygame.display.flip()
                clock.tick(FPS)