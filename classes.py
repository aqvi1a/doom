from sett import *
import pygame
import math
import random as rd

SCORE = []
vertical_walls = pygame.sprite.Group()
horizontal_walls = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bulets = pygame.sprite.Group()
planets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.x, self.y = p_pos
        self.v = p_vis
        self.speed = 10
        self.original_image = pygame.image.load('assets/ship1.png')
        self.image = pygame.image.load('assets/ship1.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @property
    def pos(self):
        return self.rect.center

    def rotate(self, x, y):
        rel_x, rel_y = x - self.rect.x, y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        self.v = pygame.mouse.get_pos()
        ke = pygame.key.get_pressed()
        if ke[pygame.K_w]:
            self.rect.y -= self.speed
        if ke[pygame.K_a]:
            self.rect.x -= self.speed
        if ke[pygame.K_s]:
            self.rect.y += self.speed
        if ke[pygame.K_d]:
            self.rect.x += self.speed

    def update(self):
        if pygame.sprite.spritecollideany(self, planets, pygame.sprite.collide_circle_ratio(0.65)):
            q = (planets.sprites()[0].rect.left, planets.sprites()[0].rect.right, planets.sprites()[0].rect.top, planets.sprites()[0].rect.bottom)
            if q[0] < self.rect.centerx + 20 < q[1]:
                self.rect.centerx -= 20
            if q[0] < self.rect.centerx - 20 < q[1]:
                self.rect.centerx += 20
            if q[2] < self.rect.centery + 20 < q[3]:
                self.rect.centery -= 20
            if q[2] < self.rect.centery - 20 < q[3]:
                self.rect.centery += 20


        # walls
        if pygame.sprite.spritecollideany(self, horizontal_walls):
            if self.rect.bottom + 20 > HEIGHT:
                self.rect.bottom -= 20
            else:
                self.rect.top += 20
        if pygame.sprite.spritecollideany(self, vertical_walls):
            if self.rect.right + 20 > WIDTH:
                self.rect.right -= 20
            else:
                self.rect.left += 20


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mosx, mosy):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.add(bulets)
        self.image = pygame.image.load('assets/bullet.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mosx, self.mosy = mosx, mosy
        self.speed = b_speed
        self.angle = math.atan2(mosy-y, mosx-x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def move(self):
        self.rect.x = self.rect.x + int(self.x_vel)
        self.rect.y = self.rect.y + int(self.y_vel)

    def update(self):
        for hit in pygame.sprite.groupcollide(bulets, asteroids, True, True):
            Boom(pygame.image.load('assets/boom.png'), 10, 7, hit.rect.x - 40, hit.rect.y - 40)
            SCORE.append(hit)
            hit.kill()
        for _ in pygame.sprite.groupcollide(bulets, planets, True, False):
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_walls)
            self.image = pygame.Surface([1, y2 - y1], pygame.SRCALPHA)
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

        if y1 == y2:
            self.add(horizontal_walls)
            self.image = pygame.Surface([x2 - x1, 1], pygame.SRCALPHA)
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Planet(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.add(planets)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        ################
        if pygame.sprite.spritecollideany(self, asteroids):
            pass


class GameSpace:
    def __init__(self, num):
        self.stars = []
        self.colors = [(255, 255, 255), (192, 192, 192), (128, 128, 128), (255, 184, 69), (251, 121, 116),
                       (249, 118, 152), (163, 72, 166)]
        self.num = num
        for st in range(self.num):
            self.stars.append(Star(rd.choice(self.colors), [rd.randint(0, 900), rd.randint(0, 900)], rd.randint(1, 5)))

    def draw(self, display):
        for st in self.stars:
            st.draw(display)


class Star:
    def __init__(self, color, pos, radius):
        self.pos = pos
        self.radius = radius
        self.color = color

    def draw(self, display):
        pygame.draw.circle(display, self.color, self.pos, self.radius)


class Asteroids(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__(all_sprites)
        self.add(asteroids)
        self.x = x
        self.y = y
        i = rd.randint(0, 1)
        self.image = pygame.image.load(astr_images[i])
        self.spawn_angle = rd.randint(0, 360)
        self.t = target
        self.rect = None

    def move(self, display):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        ast_vector = pygame.Vector2(self.rect.center)
        planet_vector = pygame.Vector2(self.t.rect.center)
        try:
            towards = (planet_vector - ast_vector).normalize() * 2
            self.x += towards[0]
            self.y += towards[1]
        except Exception:
            pass


class Boom(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.cur_frame + 1 == len(self.frames):
            self.kill()
