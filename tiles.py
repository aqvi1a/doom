import pygame
import math

pygame.init()
win = pygame.display.set_mode((500, 500))  # Окно игры

pygame.display.set_caption("Test game")  # Заголовок

# Переменные сверху
x = 50
y = 425
widht = 40
heigth = 60
speed = 5
isJump = False
jumpCount = 10

# Основной цикл
run = True
while run:
    pygame.time.delay(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Условие закрытия игры
            run = False

        # Уравление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
    if keys[pygame.K_RIGHT] and x < 500 - widht - 5:
        x += speed
    if not isJump:
        if keys[pygame.K_UP] and y > 5:
            y -= speed
        if keys[pygame.K_DOWN] and y < 500 - heigth - 15:
            y += speed
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount <= 0:
                y += (jumpCount ** 2) / 2
                jumpCount -= 1
            else:
                y -= (jumpCount ** 2) / 2
                jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    win.fill((0, 0, 0))

    pygame.draw.rect(win, (0, 0, 255), (x, y, widht, heigth))
    pygame.display.update()


    # Вроде похоже на функцию следования за мышью
    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.position)

pygame.quit()