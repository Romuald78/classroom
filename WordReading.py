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

    # get user names
    # var.allUsers     = ["EMELINE","NATHAN","ROMU","MIMI"]
    fp = open("names2.txt","r")
    lines = fp.readlines()
    fp.close()
    var.allUsers = [x.replace("\n", "") for x in lines]

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

    # fill stats
    var.stats = {}
    fp = open("save_records.txt", "r", encoding='utf-8')
    lines = fp.readlines()
    fp.close()
    for line in lines[1:]:
        tab = line.replace("\n", "").split(",")
        usr = tab[1]
        mat = tab[2]
        scr = tab[3]
        tim = tab[4]
        if usr not in var.stats.keys():
            var.stats[usr] = {}
        if mat not in var.stats[usr].keys():
            var.stats[usr][mat] = []
        var.stats[usr][mat].append((int(scr),float(tim)))

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
            chooseNumbers(10,10)
    if var.exoType == "MULTIPLICATION":
        if var.number1 == 0 and var.number2 == 0:
            chooseNumbers(10,10)

def startExo(key,isPressed):
    if key == arcade.key.ENTER and isPressed and var.exoType != "" and var.userName != "":
        var.totalTime  = 0
        var.lastQuestionTime = 0
        var.nbFAIL = 0
        var.nbOK = 0
        var.hasStarted = True


def drawStats():
    # draw USER STATS
    refH = 250
    refW = 500
    refX = SCREEN_WIDTH / 2 - 70-140
    refY = SCREEN_HEIGHT / 2
    # draw back
    arcade.draw_rectangle_filled(refX + refW / 2, refY + refH / 2, refW, refH, (255, 255, 255, 16))
    # draw grid
    for i in range(1, 10, 1):
        dx = i * refW / 10
        dy = i * refH / 10
        if i % 2 == 1:
            # vertical secondary axe
            arcade.draw_line(refX + dx, refY, refX + dx, refY + refH, (255, 255, 255, 24), 1)
            # horizontal secondary axe
            arcade.draw_line(refX, refY + dy, refX + refW, refY + dy, (255, 255, 255, 24), 1)
        else:
            # vertical axe
            arcade.draw_text(str(400 - i * 40) + "s.", refX + dx, refY - 5, arcade.color.WHITE, 12, anchor_x="center",
                             anchor_y="top", bold=True)
            arcade.draw_line(refX + dx, refY, refX + dx, refY + refH, (255, 255, 255, 48), 1)
            # horizontal axe
            arcade.draw_text(str(50 + i * 5) + "%", refX - 5, refY + dy, arcade.color.WHITE, 12, anchor_x="right",
                             anchor_y="center", bold=True)
            arcade.draw_line(refX, refY + dy, refX + refW, refY + dy, (255, 255, 255, 48), 1)
    # draw grid borders
    arcade.draw_line(refX, refY, refX, refY + refH, arcade.color.WHITE, 1)
    arcade.draw_line(refX, refY, refX + refW, refY, arcade.color.WHITE, 1)
    # for each user
    for usr in var.allUsers:
        datas = var.stats[usr]
        # for each exercice
        for m in datas.keys():
            ptSize = 3
            clr = (255, 255, 255, 160)
            if var.userName == usr:
                ptSize = 7
                clr = (255, 255, 255, 160)
                if var.exoType == m:
                    ptSize = 10
                    clr = (255, 255, 0, 192)
            # display all points for this user and this exercice
            if len(datas[m]) > 0:
                pScr = datas[m][0][0]
                pTim = datas[m][0][1]
            for d in datas[m]:
                if d[0] >= 50 and d[1] <= 400:
                    tim0 = refW * ((400 - pTim) / 400)
                    scr0 = refH * (pScr - 50) / 50
                    tim1 = refW * ((400 - d[1]) / 400)
                    scr1 = refH * (d[0] - 50) / 50
                    if var.userName == usr:
                        clr2 = (clr[0], clr[1], clr[2], 64)
                        arcade.draw_line(refX + tim0, refY + scr0, refX + tim1, refY + scr1, clr2, 1)
                    arcade.draw_point(refX + tim1, refY + scr1, clr, ptSize)
                pScr = d[0]
                pTim = d[1]


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
    em = createParticleBurst(old.center_x, old.center_y, 0.0025, 0.25, 100, 0.5, 6.0, arcade.color.WHITE, 100,0, spritePath)
    var.emitters.append(em)

def processInGame(deltaTime):
    # increase total time
    var.totalTime += deltaTime
    #choose new word/computation if not existing
    getRandomQuestion()
    # check if the current question is not too long (20sec max)
    if var.totalTime - var.lastQuestionTime >= 20:
        print("update SCORE 1")
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
        if var.hasStarted:
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
        # draw stats
        drawStats()

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
        refX = SCREEN_WIDTH/2+50
        refY = SCREEN_HEIGHT/2-100
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
            clr = (int(255*ratio/360),255-int(255*ratio/360),0,225)
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
            chooseUser(arcade.key.ENTER, isPressed)
            chooseExo(arcade.key.ENTER, isPressed)
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


