#!/usr/bin/python3

import os, platform
if platform.system() == "Linux" or platform.system() == "Darwin":
    os.environ["KIVY_VIDEO"] = "ffpyplayer"
    
from pysimbotlib.core import PySimbotApp, Robot
from kivy.config import Config
from kivy.logger import Logger
# Force the program to show user's log only for "info" level or more. The info log will be disabled.
Config.set('kivy', 'log_level', 'info')

from random import seed

# Fixed Seed
seed(1)

class FuzzyRobot(Robot):

    def __init__(self):
        super(FuzzyRobot, self).__init__()
        # self.pos = START_POINT
        self.close = 3
        self.near = 12
        self.far = 20
        
        # for front sensor
        self.fr_near = 12
        self.fr_far = 30
        

    def update(self):
        ''' Update method which will be called each frame
        '''        
        self.ir_values = self.distance()
        self.target = self.smell()

        # initial list of rules
        rules = list()
        turns = list()
        moves = list()
        
        # 1. Goal: Aim the target
        # rule 0
        rules.append(self.front_far(self.fr_near,self.fr_far) * self.left_far(self.near,self.far) * self.right_far(self.near,self.far))
        turns.append(0)
        moves.append(5)
        
        # rule 1
        rules.append(self.smell_left() * self.front_far() * self.left_far() * self.right_far())
        turns.append(-45)
        moves.append(0)

        # rule 2
        rules.append(self.smell_right() * self.front_far() * self.left_far() * self.right_far())
        turns.append(90)
        moves.append(0)

        
        # 2. Goal: Avoid the obstacles(wall)
        # IF (FRONT FAR ADD (LEFT NEAR OR RIGHT NEAR))
        # THEN GO FORWARD
        rules.append(self.front_far(self.fr_near,self.fr_far) * max( self.left_near(self.near,self.far) , self.right_near(self.near,self.far)))
        turns.append(0)
        moves.append(5)
        
        # IF (FR NEAR, LEFT FAR , RIGHT FAR)
        rules.append(self.front_near(self.fr_near,self.fr_far) * self.left_far(self.near,self.far) * self.right_far(self.near,self.far))
        turns.append(80)
        moves.append(0)

        # rule 2
        # IF (FR FAR, LEFT NEAR , RIGHT FAR)
        # THEN TURN CLOCKWISE (100)
        rules.append(self.front_far(self.fr_near,self.fr_far) * self.left_near(self.near,self.far) * self.right_far(self.near,self.far))
        turns.append(100)
        moves.append(0)
        
        # IF (FR FAR, LEFT NEAR , RIGHT FAR)
        # THEN TURN CLOCKWISE (100)
        rules.append(self.front_far(self.fr_near,self.fr_far) * self.left_far(self.near,self.far) * self.right_near(self.near,self.far))
        turns.append(-45)
        moves.append(0)

        rules.append(self.front_near(self.fr_near,self.fr_far) * self.left_near(self.near,self.far) * self.right_near(self.near,self.far))
        turns.append(90)
        moves.append(0)
        
        
        # IF (FRONTLEFT NEAR OR FRONTRIGHT NEAR) THEN TURN(90)
        rules.append(max( self.frontleft_near(self.near,self.far), self.frontright_near(self.fr_near,self.fr_far) ) )
        turns.append(90)
        moves.append(0)
        
        rules.append(self.front_close(self.near,self.far) )
        turns.append(120)
        moves.append(0)
        
        
        
        ans_turn = 0.0
        ans_move = 0.0
        i = 0
        for r, t, m in zip(rules, turns, moves):
            if r > 0:
                Logger.info(f"Rules {i} is Effect, Values: {r}")
            ans_turn += t * r
            ans_move += m * r
            i += 1
        Logger.info(f"Move Values: {ans_move}")
        Logger.info(f"Turn Values: {ans_move}")
        self.turn(ans_turn)
        self.move(ans_move)
        Logger.info(f"After Moved: Dist Sensor: {self.ir_values}")
        
    def front_close(self,first_value,second_value):
        irfront = self.ir_values[0]
        if irfront <= first_value:
            return 0.0
        elif irfront >= second_value:
            return 1.0
        else:
            return (irfront-first_value) / abs(first_value-second_value)
        
    def front_far(self,first_value=10,second_value = 40):
        irfront = self.ir_values[0]
        if irfront <= first_value:
            return 0.0
        elif irfront >= second_value:
            return 1.0
        else:
            return (irfront-first_value) / abs(first_value-second_value)
    
    def front_near(self,first_value=10,second_value = 40):
        return 1 - self.front_far(first_value, second_value)


    def frontright_far(self, first_value= 10, second_value=10):
        irfrontright = self.ir_values[1]
        if irfrontright <= first_value:
            return 0.0
        elif irfrontright >= second_value:
            return 1.0
        else:
            return (irfrontright - first_value) / abs(first_value-second_value)
    
    def frontright_near(self,first_value=10,second_value = 40):
        return 1 - self.frontright_far(first_value, second_value)
    
    def frontleft_far(self, first_value= 10, second_value=10):
        irfrontleft = self.ir_values[7]
        if irfrontleft <= first_value:
            return 0.0
        elif irfrontleft >= second_value:
            return 1.0
        else:
            return (irfrontleft-first_value) / abs(first_value-second_value)
    
    def frontleft_near(self,first_value=10,second_value = 40):
        return 1 - self.frontleft_far(first_value, second_value)

    def left_far(self,first_value=10,second_value = 40):
        irleft = self.ir_values[6]
        if irleft <= first_value:
            return 0.0
        elif irleft >= second_value: 
            return 1.0
        else:
            return (irleft-first_value) / abs(first_value-second_value)
    
    def left_near(self,first_value=10,second_value = 40):
        return 1 - self.left_far(first_value, second_value)

    def right_far(self,first_value=10,second_value = 40):
        irright = self.ir_values[2]
        if irright <= first_value:
            return 0.0
        elif irright >= second_value:
            return 1.0
        else:
            return (irright-first_value) / abs(first_value-second_value)

    def right_near(self,first_value=10,second_value = 40):
        return 1 - self.right_far(first_value, second_value)
    
    def smell_right(self):
        target = self.smell()
        if target >= 90:
            return 1.0
        elif target <= 0:
            return 0.0
        else:
            return target / 90.0

    def smell_center(self):
        target = abs(self.smell())
        if target >= 45:
            return 1.0
        elif target <= 0:
            return 0.0
        else:
            return target / 45.0

    def smell_left(self):
        target = self.smell()
        if target <= -90:
            return 1.0
        elif target >= 0:
            return 0.0
        else:
            return -target / 90.0

if __name__ == '__main__':
    app = PySimbotApp(
        robot_cls=FuzzyRobot,
        max_tick=5000,
        interval=1.0/60.0)
    app.run()