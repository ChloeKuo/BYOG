import pygame
from pygame import *
import random
import sys
import math
import os

WIN_WIDTH = 800
WIN_HEIGHT = 800
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
PURPLE = (186, 85, 211)
GRAY = (100, 100, 100)
GREEN = "#259d60"

BLOCK_HEIGHT = 32
ITEM_HEIGHT = BLOCK_HEIGHT * 5

fps = 80



OBSTACLE_WIDTH = WIN_WIDTH/8
MIN_O_HEIGHT = WIN_HEIGHT/10

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.intro = self.menu = self.play = self.outro = True
        self.back_image = pygame.image.load("images/background.jpg")
        self.back_image = pygame.transform.scale(self.back_image, (DISPLAY))
        self.back_rect = self.back_image.get_rect()
        self.intro_back = pygame.image.load("images/introback.jpg")
        self.intro_back = pygame.transform.scale(self.intro_back, (WIN_WIDTH, WIN_HEIGHT))
        self.intro_rect = self.intro_back.get_rect()
        self.title = Text(150, ":)", WIN_WIDTH / 2, WIN_HEIGHT / 2, WHITE)
        self.subtitle = Text(50, "-- Click Here --", WIN_WIDTH / 2, self.title.rect.bottom + self.title.rect.height, WHITE)
        self.endsub = Text(50, "-- Click to Play Again --", WIN_WIDTH / 2, WIN_HEIGHT * 4/5, WHITE)
        self.instructions = Text(WIN_WIDTH/15, "Click to choose your character", WIN_WIDTH / 2, WIN_HEIGHT / 5, WHITE)
        self.clock = pygame.time.Clock()
        self.mode = 0
        self.exit_count = 0

        self.score = Text(50, "Score: 0", WIN_WIDTH / 2, BLOCK_HEIGHT * 2, BLACK)
        self.menu_back = pygame.image.load("images/dots.jpg")
        self.menu_back = pygame.transform.scale(self.menu_back, (WIN_WIDTH, WIN_HEIGHT))
        self.menu_rect = self.menu_back.get_rect()

        self.end_back = pygame.image.load("images/endback.jpg")
        self.end_back = pygame.transform.scale(self.end_back, (WIN_WIDTH, WIN_HEIGHT))
        self.end_rect = self.end_back.get_rect()

    def blink(self, text):
        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(text.image, text.rect)

    def update(self, player_score):
        font = pygame.font.SysFont("Britannic Bold", 50)
        self.score.image = font.render("Score: " + str(player_score), 1, BLACK)

    def set_mode(self, mode):
        self.type = mode
        if self.type == "penguin":
            self.back_image = pygame.image.load("images/background.jpg")
            self.back_image = pygame.transform.scale(self.back_image, (DISPLAY))

        elif self.type == "pusheen":
            self.back_image = pygame.image.load("images/push_back.jpg")
            self.back_image = pygame.transform.scale(self.back_image, (DISPLAY))


class Mode(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if self.type == "penguin":
            self.image = pygame.image.load("images/penguin/rest.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (ITEM_HEIGHT, ITEM_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect = self.rect = Rect(WIN_WIDTH/4, WIN_HEIGHT/2, ITEM_HEIGHT, ITEM_HEIGHT)
        elif self.type == "pusheen":
            self.image = pygame.image.load("images/pusheen/rest.tiff").convert_alpha()
            self.image = pygame.transform.scale(self.image, (ITEM_HEIGHT, ITEM_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect = Rect(WIN_WIDTH * 2/3, WIN_HEIGHT/2.05, ITEM_HEIGHT, ITEM_HEIGHT)



class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.height = random.randrange(MIN_O_HEIGHT, WIN_HEIGHT/2 - 2 * BLOCK_HEIGHT)
        self.mode = 0
        self.type = type
        if self.type == "b":
            self.image = pygame.image.load("images/bottompipe.png").convert_alpha()
        if self.type == "t":
            self.image = pygame.image.load("images/toppipe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, self.height))
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, OBSTACLE_WIDTH, self.height)
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed

    # def set_mode(self):
    #



class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, mode):
        pygame.sprite.Sprite.__init__(self)
        self.mode = mode
        if self.mode == "penguin":
            self.image = pygame.image.load("images/sushi.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_HEIGHT, BLOCK_HEIGHT)) #sldrghsdlfkghsdlkgdf;lgjl;gj;lj;lj;ljl;kl;kln
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed



class Player(Entity):
    def __init__(self, x, y, loop_count, food_group):
        Entity.__init__(self)
        self.init_x = x
        self.init_y = y
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load("images/penguin/rest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_HEIGHT, BLOCK_HEIGHT))
        self.pic_format = ""
        self.rect = self.image.get_rect()
        self.rect = Rect(self.init_x, self.init_y, BLOCK_HEIGHT, BLOCK_HEIGHT)
        self.lives = 1
        self.loop_count = loop_count
        self.score = 0
        self.food_group = food_group
        self.height = 0

    def update(self, up, running, platforms, obstacle_group):
        if self.lives > 0:
            if up:
                self.jump()
                # only jump if on the ground
                if self.onGround: self.yvel -= 5

            else:
                self.rest()

            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += 0.3
                # max falling speed
                if self.yvel > 100: self.yvel = 100
                if up:
                    self.yvel -= 1


        else:
            self.yvel += 0.2

        for p in obstacle_group:
            if pygame.sprite.collide_rect(self, p):
                self.lives = 0
                self.explode()

            self.eat()


        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.yvel, 0, platforms)

        # increment in y direction
        self.rect.top += self.yvel

        # assuming we're in the air
        self.onGround = False;

        # do y-axis collisions
        self.collide(0, self.yvel, platforms)


    def eat(self):
        collisions = pygame.sprite.spritecollide(self, self.food_group, True)
        for p in collisions:
            self.score += 1

    def explode(self):
        x = self.rect.x
        y = self.rect.y
        self.image = pygame.image.load("images/explosion.png")
        self.image = pygame.transform.scale(self.image, (BLOCK_HEIGHT * 5, BLOCK_HEIGHT * 5))
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, BLOCK_HEIGHT, BLOCK_HEIGHT)


    def collide(self, xvel, yvel, platforms):
        if self.lives > 0:
            for p in platforms:
                if pygame.sprite.collide_rect(self, p):
                    if isinstance(p, ExitBlock):
                        pygame.event.post(pygame.event.Event(QUIT))
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        print "collide right"
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        print "collide left"
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom

    def jump(self):
        self.image = pygame.image.load("images/" + self.type + "/jump." + self.pic_format).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.height, self.height))


    def rest(self):
        self.image = pygame.image.load("images/" + self.type + "/rest." + self.pic_format).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.height, self.height))

    def set_mode(self, mode):
        self.type = mode
        if self.type == "penguin":
            self.height = BLOCK_HEIGHT
            self.image = pygame.image.load("images/penguin/rest.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.height, self.height))
            self.rect = self.image.get_rect()
            self.rect = Rect(self.init_x, self.init_y, self.height, self.height)
            self.pic_format = "png"
        elif self.type == "pusheen":
            self.height = BLOCK_HEIGHT * 2
            self.image = pygame.image.load("images/pusheen/rest.tiff").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.height, self.height))
            self.rect = self.image.get_rect()
            self.rect = Rect(self.init_x, self.init_y, self.height, self.height)
            self.pic_format = "tiff"

    def reset(self, x, y):
        self.init_x = x
        self.init_y = y
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load("images/penguin/rest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_HEIGHT, BLOCK_HEIGHT))
        self.pic_format = ""
        self.rect = self.image.get_rect()
        self.rect = Rect(self.init_x, self.init_y, BLOCK_HEIGHT, BLOCK_HEIGHT)
        self.lives = 1
        self.score = 0
        self.height = 0


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((BLOCK_HEIGHT, BLOCK_HEIGHT))
        self.image.convert()
        self.image.fill(Color(GREEN))
        self.rect = Rect(x, y, BLOCK_HEIGHT, BLOCK_HEIGHT)


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))


class Text:
    def __init__(self, size, text, x, y, color):
        font = pygame.font.SysFont("Britannic Bold", size)
        self.image = font.render(str(text), 1, color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x - self.rect.width/2, y - self.rect.height/2)


def main():
    pygame.init()
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()
    run = Game()
    up = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(WHITE)
    entities = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    mode_group = pygame.sprite.Group()
    loop_count = 0
    player = Player(BLOCK_HEIGHT, BLOCK_HEIGHT, loop_count, food_group)
    mode1 = Mode("penguin")
    mode2 = Mode("pusheen")
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPP",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "                         ",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",]

    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32

    entities.add(player)
    mode_group.add(mode1, mode2)

    while 1:
        loop_count = 0
        player.reset(BLOCK_HEIGHT, BLOCK_HEIGHT)
        run.exit_count = 0
        for p in obstacle_group:
            p.kill()
        for x in food_group:
            x.kill()
        while run.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    pygame.time.wait(1500)
                    run.intro = False
                    run.menu = True

            run.screen.blit(run.intro_back, run.intro_rect)

            run.screen.blit(run.title.image, run.title.rect)

            run.blink(run.subtitle)

            run.clock.tick(fps)

            pygame.display.update()

        while run.menu:
            # Get mouse position
            mpos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for p in mode_group:
                        if p.rect.collidepoint(mpos):
                            run.set_mode(p.type)
                            player.set_mode(p.type)
                            run.menu = False
                            run.play = True
                else:
                    pass

            run.screen.blit(run.menu_back, run.menu_rect)

            run.blink(run.instructions)

            mode_group.draw(run.screen)

            run.clock.tick(fps)

            pygame.display.update()

        while run.play:
            timer.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit, "ESCAPE"

                if e.type == QUIT: raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit, "ESCAPE"
                if e.type == KEYDOWN and e.key == K_SPACE:
                    up = True

                if e.type == KEYUP and e.key == K_SPACE:
                    up = False

            # draw background
            for y in range(32):
                for x in range(32):
                    run.screen.blit(bg, (x * 32, y * 32))

            run.screen.blit(run.back_image, run.back_rect)
            obstacle_group.draw(run.screen)
            food_group.draw(run.screen)

            if loop_count % 120 == 0:
                top = Obstacle(WIN_WIDTH, WIN_HEIGHT, "t")
                top.rect.y = BLOCK_HEIGHT/4.5
                obstacle_group.add(top)
                bottom = Obstacle(WIN_WIDTH, 0, "b")
                bottom.rect.y = WIN_HEIGHT - BLOCK_HEIGHT/4.5 - bottom.rect.height
                obstacle_group.add(bottom)
                middle = (top.rect.y + bottom.rect.y + top.rect.height)/2
                food = Food(top.rect.centerx, middle, "penguin")
                food_group.add(food)


            run.update(player.score)
            obstacle_group.update()
            food_group.update()
            # update player, draw everything else
            player.update(up, running, platforms, obstacle_group)
            for e in entities:
                run.screen.blit(e.image, e.rect)

            run.screen.blit(run.score.image, run.score.rect)

            loop_count += 1

            if player.lives < 1:
                run.exit_count += 1
            if run.exit_count >= fps * 2:
                run.play = False
                run.outro = True


            run.clock.tick(fps)

            pygame.display.update()


        while run.outro:
            timer.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    pygame.time.wait(1500)
                    run.outro = False
                    run.intro = True

            run.screen.blit(run.end_back, run.end_rect)
            run.blink(run.endsub)

            run.clock.tick(fps)

            pygame.display.update()




if __name__ == "__main__":
    main()