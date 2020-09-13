import math
import random
import pyxel

border = {
            'sizex'  : 160,
            'sizey'  : 160,
            'left'   : 49,
            'right'  : 209,
            'top'    : 59,
            'bottom' : 219,
            }

class Atr:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Blaster:
    def __init__(self,posx,posy,vecx,vecy):
        
        self.vecx = vecx
        self.vecy = vecy
        self.posx = posx
        self.posy = posy
        
        self.position = Atr(self.posx, self.posy)

    def update(self):
        self.position.x += self.vecx
        self.position.y += self.vecy
        

class Package:      
    def __init__(self):
        self.which_power=random.randint(0, 9) 

        self.sizexy = 10
        self.position = Atr (
            random.randrange(border['left']+self.sizexy, border['right']-self.sizexy),
            random.randrange(border['top']+self.sizexy, border['bottom']-self.sizexy)
            )


class Ball:
    def __init__(self):

        def draw():
            return random.randrange(-self.ball_speed, self.ball_speed, 2)
        
        self.which_ball = random.randint(1, 3)

        if self.which_ball == 1 or self.which_ball == 2:
            self.ball_speed = 6
            self.radius = 2
            self.color = 8
        else:
            self.ball_speed = 3
            self.radius = 4
            self.color = 2

        self.position = Atr(
            random.randrange(border['left']+self.radius, border['right']-self.radius,self.radius),
            random.randrange(border['top']+self.radius, border['bottom']-self.radius,self.radius)
            )

        while True:
            self.vx = draw()
            self.vy = draw()
            if self.vx or self.vy: break
            
        self.vec_speed = Atr(self.vx, self.vy)

    def update(self):
        self.position.x += self.vec_speed.x
        self.position.y += self.vec_speed.y

        #bouncing the walls 
        if self.vec_speed.x < 0 and self.position.x <= border['left'] + self.radius:
            self.vec_speed.x *= -1

        if self.vec_speed.x > 0 and self.position.x >= border['right'] - self.radius:
            self.vec_speed.x *= -1

        if self.vec_speed.y < 0 and self.position.y <= border['top'] + self.radius:
            self.vec_speed.y *= -1

        if self.vec_speed.y > 0 and self.position.y >= border['bottom'] - self.radius:
            self.vec_speed.y *= -1


class App:
    def __init__(self):
        pyxel.init(256, 256, caption="Dodge Master", fps=20)
        pyxel.load('assets.pyxres')

        #map size & properties for the player
        self.border = {
            'sizex'  : 160,
            'sizey'  : 160,
            'left'   : 42,
            'right'  : 204,
            'top'    : 54,
            'bottom' : 216,
            }
        
        #game state
        self.score = 0
        self.is_gameover = False
        self.is_hit = False
        self.timer = 0

        #player
        self.posx = random.randrange(self.border['left'], self.border['right'], 6)
        self.posy = random.randrange(self.border['top'], self.border['bottom'], 6)
        self.player_speed = 6

        #balls
        self.balls = []
        self.how_many = 0

        #packages
        self.packages = []
        self.new_package_timer = 100

        #special things
        self.double_points = 0
        self.dp_timer = 0
        self.shield = 1
        self.freeze = 0
        self.fr_timer = 0
        self.blaster = 1
        self.blasters = []

        pyxel.run(self.update, self.draw)

    def update(self):
        '''   1. Input
              2. Index
              3. Logic    '''
        
        def add_ball(divider):
            if self.timer%divider == 0 or self.timer == 50:
                new_ball = Ball()
                self.how_many += 1
                self.balls.append(new_ball)

        def shoot_blaster():
            pyxel.play(1,1)
            bl = Blaster(self.posx, self.posy, 0, 10)
            self.blasters.append(bl)
            bl = Blaster(self.posx, self.posy, 0, -10)
            self.blasters.append(bl)
            bl = Blaster(self.posx, self.posy, 10, 0)
            self.blasters.append(bl)
            bl = Blaster(self.posx, self.posy, -10, 0)
            self.blasters.append(bl)
            self.blaster -= 1
        
        ############ - 1 - ###########
        
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_UP):
            self.posy -= self.player_speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.posy += self.player_speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.posx -= self.player_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.posx += self.player_speed
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.blaster != 0: shoot_blaster()
        
        ############ - 2 - ############

        if not self.is_gameover: 
        
            #extra score increase 
            if self.double_points: self.score += 1
            
            # -- 3 -- #

            #timer increase
            self.timer += 1
            
            #score increase
            self.score += 1
            
            #new ball
            if self.how_many <= 3: add_ball(100)
            elif self.how_many <= 6: add_ball(300)
            elif self.how_many <= 9: add_ball(600)
            elif self.how_many <= 12: add_ball(1000)
            elif self.how_many <= 15: add_ball(1500)
            elif self.how_many < 20: add_ball(2000)
            else: pass
                
            #new package and first 
            if self.timer == self.new_package_timer or self.timer == 200:
                new_package = Package()
                self.packages.append(new_package)
                self.new_package_timer = 0
                self.new_package_timer = self.timer + random.randint(150,350)
                
            #balls update
            if self.freeze: pass
            else:
                for x in range(0, self.how_many):
                    b = self.balls[x]
                    b.update()

            #blasters update
            if len(self.blasters):
                how_many_blasters = len(self.blasters)
                for x in range(0, how_many_blasters):
                    bl = self.blasters[x]
                    bl.update()
            
            ############ - 3 - #########

            #border player
            if self.posx <= self.border['left']: self.posx += self.player_speed
            if self.posx >= self.border['right']: self.posx -= self.player_speed
            if self.posy <= self.border['top']: self.posy += self.player_speed
            if self.posy >= self.border['bottom']: self.posy -= self.player_speed
            
            #packages check
            if len(self.packages):
                how_many_p = len(self.packages)
                for x in range(0,how_many_p):
                    p = self.packages[x]
                    
                    #checks if player collected the package
                    if (
                        math.fabs(p.position.x - self.posx) <= 6
                        and math.fabs(p.position.y - self.posy) <= 6
                    ):
                        pyxel.play(1,2)
                        if p.which_power == 9:
                            self.blaster += 1
                        elif p.which_power > 5:
                            self.double_points += 149
                            self.dp_timer = 5
                        elif p.which_power > 2:
                            if self.shield < 5: self.shield += 1
                        else:
                            self.freeze += 89
                            self.fr_timer = 3                      
                                    
                        del self.packages[x]
                        break;
                            
                    #checks if ball destroyed the package
                    for y in range(0,self.how_many):
                        b = self.balls[y]
                        if (
                            math.fabs(p.position.x - b.position.x) <= 5 + b.radius
                            and math.fabs(p.position.y - b.position.y) <= 5 + b.radius
                        ):
                            pyxel.play(1,3)
                            del self.packages[x]
                            break;

            #blasters check
            if len(self.blasters):
                how_many_blasters = len(self.blasters)
                for x in range(0, how_many_blasters):
                    bl = self.blasters[x]

                #check if blaster hit the wall
                    if bl.position.x >= self.border['right'] or bl.position.x <= self.border['left']:
                        del self.blasters[x]
                        break
                    if bl.position.y >= self.border['bottom'] or bl.position.y <= self.border['top']:
                        del self.blasters[x]
                        break

                    #check if blaster hit the ball
                    for y in range(0, self.how_many):
                        b = self.balls[y]
                        if (
                            math.fabs(bl.position.x - b.position.x) <= 5 + b.radius
                            and math.fabs(bl.position.y - b.position.y) <= 5 + b.radius
                        ):
                            pyxel.play(1,1)
                            del self.balls[y]
                            self.how_many -= 1
                            del self.blasters[x]
                            break
                        
                    if how_many_blasters != len(self.blasters): break

            #check if player is hited
            for x in range(0, self.how_many):
                b = self.balls[x]
                if (
                    math.fabs(self.posx - b.position.x) <= 5 + b.radius
                    and math.fabs(self.posy - b.position.y) <= 5 + b.radius
                ):
                    self.is_hit = True 
                    del self.balls[x]
                    self.how_many -= 1
                    break
                
            
            #special timers
            if self.double_points:
                if self.double_points % 30 == 0: self.dp_timer -= 1
                self.double_points -= 1

            if self.freeze:
                if self.freeze % 30 == 0: self.fr_timer -= 1
                self.freeze -= 1
            
            #checks damage to the player
            if self.is_hit:
                if self.shield:
                    pyxel.play(1,3)
                    self.shield -= 1
                    self.is_hit = False
                else:
                    pyxel.play(1, 0)
                    self.is_gameover = True

    def draw(self):
        pyxel.cls(0)
        
        #borders
        if self.freeze: pyxel.rectb(48, 60, 160, 160, 6)
        else: pyxel.rectb(48, 60, 160, 160, 7)    
        
        #score
        pyxel.text(25,20, "YOUR SCORE :", 7)
        if self.double_points: pyxel.text(80, 20, str(self.score),10)
        else: pyxel.text(80, 20, str(self.score), 8)

        #info text
        pyxel.text(35, 235, "Try to dodge the", 7)
        pyxel.text(103, 235, "balls", 8)
        pyxel.text(127, 235, "and collect", 7)
        pyxel.text(175, 235, "superpowers ", 14)

        #player
        pyxel.rect(self.posx, self.posy, 10, 10, 7)

        #superpower
        pyxel.text(150,20, "SUPERPOWER :",7)

        #double points
        if self.double_points:
            pyxel.text(200, 12, "POINTS x2", 10)
            pyxel.rect(240, 10, 10, 10, 10)
            pyxel.text(243, 13, str(self.dp_timer), 0)

        #freeze
        if self.freeze:
            pyxel.text(200, 27, "FREEZE", 6)
            pyxel.rect(234, 24, 10, 10, 6)
            pyxel.text(237, 27, str(self.fr_timer), 0)
            
        #shield
        if self.shield:
            pyxel.text(200, 20, "SHIELD", 3)
            if self.shield >= 1: pyxel.rectb(self.posx, self.posy, 10, 10, 3)
            if self.shield >= 2: pyxel.rectb(self.posx+2, self.posy+2, 6, 6, 3)
            if self.shield >= 3: pyxel.rect(self.posx+4, self.posy+4, 2, 2, 3)  
            if self.shield >= 4: pyxel.rect(self.posx+3, self.posy+3, 4, 4, 3)  
            if self.shield >= 5:
                pyxel.rect(self.posx+1, self.posy+1, 8, 8, 3)
                pyxel.text(50, 51,'MAX SHIELD LEVEL', 3)

        #blaster
        if self.blaster:
            pyxel.text(200, 36, "BLASTER", 14)
            pyxel.rect(234, 35, 10, 10, 14)
            pyxel.text(237, 38, str(self.blaster), 0)
            pyxel.text(122, 51, 'PRESS SPACE TO BLAST !', 14)

        #blasters
        for blaster in self.blasters:
            pyxel.rect(blaster.position.x, blaster.position.y, 10, 10, 14)

        #packages
        for package in self.packages:
            pyxel.rect(package.position.x, package.position.y, package.sizexy, package.sizexy, 14)
            pyxel.text(package.position.x + 4, package.position.y + 3, "S", 0)
              
        #balls
        for ball in self.balls:
            pyxel.circ(ball.position.x, ball.position.y, ball.radius, ball.color)
            
        #GAMEOVER
        if self.is_gameover:
            pyxel.cls(0)
            pyxel.rectb(60, 60, 136, 136, 8)
            pyxel.text(105, 80, " GAME OVER ", 8)
            pyxel.tri(80, 120, 80, 126, 86, 123, 8)
            pyxel.tri(80, 140, 80, 146, 86, 143, 7)
            pyxel.tri(80, 160, 80, 166, 86, 163, 10)
            pyxel.text(106, 120, "YOUR SCORE : ", 8)
            pyxel.text(160, 120, str(self.score), 8)
            pyxel.text(106, 140, "Press Q to Quit ", 7)
            pyxel.text(106, 160, "Pls give me star", 10)
            pyxel.text(106, 170, "on Github ", 10)
        


                          
App()
    

