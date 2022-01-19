import pygame.mixer
import time
from progi.classes import *
from progi.sett import *

pygame.init()

#-------------FONTS AND MUSIC/SOUND----------------------------#

cursor = pygame.transform.scale(pygame.image.load('assets/crosshair.png'), (32, 32))
l_font = pygame.font.Font('assets/fon/menu.ttf', 40)
s_font = pygame.font.Font('assets/fon/menu.ttf', 30)
ss_font = pygame.font.Font('assets/fon/menu.ttf', 24)
very_small_font = pygame.font.Font('assets/fon/menu.ttf', 10)
laser = pygame.mixer.Sound('assets/sounds/laser.wav')
jet = pygame.mixer.Sound('assets/sounds/jetsoun.wav')
boom_s = pygame.mixer.Sound('assets/sounds/boom.wav')
die = pygame.mixer.Sound('assets/sounds/start-level.wav')
laser.set_volume(0.1)
jet.set_volume(0.01)
boom_s.set_volume(0.1)
die.set_volume(0.1)
#-----------------------------------------#


def load_image(name):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


def high():
    i = 0
    with open('score.txt', mode='r+', encoding='utf-8') as f:
        k = f.readline()
    screen.fill((0, 0, 0))
    sc = s_font.render(F'HIGHEST SCORE: {k}', True, (255, 255, 255))
    s = sc.get_rect()
    s.center = WIDTH // 2 - 300, HEIGHT // 2 - 70
    screen.blit(sc, s.center)
    while i != 100:
        i += 1
        pygame.display.flip()
        clock.tick(FPS)

def dies():
    screen.fill((0,0,0))
    text = l_font.render('GAME OVER', True, (255, 255, 255))
    sc = s_font.render(F'SCORE: {get_score()}', True, (255, 255, 255))
    t, s = text.get_rect(), sc.get_rect()
    t.center = WIDTH // 2 - 190, HEIGHT // 2 - 70
    s.center = t.centerx, t.centery + 100
    screen.blit(text, t.center)
    screen.blit(sc, s.center)
    with open('score.txt', mode='r+', encoding='utf-8') as f:
        k = f.readline()
        c = get_score()
        if int(k) < c:
            f.seek(0)
            f.write(str(c))
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        pygame.display.flip()
        clock.tick(FPS)


def rules():
    # ---------------------RULES---------------------------------------------------#
    background = pygame.transform.scale(load_image('assets/start_back.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (27, 24, 32), [200, 200, 500, 370])
    s_text = s_font.render('WASD: move', True, (255, 255, 255))
    h_text = s_font.render('LKM: shoot', True, (255, 255, 255))
    e_text = s_font.render('ESC: restart', True, (255, 255, 255))
    s_pos, h_pos, e_pos = s_text.get_rect(), h_text.get_rect(), e_text.get_rect()
    s_pos.center = (210, 250)
    h_pos.center = (210, 350)
    e_pos.center = (210, 450)
    screen.blit(s_text, s_pos.center)
    screen.blit(h_text, h_pos.center)
    screen.blit(e_text, e_pos.center)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        pygame.display.flip()
        clock.tick(FPS)
    # ------------------------------------------------------------------------#


def choose_planet():
    background = pygame.transform.scale(load_image('assets/start_back.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    text = l_font.render('CHOOSE THE PLANET', True, (255, 255, 255))
    scoretextrect = text.get_rect()
    scoretextrect.center = (120, 80)
    screen.blit(text, scoretextrect.center)
    names = ['assets/plim/earth.png', 'assets/plim/mars.png', 'assets/plim/arctic.png']
    ar_r = pygame.image.load('assets/arrow.png')
    ar_l = pygame.transform.rotate(pygame.image.load('assets/arrow.png'), 180)
    fir = 0
    running = True
    Planet(load_image(names[fir]), 60, 4, 380, 400)
    while running:
        screen.blit(text, scoretextrect.center)
        screen.blit(ar_r, (520, 430))
        screen.blit(ar_l, (315, 430))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if fir + 1 <= 2:
                    fir += 1
                else:
                    fir = 0
                Planet(load_image(names[fir]), 60, 4, 380, 400)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                screen.blit(background, (0, 0))
                if fir - 1 < 0:
                    fir = 2
                else:
                    fir -= 1
                Planet(load_image(names[fir]), 60, 4, 380, 400)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                k = names[fir]
                return k
        planets.draw(screen)
        planets.update()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    pygame.mixer.music.play(-1, 0.0)
    background = pygame.transform.scale(load_image('assets/start_back.jpg'), (WIDTH, HEIGHT))

    #---------------------MAIN MENU---------------------------------------------------#
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (27, 24, 32), [200, 200, 500, 370])
    text = l_font.render('ASTRONOMICON', True, (255, 255, 255))
    s_text = s_font.render('Start: Enter', True, (255, 255, 255))
    h_text = s_font.render('How to play: Z', True, (255, 255, 255))
    e_text = s_font.render('Close: Esc', True, (255, 255, 255))
    scoretextrect = text.get_rect()
    scoretextrect.center = (210, 80)
    s_pos, h_pos, e_pos = s_text.get_rect(), h_text.get_rect(), e_text.get_rect()
    s_pos.center = (210, 250)
    h_pos.center = (210, 350)
    e_pos.center = (210, 450)
    #------------------------------------------------------------------------#

    running = True
    while running:
        pygame.draw.rect(screen, (27, 24, 32), [200, 200, 500, 370])
        screen.blit(text, scoretextrect.center)
        screen.blit(s_text, s_pos.center)
        screen.blit(h_text, h_pos.center)
        screen.blit(e_text, e_pos.center)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return choose_planet()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                rules()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    while True:
        game_lose = True
        bullets, astr, dif = [], [], [30, 25]
        st_dif = 40
        pygame.mixer.music.load('assets/sounds/Moonlancer Menu.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mouse.set_visible(False)
        screen = pygame.display.set_mode(SIZE)
        clock = pygame.time.Clock()
        shoot_delay = 0
        ast_delay = 0
        space_map = GameSpace(70)
        player = Player()
        c = start_screen()
        planet = Planet(load_image(f'{c}'), 60, 4, 380, 400)
        w1 = Wall(2, 2, 2, HEIGHT - 2)
        w2 = Wall(WIDTH - 2, 2, WIDTH - 2, HEIGHT - 2)
        w3 = Wall(2, 2, WIDTH - 2, 2)
        w4 = Wall(2, HEIGHT - 2, WIDTH - 2, HEIGHT - 2)
        high()
        pygame.mixer.music.load('assets/sounds/GamePlay.mp3')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0)
        while game_lose:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # space_map.draw(screen)
            rand_spawns = [[0, rd.randrange(0, 800)], [850, rd.randrange(0, 800)], [rd.randrange(0, 800), 850],
                   [rd.randrange(0, 800), 0]]
            background = pygame.transform.scale(load_image('assets/back.png'), (WIDTH, HEIGHT))
            screen.blit(background, (0, 0))
            if shoot_delay < 20:
                shoot_delay += 1
            if get_score() > 5000:
                st_dif = dif[0]
            if get_score() > 10000:
                st_dif = dif[1]
            if ast_delay < st_dif:
                ast_delay += 1
            if ast_delay == st_dif:
                choice = rd.choice(rand_spawns)
                astr.append(Asteroids(choice[0], choice[1], planet))
                ast_delay = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT) and shoot_delay == 20:
                    pygame.mixer.stop()
                    laser.play()
                    bullets.append(Bullet(player.rect.centerx, player.rect.centery, *pygame.mouse.get_pos()))
                    shoot_delay = 0
            player.move(jet)
            player.rotate(*pygame.mouse.get_pos())
            for bul in bullets:
                bul.move()
            for ast in astr:
                ast.move(screen)
            if pygame.sprite.spritecollideany(planet, asteroids, pygame.sprite.collide_circle_ratio(0.65)):
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                die.play()
                dies()
                clear()
                game_lose = False

            if game_lose:
                all_sprites.draw(screen)
                all_sprites.update()
                screen.blit(cursor, (mouse_x, mouse_y))
                scor, pos = score(ss_font)
                screen.blit(scor, pos)
                pygame.display.flip()
                clock.tick(FPS)