### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from Utils import *
from random import *
import time
from datetime import datetime

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 900
var = Variables()



### ====================================================================================================
### YOUR OWN FUNCTIONS HERE
### ====================================================================================================
def initVars():
    # init variables
    var.nbOK         = 0
    var.nbFAIL       = 0
    var.totalTime    = 0
    var.lastQuestionTime = 0
    var.maxQuestions = 40

    var.currentWord  = ""
    var.number1      = 0
    var.number2      = 0

    var.stars        = []

    var.userName     = ""
    var.allUsers     = ["EMELINE","NATHAN","ROMU","MIMI"]
    var.idxUser      = -1

    var.exoType      = ""
    var.allExos      = ["LECTURE","ADDITION","MULTIPLICATION"]
    var.idxExo       = -1

    var.emitters     = []

    var.background   = createSprite("classroom.png", (SCREEN_WIDTH, SCREEN_HEIGHT), True)
    var.background.center_x = SCREEN_WIDTH/2
    var.background.center_y = SCREEN_HEIGHT/2

    var.saveOK       = False
    var.hasStarted   = False
    # create stars
    for i in range(var.maxQuestions):
        s = createSprite("starGray.png", (27, 27), True)
        s.center_x = 11+10
        s.center_y = 11+10 + i*22
        var.stars.append(s)
    # fill word list
    fp = open("words2.txt", "r", encoding='utf-8')
    lines = fp.readlines()
    var.words = [x.replace("\n", "") for x in lines]
    fp.close()

def chooseUser(key,isPressed):
    if key == arcade.key.UP and isPressed:
        var.idxUser = max(var.idxUser-1,0)
    if key == arcade.key.DOWN and isPressed:
        var.idxUser = min(var.idxUser + 1, len(var.allUsers)-1)
    var.userName = var.allUsers[var.idxUser]

def chooseExo(key,isPressed):
    if key == arcade.key.LEFT and isPressed:
        var.idxExo = max(var.idxExo-1,0)
    if key == arcade.key.RIGHT and isPressed:
        var.idxExo = min(var.idxExo+ 1, len(var.allExos)-1)
    var.exoType = var.allExos[var.idxExo]

def resetExercice():
    var.currentWord = ""
    var.number1     = 0
    var.number2     = 0
    var.lastQuestionTime = var.totalTime

def isFinished():
    return (var.nbOK+var.nbFAIL >= var.maxQuestions)

def chooseWord():
    idx = randint(0, len(var.words) - 1)
    var.currentWord = var.words[idx]

def chooseNumbers(a,b):
    var.number1 = randint(1, a)
    var.number2 = randint(1, b)

def getRandomQuestion():
    if var.exoType == "LECTURE":
        if var.currentWord == "":
            chooseWord()
    if var.exoType == "ADDITION":
        if var.number1 == 0 and var.number2 == 0:
            chooseNumbers(9,19)
    if var.exoType == "MULTIPLICATION":
        if var.number1 == 0 and var.number2 == 0:
            chooseNumbers(9,9)

def startExo(key,isPressed):
    if key == arcade.key.ENTER and isPressed and var.exoType != "" and var.userName != "":
        var.hasStarted = True
        var.totalTime  = 0

def updateScore(status):
    if status:
        idx = var.nbOK
        old = var.stars[idx]
        var.nbOK += 1
        spritePath = "starYellow.png"
    else:
        var.nbFAIL += 1
        idx = -var.nbFAIL
        old = var.stars[idx]
        spritePath = "starRed.png"
    # Create star sprite
    new = createSprite(spritePath, (36, 36), True)
    # set the new coloured star position
    new.center_x = old.center_x
    new.center_y = old.center_y
    # replace star
    var.stars[idx] = new
    # create new emitter and add it
    em = createParticleBurst(old.center_x, old.center_y, 0.005, 0.25, 100, 0.5, 4.0, arcade.color.WHITE, 100,0, spritePath)
    var.emitters.append(em)

def processInGame(deltaTime):
    # increase total time
    var.totalTime += deltaTime
    #choose new word/computation if not existing
    getRandomQuestion()
    # check if the current question is not too long (20sec max)
    if var.totalTime - var.lastQuestionTime >= 20:
        resetExercice()
        updateScore(False)

def processResults():
    if var.saveOK == False:
        # datetime object containing current date and time
        now = str(datetime.now())
        now = now.replace("-", "")
        now = now.replace(" ", "")
        now = now.replace(":", "")
        now = now.split(".")[0]
        # compile score
        score = str(int(100 * var.nbOK / var.maxQuestions))
        # compile time
        tim = str(round(var.totalTime, 1))
        # create save file
        fp = open("save_records.txt","a")
        fp.write(now+","+var.userName+","+var.exoType+","+score+","+tim+"\n")
        var.saveOK = True



### ====================================================================================================
### INITIALISATION OF YOUR VARIABLES
### ====================================================================================================
def setup():
    initVars()



### ====================================================================================================
### UPDATE OF YOUR GAME DATA
### ====================================================================================================
def update(deltaTime):
    # update ingame/results process
    if not isFinished():
        processInGame(deltaTime)
    else:
        processResults()
    # update emitters (anytime)
    for v in var.emitters:
        v.update()
        # check if emitters are finished
        if v.can_reap():
            var.emitters.remove(v)



### ====================================================================================================
### DRAW YOUR IMAGES ON THE SCREEN
### ====================================================================================================
def draw():

    # draw BG
    var.background.draw()

    if not var.hasStarted:
        # draw user menu
        refX = SCREEN_WIDTH-50
        refY = SCREEN_HEIGHT-50
        arcade.draw_text("Appuie sur HAUT/BAS pour choisir l'utilisateur", refX, refY, arcade.color.WHITE, 30,anchor_x="right", anchor_y="center", bold=True)
        for i in range(len(var.allUsers)):
            u = var.allUsers[i]
            size = 20
            if var.idxUser == i:
                size = 50
            arcade.draw_text(u, refX, refY-5 -(i+1)*42, arcade.color.GREEN_YELLOW, size, anchor_x="right", anchor_y="center", bold=True)
        # Draw start menu
        refX = SCREEN_WIDTH/2
        refY = SCREEN_HEIGHT/2
        arcade.draw_text("Appuie sur ENTREE/START pour démarrer", refX, refY, arcade.color.WHITE, 30,anchor_x="center", anchor_y="center", bold=True)
        # Draw EXO menu
        refX = 50
        refY = 50
        arcade.draw_text("Appuie sur GAUCHE/DROITE pour choisir l'exercice", refX, refY, arcade.color.WHITE, 30,anchor_x="left", anchor_y="center", bold=True)
        for i in range(len(var.allExos)):
            e = var.allExos[i]
            size = 20
            if var.idxExo == i:
                size = 50
            arcade.draw_text(e, refX, refY +(len(var.allExos)-i)*42, arcade.color.GREEN_YELLOW, size, anchor_x="left", anchor_y="center", bold=True)

    if var.hasStarted:
        # draw username
        arcade.draw_text(var.userName, SCREEN_WIDTH/2+110, SCREEN_HEIGHT - 65, arcade.color.GREEN_YELLOW, 60, anchor_x="center", anchor_y="center", bold=True)

        # draw timer
        arcade.draw_text( str(round(var.totalTime,1)), SCREEN_WIDTH/2+126, SCREEN_HEIGHT - 145, arcade.color.GREEN_YELLOW, 20,anchor_x="right", anchor_y="center", bold=True)

        # draw stars
        for s in var.stars:
            s.draw()

        # IN GAME
        if not isFinished():
            refX = SCREEN_WIDTH/2+110
            refY = SCREEN_HEIGHT/2+120
            if var.exoType == "LECTURE":
                # draw current word
                wrd = var.currentWord.title()
                if wrd != "":
                    arcade.draw_text( wrd, refX, refY, arcade.color.WHITE, 100, anchor_x="center", anchor_y="center", bold=True)
            if var.exoType == "ADDITION":
                if var.number1 != 0 and var.number2 != 0:
                    formula = str(var.number1)+ " + "+str(var.number2)
                    arcade.draw_text(formula, refX, refY, arcade.color.WHITE, 140, anchor_x="center", anchor_y="center", bold=True)
            if var.exoType == "MULTIPLICATION":
                if var.number1 != 0 and var.number2 != 0:
                    formula = str(var.number1) + " x " + str(var.number2)
                    arcade.draw_text(formula, refX, refY, arcade.color.WHITE, 140, anchor_x="center", anchor_y="center", bold=True)
            # draw current question timer bar
            ratio = 360*(var.totalTime-var.lastQuestionTime)/20
            clr = (int(255*ratio/360),255-int(255*ratio/360),0,210)
            refX = SCREEN_WIDTH/2 - 240
            refY = SCREEN_HEIGHT/2
            arcade.draw_arc_filled(refX, refY, 60, 60,(0,0,0,48), 0, 360, 90)
            arcade.draw_arc_filled(refX, refY, 50, 50,clr, 0, 360-ratio, 90)
        else:
            refX = SCREEN_WIDTH/2+110
            refY = SCREEN_HEIGHT/2+120
            arcade.draw_text( "FIN de l'exercice", refX, refY+12, arcade.color.WHITE, 80, anchor_x="center", anchor_y="center", bold=True)
            arcade.draw_text( "Appuie sur ENTREE ou START pour recommencer", refX, refY-40, arcade.color.WHITE, 24,anchor_x="center", anchor_y="center", bold=True)

        # draw emitters
        for e in var.emitters:
            e.draw()

        # draw current score
        score = int(100*var.nbOK/var.maxQuestions)
        dx = 11 + 10
        dy = 11 + 10 + (var.nbOK-1) * 22
        if var.nbOK > 0:
            arcade.draw_text( str(score)+ "%", dx+15, dy-4, arcade.color.GREEN_YELLOW, 30,anchor_x="left", anchor_y="center", bold=True)




### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A KEY ON THE KEYBOARD
### ====================================================================================================
def onKeyEvent(key,isPressed):

    if not var.hasStarted:
        chooseUser(key,isPressed)
        chooseExo(key,isPressed)
        startExo(key, isPressed)

    elif not isFinished():
        # result ok or not
        if key == arcade.key.SPACE and isPressed:
            resetExercice()
            updateScore(True)
        elif key == arcade.key.BACKSPACE and isPressed:
            resetExercice()
            updateScore(False)
    else:
        if key == arcade.key.ENTER and isPressed:
            initVars()



### ====================================================================================================
### FUNCTION CALLED WHEN YOU PRESS A BUTTON ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onButtonEvent(gamepadNum,buttonNum,isPressed):

    if not var.hasStarted:
        if buttonNum == 7:
            startExo(arcade.key.ENTER, isPressed)

    elif not isFinished():
        if buttonNum == 0 and isPressed:
            resetExercice()
            updateScore(True)
        elif buttonNum == 1 and isPressed:
            resetExercice()
            updateScore(False)
    else:
        if buttonNum == 7 and isPressed:
            initVars()



### ====================================================================================================
### FUNCTION CALLED WHEN YOU MOVE AN AXIS ON A GAMEPAD CONTROLLER
### ====================================================================================================
def onAxisEvent(gamepadNum,axisName,analogValue):

    k = None
    if not var.hasStarted:
        if axisName == "x":
            if analogValue <= -1.0:
                k = arcade.key.LEFT
            if analogValue >= 1.0:
                k = arcade.key.RIGHT
        if axisName == "y":
            if analogValue <= -1.0:
                k = arcade.key.UP
            if analogValue >= 1.0:
                k = arcade.key.DOWN
        if k != None:
            chooseUser(k, True)
            chooseExo(k, True)
            startExo(k, True)


