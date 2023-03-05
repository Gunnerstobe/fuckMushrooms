
import pygame
import os
import random


#start
pygame.init()
pygame.mixer.init()

#color
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0,128,0)


#size of screen
height = 800
width = 800
screen = pygame.display.set_mode((width, height))

#power cooldown
POWERUP_TIME = 7000

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder)


# load graphics
backround = pygame.image.load(os.path.join(img_folder, "screen.png")).convert()
backround_rect = backround.get_rect()
heart_img = pygame.image.load(os.path.join(img_folder, "heart.png")).convert()
font_name = pygame.font.match_font('arial')
pop_sound = []
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim["player"] = [] 
mushroom_images = []
mushroom_list = ['mushroom.png','mushroom2.png','mushroom1.png']
for img in mushroom_list:
     mushroom_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())
#set up expl
for i in range(9):
     filename = 'expl0{}.png'.format(i)
     img = pygame.image.load(os.path.join(img_folder, filename)).convert()
     img.set_colorkey(black)

     #size of big
     img_lg = pygame.transform.scale(img, (150, 150))
     explosion_anim['lg'].append(img_lg)

     #size of small
     img_sm = pygame.transform.scale(img, (90, 90))
     explosion_anim['sm'].append(img_sm)
     filename = 'Boom0{}.png'.format(i)

     img = pygame.image.load(os.path.join(img_folder, filename)).convert()
     img.set_colorkey(black)
     explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['coin']=  pygame.image.load(os.path.join(img_folder, "coin.png")).convert()
powerup_images['gun']=  pygame.image.load(os.path.join(img_folder, "light.png")).convert()
powerup_images['shield']=  pygame.image.load(os.path.join(img_folder, "shield.png")).convert()


#sound
for snd in ['pop.wav','pop2.wav']:
     pop_sound.append(pygame.mixer.Sound(os.path.join(img_folder, snd)))

pygame.mixer.music.load(os.path.join(img_folder, 'backroundsound.mp3'))
pygame.mixer.music.set_volume(3)

player_die_sound = pygame.mixer.Sound(os.path.join(img_folder, 'deathsound.mp3' ))
shoot_sound = pygame.mixer.Sound(os.path.join(img_folder, 'Lazer.wav' ))
power_sound = pygame.mixer.Sound(os.path.join(img_folder, 'powerup.wav' ))
#fps
clock = pygame.time.Clock()
fps = 60



#draw text
def draw_text(surf,text,size,x,y):
     font = pygame.font.Font(font_name, size)
     text_surface = font.render(text, True, black)
     text_rect = text_surface.get_rect()
     text_rect.midtop = (x ,y)
     surf.blit(text_surface, text_rect)


#display
pygame.display.set_caption('NO Mushrooms')
pygame.display.flip()


#expl sprite
class Explosion(pygame.sprite.Sprite):
     def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

     def update(self):
          now = pygame.time.get_ticks()
          if now - self.last_update > self.frame_rate:
               self.last_update = now
               self.frame += 1
               if self.frame == len(explosion_anim[self.size]):
                    self.kill()
               else:
                    center = self.rect.center
                    self.image = explosion_anim[self.size][self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center


#newmob
def newmob():
     m = mob()
     all_sprites.add(m)
     mobs.add(m)

#game over screen
def show_go_screen():
     screen.blit(backround, backround_rect)
     draw_text(screen, 'NO Mushrooms', 64, width /2, height/4)
     draw_text(screen, 'Q and D to move, Space to shoot', 22, width/2, height/2)
     draw_text(screen, 'Press any key to begin', 18, width/2, height/2 + 100)
     pygame.display.flip()
     waiting = True 
     while waiting:
          clock.tick(fps)
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    exit()
               if event.type == pygame.KEYUP:
                     waiting = False

def draw_shield(surf, x,y,pct):
     if pct<0:
          pct = 0
     BAR_LENGTH = 100
     BAR_HEIGHT = 10
     death = BAR_LENGTH
     fill = (pct/100)* BAR_LENGTH
     outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
     fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
     death_rect = pygame.Rect(x, y, death, BAR_HEIGHT)
     pygame.draw.rect(surf, red, death_rect )
     pygame.draw.rect(surf, green, fill_rect)
     pygame.draw.rect(surf, white, outline_rect, 2)


#draw life
def draw_lives(surf, x, y, lives, img):
     for i in range(lives):
           img = pygame.image.load(os.path.join(img_folder, "heart.png")).convert() 
           img.set_colorkey(black)
           img_rect = img.get_rect()
           img_rect.x = x + 30 * i
           img_rect.y = y 
           surf.blit(img, img_rect)


#bullets
class Bullets(pygame.sprite.Sprite):
     def __init__(Bullet, x, y, ):
          pygame.sprite.Sprite.__init__(Bullet)
          Bullet.image = pygame.image.load(os.path.join(img_folder, "middle.png")).convert()
          Bullet.image.set_colorkey(black)
          Bullet.rect = Bullet.image.get_rect()
          Bullet.rect.bottom = y
          Bullet.rect.centerx = x
          Bullet.speedy = -10
     def update(Bullet):
          Bullet.rect.y += Bullet.speedy 
          if Bullet.rect.bottom < 0:
               Bullet.kill()


class Pow(pygame.sprite.Sprite):
     def __init__(self, center):
          pygame.sprite.Sprite.__init__(self)
          self.type = random.choice(['coin', 'gun', 'shield'])
          self.image = powerup_images[self.type]
          self.image.set_colorkey(black)
          self.rect = self.image.get_rect()
          self.rect.center = center
          self.speedy = 3
     def update(self):
          self.rect.y += self.speedy 
          if self.rect.top > height:
               self.kill()

#defin mob
class mob(pygame.sprite.Sprite):
     def __init__(mush):
          pygame.sprite.Sprite.__init__(mush)
          mush.image = random.choice(mushroom_images)
          mush.image.set_colorkey(black)
          mush.rect = mush.image.get_rect()
          mush.radius = int(mush.rect.width / 2)
          #pygame.draw.circle(mush.image, red, mush.rect.center, mush.radius )
          
          #spawn of screen
          mush.rect.x = random.randrange(width - mush.rect.width)
          mush.rect.y = random.randrange(-100, -40)

          #speed of mush
          mush.speedy = random.randrange(1, 8)

          #mush move angle 
          mush.speedx = random.randrange(-10, 10)

     def update(mush):

          #if hits side
          mush.rect.x += mush.speedx
          if mush.rect.right > width : 
               mush.rect.right = width
               mush.speedx = random.randrange(-5, 5)
               mush.speedy = random.randrange(3, 4)
          if mush.rect.left < 0 :
               mush.rect.left = 0
               mush.speedx = random.randrange(1, 4)
               mush.speedy = random.randrange(2, 4)

          #if hit bottom
          mush.rect.y += mush.speedy
          if mush.rect.bottom > height :
            mush.rect.x = random.randrange(width - mush.rect.width)
            mush.rect.y = random.randrange(-100, -40)
            mush.speedy = mush.speedy + 2


class bottom(pygame.sprite.Sprite):
     def __init__(bot):
          pygame.sprite.Sprite.__init__(bot)
          bot.image = pygame.Surface((800, 2))
          bot.image.fill(red)
          bot.image.set_colorkey(red)
          bot.rect = bot.image.get_rect()
          bot.rect.topright = (800, 798)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "My_face.png")).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 48
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius )
        self.rect.center = (width/2 , 740)
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    
    def update(self):
         #timeout for power
         if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
              self.power -= 1
         if self.power >=3 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
              self.power -= 1
              self.power_time = pygame.time.get_ticks()
         if self.hidden and pygame.time.get_ticks() - self.hide_timer > 3000:
              self.hidden = False
              self.rect.center = (width/2 , 740)

          #keys    
         self.speedx = 0
         self.speedy = 0
         keystate = pygame.key.get_pressed()
         if keystate[pygame.K_q]:
              self.speedx = -8 
         if keystate[pygame.K_d]:
              self.speedx = 8
         if keystate[pygame.K_SPACE] and not self.hidden:
              self.shoot()
         self.rect.x += self.speedx
         self.rect.y += self.speedy

        #boarders
         if self.rect.left < 0 :
              self.rect.left = 0
         if self.rect.right > width : 
              self.rect.right = width 

    def powerup(self):
         self.power += 1
         self.power_time = pygame.time.get_ticks()

     #shoot from player  
    def shoot(self):
         now = pygame.time.get_ticks()
         if now - self.last_shot > self.shoot_delay:
              self.last_shot = now
              #power3
              if self.power >= 3:
               bullet1 = Bullets(self.rect.left, self.rect.centery)
               bullet2 = Bullets(self.rect.right, self.rect.centery)
               bullet3 = Bullets(self.rect.centerx, self.rect.centery)
               all_sprites.add(bullet1)
               all_sprites.add(bullet2)
               all_sprites.add(bullet3)
               bullets.add(bullet1)
               bullets.add(bullet2)
               bullets.add(bullet3)
               shoot_sound.play()

               #power2
              if self.power >= 2:
               bullet1 = Bullets(self.rect.left, self.rect.centery)
               bullet2 = Bullets(self.rect.right, self.rect.centery)
               all_sprites.add(bullet1)
               all_sprites.add(bullet2)
               bullets.add(bullet1)
               bullets.add(bullet2)
               shoot_sound.play()

               #power1
              if self.power == 1:
               bullet = Bullets(self.rect.centerx, self.rect.top)
               all_sprites.add(bullet)
               bullets.add(bullet)
               shoot_sound.play()

     #def hide
    def hide(self):
     self.hidden = True
     self.hide_timer = pygame.time.get_ticks()
     self.rect.center = (width/2, 1000)



#backround music 
pygame.mixer.music.play(loops=-1)


#game loop
game_over = True
run = True
while run:
    
    if game_over:
         show_go_screen()
         game_over = False
         #images
         mobs = pygame.sprite.Group()
         all_sprites = pygame.sprite.Group()
         bullets = pygame.sprite.Group()
         player = Player()
         bottoms = bottom()
         coins = pygame.sprite.Group()
         all_sprites.add(player, bottoms,)
         powerups = pygame.sprite.Group()
         for i in range(8):
               newmob()
         score = 0
    for events in pygame.event.get():
         if events.type == pygame.QUIT:
              run = False

    clock.tick(fps)
	#time between press
    pygame.time.delay(10)  
   
    all_sprites.update()
#check for collistion

     #when shot hit mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True )
    for hit in hits :
          random.choice(pop_sound).play()
          expl = Explosion(hit.rect.center, 'lg')
          all_sprites.add(expl)
          #score += 77- hit.radius
          score += 1
          #powerups
          if random.random() > 0.9:
               pow = Pow(hit.rect.center)
               all_sprites.add(pow)
               powerups.add(pow)
          newmob()

     #when mob hits bottom
    hits = pygame.sprite.spritecollide(bottoms, mobs, False)
    for hit in hits: 
         #score -= 77 - hit.radius 
         score -= 3

    #when hits player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
         player.shield -= 25
         expl = Explosion(hit.rect.center, 'sm')
         all_sprites.add(expl)
         newmob()
         if player.shield <=0:
          player_die_sound.play() 
          death_explosion = Explosion(player.rect.center, 'player')
          all_sprites.add(death_explosion)
          player.hide()
          player.lives -= 1
          player.shield =100


    #player hits power up 
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
         if hit.type == 'gun':
              player.powerup()
              power_sound.play()
         if hit.type == 'shield':
              player.shield += random.randrange(10, 30)
              if player.shield >=100:
                   player.shield = 100
                   power_sound.play()
         if hit.type == 'coin':
              score += 10
              power_sound.play()
          

#when play death/expl over
    if player.lives == 0 and not death_explosion.alive():
          game_over = True
     

    #draw
    screen.fill(white)
    screen.blit(backround, backround_rect)
    all_sprites.draw(screen)
    draw_text (screen, str(score), 30, width/ 2, 10)
    draw_shield(screen, 1, 1, player.shield)
    draw_lives(screen, 1, 16, player.lives, heart_img)

    #update
    pygame.display.flip()
    

#closes the pygame window 
pygame.display.update()
pygame.quit()