import pygame
import random
import os
WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
score = 0
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid")
clock = pygame.time.Clock()
# set up asset folders


img_dir = os.path.join(os.path.dirname(__file__), 'img')
 # Load all game graphics
background = pygame.image.load(os.path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir, "ship.png")).convert()
asteroid_img = pygame.image.load(os.path.join(img_dir, "Asteroid.png")).convert_alpha()
lazer_img = pygame.image.load(os.path.join(img_dir, "lazershoot.png")).convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(player_img,(40,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.limit = None

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.speed_x += x
        self.speed_y += y

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.speed_x
#loop the position x
        if self.rect.left>WIDTH :
            self.rect.right=0
        elif self.rect.right<0 :
            self.rect.left=480

        # Move up/down
        self.rect.y += self.speed_y
 
        # Check and see if we hit anything            
        block_hit_list = pygame.sprite.spritecollide(self, self.limit, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)




class Astro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(asteroid_img,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
#    def update(self) :
#        self.rect.x += self.speed_x
#        self.rect.y += self.speed_y
#
        #check if collide with player
        #block_hit_list = pygame.sprite.spritecollide(self, self.limit, False)
        #for block in block_hit_list:
         
        #    pygame.quit()



class Limit(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(lazer_img,(10,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()



all_sprites = pygame.sprite.Group()

limit_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
astro = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(4):
    m = Astro()
    all_sprites.add(m)
    enemy_list.add(m)

    Astro.add(m)
#top limit
limit = Limit(0, 0, 480, 0)
limit_list.add(limit)
all_sprites.add(limit)

#bottom limit
limit = Limit(0, 600, 480, 0)
limit_list.add(limit)
all_sprites.add(limit)

player = pygame.sprite.Group()

player = Player()
player.limit = limit_list
all_sprites.add(player)

#1st enemy
#enemy = Enemy()
#enemy_list.add(enemy)
#enemy.limit = limit_list
#all_sprites.add(enemy)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-5, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(5, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -5)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 5)


 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(5, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-5, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 5)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -5)

        elif event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:        
            if event.key == pygame.K_SPACE : 
                player.shoot()
    # Update
    all_sprites.update()


    # check to see if a bullet hit a mob
    taps = pygame.sprite.groupcollide(enemy_list, bullets, True, True)
    for tap in taps:
        m = Astro()
        all_sprites.add(m)
        Astro.add(m)

    hit = pygame.sprite.spritecollide(player, enemy_list, False, pygame.sprite.collide_circle) 
    if hit :
        pygame.quit()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
