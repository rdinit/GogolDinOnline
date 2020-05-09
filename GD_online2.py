import pygame
from random import randint as rnd
from easygui import enterbox, msgbox
import ogp


class Dino(pygame.sprite.Sprite):
    def sozdat(self):
        # создаем динозаврика и задаем начальные значения переменых
        self.y = 300
        self.x = 100
        self.kstep = 0
        
        self.image = pygame.image.load('dinodata/dino/1_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 300
        self.vs = 0
        self.sogn = False

        self.imgs_run = ['dinodata/dino/1_1.png', 'dinodata/dino/1_2.png', 'dinodata/dino/1_3.png']
        self.imgs_sog = ['dinodata/dino/2_1.png', 'dinodata/dino/2_2.png']
        
        self.cost_norm = 0
        self.cost_sog = 0
        
    def step(self, spd):
        # вызывается на каждый цикл
        self.kstep += 1
        self.y += self.vs
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
        self.vs += 1
        if self.rect.y >= 300 and self.vs != 0:
            if self.sogn:
                self.vs = 0
                self.y = 340
            else:
                self.vs = 0
                self.y = 300
        if self.y >= 300:
            if self.sogn:
                if self.kstep > 25 / spd:  # проверкаа на надобность делания шага
                    self.cost_sog += 1
                    self.cost_sog %= 2
                    self.kstep = 0
                    self.image = pygame.image.load(self.imgs_sog[self.cost_sog]).convert_alpha()
                    self.rect = self.image.get_rect()
                    self.y = 340
                self.rect.y = self.y
                self.rect.x = self.x
            else:
                if self.kstep > 25 / spd:
                    self.cost_norm += 1
                    self.cost_norm %= 3
                    self.kstep = 0
                    self.image = pygame.image.load(self.imgs_run[self.cost_norm]).convert_alpha()
                    self.rect = self.image.get_rect()
                self.rect.y = self.y
                self.rect.x = self.x
        
    def jump(self):
        # прыжок
        if self.vs == 0 and self.rect.y > 290:
            self.vs = -20
            self.image = pygame.image.load('dinodata/dino/1_1.png').convert_alpha()
            self.rect = self.image.get_rect()

    def prigib(self):
        # пригибание
        if self.vs != 0:
            self.vs += 2.5
        self.sogn = True

        
class Cactus(pygame.sprite.Sprite):
    def sozdat(self):
        self.tip = rnd(1, 4)
        self.image = pygame.image.load(f'dinodata/cactus/{self.tip}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 1500
        self.rect.y = 300

    def step(self, spd):
        self.rect.x -= int(spd)
        return self.rect.x < -100


class Ground(pygame.sprite.Sprite):
    def sozdat(self):
        tip = rnd(1, 1)
        self.image = pygame.image.load(f'dinodata/fon/fon_{tip}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 1300
        self.rect.y = 350
        self.zam = False

    def step(self, spd):
        self.rect.x -= int(spd)
        n = 0
        if self.rect.x < 100 and not self.zam:
            # правый конец земли подьезжает к концу экрана значит надо создать следующую
            n = 1
            self.zam = True
        if self.rect.x < -2000:
            # землч уже уехада за экран и ее можно удалять
            n = 2
        return n


class FlyingDino(pygame.sprite.Sprite):
    def sozdat(self):
        self.tip = rnd(2, 2)
        self.image = pygame.image.load(f'dinodata/pterod/base.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 1500
        y_p = [160, 250, 300]
        self.rect.y = y_p[self.tip]

    def step(self, spd):
        self.rect.x -= int(spd + 4)
        return self.rect.x < -100


def start_game():
    pygame.init()
    size = 1200, 500
    screen = pygame.display.set_mode(size)
    die = True
    running = True
    clock = pygame.time.Clock()

    hscore_file = open('dinodata/hiscore.txt', 'r')
    hiscore = int(hscore_file.read())
    hscore_file.close()
    
    k_pr = 0
    ssid = enterbox('введите номер Вашей сессии', 'введите число')
    while running:
        if die:  # перезапуск
            msgbox('You died!\nRESTART', 'restart')
            prepyat = []
            grnd = []
            all_sprites = pygame.sprite.Group()
            prep = pygame.sprite.Group()
            gnds = pygame.sprite.Group()

            speed = 10
            score = 0
            die = False
            
            dino = Dino()
            dino.sozdat()
            all_sprites.add(dino)

            g = Ground()
            g.sozdat()
            grnd.append(g)
            gnds.add(g)
            
            prep_timer = 0  # нужен чтобы соблюдать интервалы между препятствиями
            
        if rnd(1, 10) == 1 and prep_timer > 35:
            # создание препятсвий
            if rnd(1, 4) == 1:
                d = FlyingDino()
                d.sozdat()
                prepyat.append(d)
                prep.add(d)
            else:
                c = Cactus()
                c.sozdat()
                prepyat.append(c)
                prep.add(c)
            prep_timer = 0
            
        for event in pygame.event.get():
            ev = event.type
            if ev == pygame.QUIT:
                running = False
            elif ev == 2:
                if event.key == 32 or event.key == 273:
                    dino.jump()
            elif ev == 3:
                if event.key == 274:
                    dino.sogn = False
                # проверяем события
        if k_pr % 3 == 0:    
            keys = ogp.get_events(ssid)
            for i in keys:
                if i == 'K_UP':
                    dino.jump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            # пригибание
            dino.prigib()
            
        dino.step(speed)
        for i in prepyat:
            # вызываем для каждого препятствия
            if i.step(speed):
                i.kill()
                
        for i in grnd:
            # вызываем для каждого учатска земли
            n = i.step(speed)
            if n == 1:
                g = Ground()
                g.sozdat()
                grnd.append(g)
                gnds.add(g)
            elif n == 2:
                i.kill()
                
        if pygame.sprite.spritecollide(dino, prep, False):
            # пересечение с препятсвиями
            die = True
            if score > hiscore:
                hiscore = score
        t = clock.tick(60)
        
        screen.fill((255, 255, 255))
        score += 1
        
        speed += 0.006
        prep_timer += 0.5  # таймер препятствий
        
        all_sprites.draw(screen)
        prep.draw(screen)
        gnds.draw(screen)
        
        score_font = pygame.font.Font(None, 50)
        
        score_font_surf = score_font.render('SCORE: ' + str(score), 1, (0, 0, 0))
        screen.blit(score_font_surf, (10, 10))  # отображаем очки
        
        hiscore_font = pygame.font.Font(None, 50)
        hiscore_font_surf = hiscore_font.render('HISCORE: ' + str(hiscore), 1, (0, 0, 0))
        screen.blit(hiscore_font_surf, (600, 10))
        
        pygame.display.flip()
        
        k_pr += 1
    if score > hiscore:
        hiscore = score
        
    hscore_file = open('dinodata/hiscore.txt', 'w')  # сохранение хискоре
    hscore_file.write(str(hiscore))
    hscore_file.close()
    pygame.quit()
    return True


if __name__ == '__main__':
    start_game()
