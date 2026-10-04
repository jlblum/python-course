import os
import random

# How big should the grid be?
GRIDHEIGHT = 7
GRIDWIDTH = 7
STARTPOS = (3,3)
EXITLIST = [(0,0),(0,6),(6,0),(6,6)]
global playerPos

gameBoard = {}

for x in range(GRIDWIDTH):
    for y in range(GRIDHEIGHT):
        gameBoard[(x,y)] = "Empty Space"

def randomizeExit(exitList):
    global exit
    exit = random.choice(exitList)
    #print("The exit is located at :" + str(exit))
    # input()

def placeHazard(height,width):
    hazardYesNo = [True,False]
    for y in range(height):

        for x in range(width):
            if (random.choice(hazardYesNo) == True) and (gameBoard[(x,y)] != "X"):
                gameBoard[(x,y)] = "HAZARD"
                break;
def printBoard(height,width):
    os.system('cls' if os.name =='nt' else 'clear') 
    print("Mini Dungeon Quest")
    print("Can you escape the Dungeon?")
    for y in range(height):
        #outer loop
        rowChars = ""
        for x in range(width):
            if playerPos == (x,y):
                rowChars += "# "
            elif exit == (x,y):
                rowChars += "X "
           # Un-comment the two lines below to expose the hazards     
           # elif gameBoard[(x,y)] == "HAZARD":
           #      rowChars += "! "
            else:     
                rowChars += ". "
        print(rowChars)



def main():
    global playerPos
    playerPos = STARTPOS
    randomizeExit(EXITLIST)
    placeHazard(GRIDHEIGHT,GRIDWIDTH)
    printBoard(GRIDHEIGHT,GRIDWIDTH)

    while True:
            
            printBoard(GRIDHEIGHT,GRIDWIDTH)
            player_x = playerPos[0]
            player_y = playerPos[1]
            # Get player input
            move = input("Use W (up), A (left), S (down), D (right) to move. Press Q to quit.\nMove: ").lower().strip()
        
            if move == 'q':
                print("Goodbye!")
                break
            
            if move == 'w' and player_y > 0:           # Move Up
                player_y -= 1
                playerPos = (player_x,player_y)
            elif move == 's' and player_y < GRIDHEIGHT - 1: # Move Down
                player_y += 1
                playerPos = (player_x,player_y)
            elif move == 'a' and player_x > 0:           # Move Left
                player_x -= 1
                playerPos = (player_x,player_y)
            elif move == 'd' and player_x < GRIDWIDTH - 1:  # Move Right
                player_x += 1
                playerPos = (player_x,player_y)

            if gameBoard[(player_x,player_y)] == "HAZARD":
                print("You have died. Your quest is over.")
                break;

            if playerPos == exit:
                print("You have reached the exit! Your quest is over!")
                break;





if __name__ == "__main__":
    main()