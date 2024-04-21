from pygame import *
from random import randint
from time import time as timer


font.init()

window = display.set_mode((700, 500))
display.set_caption('shooter')
background = transform.scale(image.load("kpsmos.jpg"), (700, 500))

clock = time.Clock()
FPS = 60
app = True
finish = False
real_time = True
num_fire = 0

y1 = 0
y2 = -500


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, width, height):
        super().__init__()
        self.direction = 'left'
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
            key_pressed = key.get_pressed()
            if key_pressed[K_a] and self.rect.x >5:
                self.rect.x -= self.speed

            if  key_pressed[K_d] and self.rect.x < 595:
                self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('pulya.png', 10, self.rect.x, self.rect.y, 50, 50)
        bullets.add(bullet)

        
kills = 0
lost = 0

font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
font3 = font.Font(None, 36)
font4 = font.Font(None, 36)
font5 = font.Font(None, 36)


class Enemy(GameSprite):
    def update(self):
        if self.rect.y >= 500:
            global lost
            lost += 1
        
            self.rect.y = -50
        self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        


rocket = Player('rocket.png', 10, 200, 380, 65, 65)

ufos = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('asteroid.png', randint(1,3), randint(0,500), -100, 65, 65)
    monsters.add(monster)

for i in range(5):
    ufo = Enemy('ufo.png', randint(1,3), randint(0,500), -100, 65, 65)
    ufos.add(ufo)

start = 0
num_Fire = 0 
real_time = False

while app:
    for e in event.get():
        if e.type == QUIT:
            app = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_Fire <= 5 and real_time == False:
                    rocket.fire()
                    num_fire+=1
                if num_fire >= 5 and real_time == False:
                    real_time=True
                    start = timer()
        

    if finish != True:       
        window.blit(background, (0,y1))
        window.blit(background, (0,y2))

        collides = sprite.groupcollide(bullets, monsters, True, True)
        collides = sprite.groupcollide(bullets, ufos, True, True)
        for i in collides:
            monster = Enemy('asteroid.png', randint(1,3), randint(0,500), -100, 65, 65)
            monsters.add(monster)
            kills += 1

        for i in collides:
            ufo = Enemy('ufo.png', randint(1,3), randint(0,500), -100, 65, 65)
            ufos.add(ufo)
            kills += 1

        text_youlose = font4.render(
            'ВЫ ПРОИГРАЛИ!', True,(255,0,0)
        )

        text_win = font3.render(
            'ВЫ ВЫИГРАЛИ!', True,(0,255,0)
        )

        text_kills = font2.render(
            "Убийства " + str(kills), True, (255,255,255)
        )
        text_lose = font1.render(
            'Пропущено: ' + str(lost), True, (255,255,255)
           
        )
        reloading = font5.render(
            'Wait . . . Reloading . . .', True, (255,255,255)
        )
        if lost >= 10:
            window.blit(text_youlose, (40,40))
        if kills >= 10:
            window.blit(text_win, (40,40))
    
        window.blit(text_lose, (10,10))
        window.blit(text_kills, (10, 35))
        y1 += 5
        y2 += 5
        if y1 >= 500:
            y1 = -500
        if y2 >= 500:
            y2 = -500

        if real_time == True:
            end = timer()
            if end - start >= 3:
                num_fire = 0
                real_time = False
            else:
                window.blit(reloading, (10,60))

        bullets.draw(window)
        bullets.update()
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        ufos.draw(window)
        ufos.update()
        clock.tick(FPS)
        display.update()

#gsfueorhcfwaleihmnwv4uifhp4rihfa;lekrhgw24gtbq2e4
