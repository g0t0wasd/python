# AUTHOR : HARIHARAN 
# GITHUB : github.com/hariharan1412

import random , os
from time import sleep
import threading
from pynput import keyboard
import pyautogui as pt
from torch import rand 

class aliens:

    def __init__(self , i , j):
        
        self.i = i 
        self.j = j 
    
class missile:
    
    def __init__(self , i , j):
        
        self.i = i 
        self.j = j 
    

class starship:

    def __init__(self):

        self.board = []
        self.done = False
        self.letAlien = 5

        self.w = 20
        self.h = 15

        self.dot_bg = "."

        self.score = 0

        for i in range(self.w):
            row = []
            for j in range(self.h):
                row.append(self.dot_bg)
            self.board.append(row)
            
        self.ship = "@" 

        self.x , self.y = self.w-1 , self.h//2

        self.alien = []
        self.missile = []
        self.No_alien = random.randint(1 , 2)
        # os.system('cls')

    def display(self):

        while not self.done and not self.letAlien == 0:    

            
            print(" [ SPACE INVADER ] ")
            print("\n")
            x = random.randint(0 , 2)
            if x == 1:
                
                self.alien.append(aliens(0 , random.randint(0 , self.h-1)))

            for i in self.alien:
                self.board[i.i][i.j] = "$"

            self.missile.append(missile(self.w-1 , self.y))

            for i in self.missile:
                self.board[i.i][i.j] = "|"


            self.board[self.x][self.y] = self.ship
            
            for i in self.alien:
                if i.i == self.x and i.j == self.y:
                    print("[ LOST ] ")
                    self.done = True

            for i in range(self.w):
                for j in range(self.h):
                    print(self.board[i][j] , end=" ")
                print("")  
            
            print("\n\n")
            print(f" SCORE : {self.score} ")
            print(f" ALIEN ESCAPED : {5 - self.letAlien} ")


            for i in self.missile:
                self.board[i.i][i.j] = self.dot_bg
                i.i -= 1
                if i.i < 0:
                    self.missile.remove(i)

            for i in self.alien:
                self.board[i.i][i.j] = self.dot_bg
                i.i += 1
                if i.i == self.w:
                    self.letAlien -= 1
                    self.alien.remove(i)


            for i in self.alien:
                for j in self.missile:
                  
                    if i.i == j.i and i.j == j.j:
                        
                        self.score += 1
                        self.alien.remove(i)
                        self.missile.remove(j)

                        self.board[j.i][j.j] = self.dot_bg
                        self.board[i.i][i.j] = self.dot_bg

            sleep(0.5)
            os.system('cls')

        os.system('cls')
        print( "    [ GAME OVER : ]   ")
        print(f" TOTAL SCORE : {self.score}")

    def on_press(self , key):

        if key == keyboard.Key.esc:
            return False  
        try:
            k = key.char  
        except:
            k = key.name  

        if k == 'q':
            print("/nQuit/n")
            self.done = True
            self.listener.stop()
            pt.hotkey('ctrl' , 'x')

        if k == 'left':
            
            if self.y > 0:
                self.board[self.x][self.y] = self.dot_bg
                self.y -= 1

        if k == 'right':
            
            if self.y < self.h-1:
                self.board[self.x][self.y] = self.dot_bg
                self.y += 1
            

    def move(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  
        self.listener.join()  


def main():
    pass

if __name__ == "__main__":
    main()
    
    s = starship()

    t1 = threading.Thread(target=s.display)
    t1.start()
    
    t2 = threading.Thread(target=s.move)
    t2.start()
    