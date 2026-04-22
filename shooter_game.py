from pygame import *
from random import randint
from time import time as timer

display.set_caption("Shooter")
window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed                                                                                                                                                                     
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 600)
            self.rect.y = 0
            lost = lost + 1

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 600)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill

bullets = sprite.Group()
monsters = sprite.Group()

for i in range(2):
    monster = Enemy("ufo.png", randint(0, 500), 0, 60, 60, randint(1,3))
    monster2 = Enemy2("asteroid.png", randint(0, 500), 0, 60, 60, randint(2,4))
    monsters.add(monster)
    monsters.add(monster2)
        
mixer.init()
fire_sound = mixer.Sound("fire.ogg")

player = Player("rocket.png", 100, 450, 70, 50, 10)

finish = False
run = True

font.init()
font2 = font.SysFont('Arial', 36)
score = 0

font1 = font.SysFont('Arial', 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (255, 0, 0))

num_fire = 0
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 8 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_sound.play()
                if num_fire >= 8 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))

        text = font2.render("Счет:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))
        text2 = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text2, (10,50))

        player.update()
        monsters.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()

        if rel_time == True:
            now_timer = timer()
            if now_timer - last_time < 3:
                reload = font2.render("Wait, reloading!", 1, (255, 0, 0))
                window.blit(reload, (250, 300))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, 700), 0, 80, 50, randint(1,3))
            monster2 = Enemy2("asteroid.png", randint(80, 700), 0, 60, 60, randint(2,4))
            monsters.add(monster)
            monsters.add(monster2)

        if sprite.spritecollide(player, monsters, False) or lost >= 10:
            finish = True
            window.blit(lose, (135, 200))

        if score >= 20: 
        
            finish = True
            window.blit(win, (200, 200))

        display.update()

    else:
        finish = False
        lost = 0
        score = 0
        num_fire = 0
        for b in bullets:
            b.kill()

        for m in monsters:
            m.kill()
        time.delay(3000)

        for i in range(2):
            monster = Enemy("ufo.png", randint(80, 700), 0, 60, 60, randint(1,3))
            monster2 = Enemy2("asteroid.png", randint(0, 500), 0, 60, 60, randint(2,4))
            monsters.add(monster)
            monsters.add(monster2)

                


    time.delay(50)






























































































