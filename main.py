###################### FREEWAY TERROR #####################################

#created by Joshua Ramos in 2019


import pygame
import time
import random
import threading
import sys, os
from appJar import gui
from accounts import * #accounts.py has csv code


#Imports the accounts from the CSV file
initAccounts()

accounts.sort(key=lambda x: x[2], reverse=True) # used to sort list of lists by each nested lists' third element (in this case the high score value)

# taken from https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list

saveAccount() #DONT FORGET THIS LINE


### APPJAR GAME LAUNCHER ###


#handle button events

def go(btn): #For when the opening splash screen is opened
    app.hide()
    app.showSubWindow("Login Window")

def exit(btn): # if user wishes to quit
    os._exit(0) #shuts down entire program

def cancel(btn): #if user chooses to stop registering account,
    app.hideSubWindow("Account Registration") # hide 

def validate(btn): #
    #import global variables
    global accounts
    global active_account
    global validated

    
    validated = False #set validated to false

    username = app.getEntry("Username") #get username entries
    password = app.getEntry("Password") # get password entry

    for a in accounts: #Analyse each account in the database
        if username == a[0] and password == a[1]:
            active_account = a
            validated = True
    if not validated:
        app.errorBox("Error", "Invalid Username or Password") # error message
        app.clearEntry("Username") # reset entries
        app.clearEntry("Password") # reset entries
        app.setFocus("Username")
    else:
        validated = True #validated set to true: thus game will start
        app.stop()

def registration():
    app.showSubWindow("Account Registration") #show registration menu

def regoSubmission(btn): #When someone registers
    global accounts
    duplication = False #To prevent usernames with the same name
    
    userN_input = app.getEntry(userN) #get username entries
    pw_input = app.getEntry(pw)
    pw_verification_input = app.getEntry(confirm_pw)

    for a in accounts: #for the accounts in the accounts list
        if a[0] == userN_input: #if the username input is equal to an already existing username
            duplication = True
    
    if pw_verification_input == pw_input and not duplication:
        new_acc = [userN_input, pw_input, 0] #create a new record that will be appended to the CSV file
        accounts.append(new_acc)
        saveAccount()
        app.infoBox("Success!", "The account \"" + userN_input + "\" was successfully created", parent=None)
        app.hideSubWindow("Account Registration")

    else:
        if duplication:
            message = "Username is already taken."
        else:
            message = "Passwords do not match"
        app.errorBox("Error", message) # error message
        app.clearEntry(userN) # reset entries
        app.clearEntry(pw)
        app.clearEntry(confirm_pw)
        app.setFocus(userN)
        

#Create gui variable called app
app = gui("Game Launcher", "650x590")
app.addImage("Game Launcher", "launcherArt.gif")
app.setBg("DodgerBlue")
app.setButtonFont(size = 16, family = "8BIT WONDER", underline=False, slant = "roman")

#text
app.addLabel("Title", "Freeway Terror") #create a label called 'title', displaying 'Freeway Terror"
app.setLabelBg("Title", "black") #make background black
app.setLabelFg("Title", "white") #make font colour white
app.getLabelWidget("Title").config(font =("8BIT WONDER", "40", "bold")) #set font to 8 bit wonder

#link buttons to the function called play
app.addButton("PLAY", go)



### LOGIN CODE ###

validated = False #boolean to determine if user is validated.

#setting up sub window
app.startSubWindow("Login Window", modal=True)
app.setBg("midnight blue")
app.setSize(400, 200)
app.setFont(18)

app.addLabel("lTitle", "Welcome to Freeway Terror") 
app.setLabelBg("lTitle", "black")
app.setLabelFg("lTitle", "white")
app.getLabelWidget("lTitle").config(font=("8BIT WONDER", "15", "bold"))

app.addLabelEntry("Username")
app.addSecretLabelEntry("Password")
app.setLabelFg("Username", "white")
app.setLabelFg("Password", "white")


app.addButtons(["Submit", "Exit"], [validate, exit])
app.setFocus("Username")

#registration
title = "Don't have an account? Click here!"
app.addLink(title, registration)
app.setLinkFg(title, "DodgerBlue")

app.stopSubWindow()




#ACCOUNT REGISTRATION CODE#
app.startSubWindow("Account Registration", modal = True)
app.setBg("midnight blue")
app.setFont(18)
app.setSize(500, 400)

app.addLabel("rTitle", "Create your account") # rtitle is registration title
app.setLabelBg("rTitle", "black")
app.setLabelFg("rTitle", "white")
app.getLabelWidget("rTitle").config(font=("8BIT WONDER", "15", "bold"))

userN = "   Enter username   "
pw = "   Enter password"
confirm_pw = "Re-enter password"

app.addLabelEntry(userN)
app.addSecretLabelEntry(pw)
app.addSecretLabelEntry(confirm_pw)

app.setLabelFg(userN, "white")
app.setLabelFg(pw, "white")
app.setLabelFg(confirm_pw, "white")

app.setFocus(userN)

app.addButtons(["Register", "Cancel"], [regoSubmission, cancel])


app.stopSubWindow()

#Link to create new account



app.go() #start screen




###################################################### MAIN GAME #########################

if validated: #if user has validated themself and logged in,

    pygame.init() #initiate pygame

    #define dimensions of screen
    display_width = 800
    display_height = 600

    #defining colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    light_green = (126, 232, 102)
    blue = (171, 219, 255)
    dark_green = (28, 148, 64)
    grey = (178, 183, 191)
    dark_grey = (68, 68, 69)
    darkish_grey = (126, 129, 133)
    light_grey = (225, 229, 235)

    gold = (209, 178, 2)
    silver = (192,192,192)
    bronze = (187, 144, 0)

    hovered_green = (6, 140, 46)
    hovered_red = (199, 12, 6)
    hovered_gold = (227, 193, 0)

    button_green = (4, 102, 33)
    button_red = (135, 8, 4)


    #width of the car
    car_width = 63

    #app icon for game
    gameIcon = pygame.image.load("appIcon.png")
    pygame.display.set_icon(gameIcon) #set the app icon

    gameDisplay = pygame.display.set_mode((display_width, display_height)) #define the game display

    pygame.display.set_caption('Freeway Terror') # set name to freeway terror

    onToggle = pygame.image.load('toggleOn.png')
    offToggle = pygame.image.load('toggleOff.png')

    clock = pygame.time.Clock()
    #defining clock - A clock times things; specific game clock - used for FPS

    carImg = pygame.transform.flip(pygame.image.load('car19.png'), False, True) # carImg is Car Image

    car_menu = pygame.image.load("selection.png")

    carTypes = [ #Sprites for each car model
        'car1.png', 'car2.png', 'car3.png', 'car4.png', 'car5.png', 'car6.png', 'car7.png', 'car8.png', 'car9.png', 'car10.png', 'car11.png',
        'car12.png', 'car13.png', 'car14.png', 'car15.png', 'car16.png', 'car17.png', 'car18.png', 'car19.png', 'car20.png'
        ]


    duraHearts = ["0 Hearts.png", "1 Heart.png", "2 Hearts.png", "3 Hearts.png"] # Durability Heart Sprites

    boomGif = [ # the following are the frames for the explosion gif: occurs when an incoming car collides with player car
        "b1.png", "b2.png", "b3.png", "b4.png", "b5.png", 'b6.png', "b7.png", "b8.png", "b9.png", "b10.png", "b11.png", "b12.png"
        ]

    pause = False #boolean to determine when to pause or not

    musicOn = True # determines if user wants to turn on/off music

    newHS = False # made true when high score is broken

    def road(roadx, roady, roadw, roadh, colour): #Function to draw the road
        pygame.draw.rect(gameDisplay, white, [roadx - 5, roady, roadw + 10, roadh])
        pygame.draw.rect(gameDisplay, colour, [roadx, roady, roadw, roadh])

    def roadlines(x, y): #function to draw the moving road lines
        for i in range(100): # repeat 100 times
            pygame.draw.rect(gameDisplay, white, [x, y, 5, 65]) #draw dashes of lines
            y += 100 #seperate each by 35 (100-65) pixels
            
    def top_menu(): # The top bar of information while playing game
        pygame.draw.rect(gameDisplay, dark_grey, [0, 0, display_width, 40])

    def durability(d): # d for durability value
        hearts = pygame.image.load(duraHearts[d]) #load heart sprites
        gameDisplay.blit(hearts, (225, 5))
        if d == 0:  #if health = 0
            game_over() #start game over function.
        

    def things_dodged(current_hs, count): #otherwise known as the score function; keeps track of cars dodged. each car dodged is one point.
        font = pygame.font.Font('8-BIT WONDER .TTF',25) #sets the font and size
        text = font.render("Score", True, white)
        dodged = font.render(str(count), True, blue) #display amount of objects dodged
        gameDisplay.blit(text, (10, 5)) # blit label
        gameDisplay.blit(dodged, (145, 5)) # blit nyumber
        high_score(current_hs , count) #update high score if applicable

    def high_score(current, count): #for defining high score
        if count > current:#If the count (current score) is higher than the player's recorded high score,
            current = count # make the new high score count
            global active_account, newHS
            newHS = True #enables message after game is over
            active_account[2] = current #set the new high score to the csv file
            
     
        font = pygame.font.Font('8-BIT WONDER .TTF',25)
        text = font.render("High Score", True, white)
        hscore = font.render(str(current), True, light_green)
        gameDisplay.blit(text, (470, 5))
        gameDisplay.blit(hscore, (710, 5))


    def things(thing,x,y): # xy coordinates 
        gameDisplay.blit(thing, (x,y))

    def musicToggle(x, y, w, h): #Toggle Graphic Dimensions: 64 x 34
        global musicOn

        #gets position and status of mouse
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        
        if musicOn: #if music is on
            gameDisplay.blit(onToggle, (x,y)) #display on toggle
        else:
            gameDisplay.blit(offToggle, (x,y)) #display off toggle

        #label
        font = pygame.font.Font('8-BIT WONDER .TTF',10)
        label = font.render("Toggle Music", True, dark_grey) 
        gameDisplay.blit(label, (x - 120 , y + 10))
        

        if x + w > mouse[0] > x and y + h > mouse[1] > y: #if toggle is hovered over
            if click[0] == 1: # if clicked
                if musicOn:
                    gameDisplay.blit(offToggle, (x,y))
                    pygame.mixer.music.set_volume(0)
                    musicOn = False #turn off music
                    
                else:
                    gameDisplay.blit(onToggle, (x,y))
                    pygame.mixer.music.set_volume(0.15)
                    musicOn = True #turn on music
                    
     ## BUTTONS       
    def button(msg, x, y, w, h, ic, ac, action = None): # parameters: text, xval, yval, width, height, inactive colour, active colour
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + w > mouse[0] > x and y + h > mouse[1] > y: # if button is hovered over
            pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
            if click[0] == 1 and action != None: #if button is clicked
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('button.wav'), maxtime = 600)
                action() #carry out assigned function.
        else:
            pygame.draw.rect(gameDisplay, ic, (x, y, w, h)) #display button as inactive

        smallText = pygame.font.Font('8-BIT WONDER .TTF', 20)
        textSurf, textRect = button_text(msg, smallText)
        textRect.center = ((x+(w / 2)), y + (h / 2))
        gameDisplay.blit(textSurf, textRect)



    def car_button(x, y, w, h, action): # This button is the car at the bottom of the main menu that activates the selection menu.
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        gameDisplay.blit(carImg, (x,y))
                         
        if x + w > mouse[0] > x and y + h > mouse[1] > y: #if button hovered over
            
            if click[0] == 1 and action != None: #if button clicked
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('beep.wav'), maxtime = 600) #play sound
                action() #carry out action

        #label
        font = pygame.font.Font('8-BIT WONDER .TTF',10)
        label = font.render("Click Car to Change Vehicle", True, dark_grey)
        gameDisplay.blit(label, (270, 585))
        pygame.display.update()

        

    def selection_button(x, y, w, h, action, num): # For when selecting cars
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y: 
            if click[0] == 1 and action != None:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('button.wav'), maxtime = 600)
                action(num)

        
        #label
        font = pygame.font.Font('8-BIT WONDER .TTF',10)
        label = font.render("Click Car to Change Vehicle", True, dark_grey)
        gameDisplay.blit(label, (270, 585))
        
        pygame.display.update() #update screen



    def car_selection(): #car selection menu
        #Each car is 35x49 pixels, 2 pixel gap, 13 pixel gap between rows. Coordinates of first car = (207, 291)
        
        selecting = True
        
        buttons = [ ]

        #making buttons for first row of cars
        for c in range(10): # for cars in range 10 (for the 
            bx = 207 + 37 * c # bx = button x coordinate
            button = (bx, 291, 35, 49, car_assignment, c+1)
            buttons.append(button)

        #making buttons for second row of cars
        for c in range(10):
            bx = 207 + 37 * c # bx = button x coordinate
                    
            button = (bx, 353, 35, 49, car_assignment, c+11)
            buttons.append(button)
        
        
        while selecting: #while using selecting screen,
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(1)
           
            for b in buttons: #for all the buttons in the button list
                selection_button(*b) #make them selection buttons

            gameDisplay.blit(car_menu, (190, 230))
            font = pygame.font.Font('8-BIT WONDER .TTF',14)
            label = font.render("Long Click to select vehicle", True, black)
            gameDisplay.blit(label, (210, 250))
            pygame.display.update()
            
                    
            clock.tick(15)

    def car_assignment(num):
        global carImg
        selection = "car" + str(num) + ".png" 
        newCar = pygame.image.load(selection) #swap the sprites out
        carImg = pygame.transform.flip(newCar, False, True)
        main_menu() #go back to main menu

    def car(x,y): #'blit' is drawing something
        gameDisplay.blit(carImg, (x,y)) #The values in the tuple dictate where to spawn the car

    def text_objects(text, font): # For 'You died' screen
        textSurface = font.render(text, True, red) #boolean for anti-aliassing
        return textSurface, textSurface.get_rect()

    def text_objects1(text, font): # For Game intro
        textSurface = font.render(text, True, white) #boolean for anti-aliassing
        return textSurface, textSurface.get_rect()

    def button_text(text, font):
        textSurface = font.render(text, True, light_grey) #boolean for anti-aliassing
        return textSurface, textSurface.get_rect()


    def boom(x, y, i): #boom gif and sound
        boomGif = [
        "b1.png", "b2.png", "b3.png", "b4.png", "b5.png", 'b6.png', "b7.png", "b8.png", "b9.png", "b10.png", "b11.png", "b12.png"
        ]
        
        frame = pygame.image.load(boomGif[i])
        gameDisplay.blit(frame, (x, y)) #display assigned frame

        


    def boom_display(x, y):
        p1 = threading.Thread(target=boom, args=(x, y))  # Threading code taken from https://stackoverflow.com/questions/55881619/sleep-doesnt-work-where-it-is-desired-to/55882173#55882173

        # start the thread execution
        p1.start()

        # wait for it to complete to join it with the main program
        p1.join()


    def game_over():


        #GLOBAL VARIABLES
        global accounts
        global active_account
        global newHS

        accounts.sort(key=lambda x: x[2], reverse=True) #see above
        saveAccount()

        game_over = True #game is now over

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(1)

            #This following only displays if the personal high score is broken
            if newHS: #if there is a new highscore
                font = pygame.font.Font('8-BIT WONDER .TTF',25)
                pygame.draw.rect(gameDisplay, white, [200, 200, 390, 100])
                text = font.render("New High Score", True, gold)
                gameDisplay.blit(text, (227, 210))
                
            #Title
            pygame.draw.rect(gameDisplay, black, [200, 250, 390, 100])
            largeText = pygame.font.Font('8-BIT WONDER .TTF', 50)
            TextSurf, TextRect = text_objects("You Died", largeText)
            TextRect.center = ((display_width/2), (display_height/2))
            gameDisplay.blit(TextSurf, TextRect)

            #Buttons
            button("Restart", 150, 400, 200, 50, button_green, hovered_green, game_loop) #restarts game
            button("Main Menu", 450, 400, 200, 50, button_red, hovered_red, main_menu) #bring user back to main menu
            
            pygame.display.update()
            
            clock.tick(15)

    def quitgame(): #if user wishes to quit game
        pygame.quit()
        os._exit(1) #shut down program

    def unpause(): #if user wants to continue playing
        global pause
        global musicOn
        if musicOn: 
            pygame.mixer.music.set_volume(0.15)
        pause = False

    def paused(): #when user presses 'P' to pause during play
        global musicOn
        
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('beep.wav'), maxtime = 600) 
        if musicOn:
            pygame.mixer.music.set_volume(0.09) #lower volume of music

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(1)

            #Title
            pygame.draw.rect(gameDisplay, dark_grey, [200, 250, 390, 250])
            pygame.draw.rect(gameDisplay, black, [200, 250, 390, 100])
            largeText = pygame.font.Font('8-BIT WONDER .TTF', 50)
            TextSurf, TextRect = text_objects1("Paused", largeText)
            TextRect.center = ((display_width/2), (display_height/2))
            gameDisplay.blit(TextSurf, TextRect)

            #Buttons
            button("Continue", 290, 370, 200, 50, button_green, hovered_green, unpause)
            button("Main Menu", 290, 430, 200, 50, button_red, hovered_red, main_menu)
            
            pygame.display.update()
            
            clock.tick(15)



    def leaderboard():
        global accounts
        tinter = pygame.image.load("tinter.png") #load a tinter to blacken the screen

        on = True

        while on:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        os._exit(1)

            gameDisplay.blit(tinter, (0, 0)) # to tint the screen black to prevent confusion between buttons on main menu + leaderboard
            #background
            pygame.draw.rect(gameDisplay, darkish_grey, [95, 57, 610, 480])

            #titles
            largeText = pygame.font.Font('8-BIT WONDER .TTF', 50)
            TextSurf, TextRect = text_objects1("Leaderboard", largeText)
            TextRect.center = ((display_width/2), (display_height/6))
            gameDisplay.blit(TextSurf, TextRect)

            font = pygame.font.Font('8-BIT WONDER .TTF',15)
            player_label = font.render("Player", True, dark_grey)
            gameDisplay.blit(player_label, (150, 140))

            score_label = font.render("High Score", True, dark_grey)
            gameDisplay.blit(score_label, (520, 140))
            
            
            count = 0 # a count to limit amount of records on the leaderboard

            y_change = 35
            
            for a in accounts:
                font = pygame.font.Font('8-BIT WONDER .TTF',14) #sets the font and size

                rank = count + 1 # integers start from 0, so add one to compensate


                # to change colours to allow for 1st, 2nd, 3rd.
                if rank == 1:
                    font_colour = gold #font set to gold 
                elif rank == 2:
                    font_colour = silver #font set to silver
                elif rank == 3:
                    font_colour = bronze # font set to bronze
                else:
                    font_colour = white #for all other players, text is white.

                #RANK
                rankNum = font.render(str(rank) , True, font_colour) #take the rank and define it as rankNum
                gameDisplay.blit(rankNum, (120, 175 + y_change*count)) #blit rankNum
                
                #USERNAMES
                user_source = a[0] #source of username is a[0] 
                username = font.render(user_source, True, font_colour)
                gameDisplay.blit(username, (150, 175 + y_change*count)) 
                

                #SCORES
                score_source = str(a[2]) #source of score is a[2] 
                score = font.render(score_source, True, font_colour)
                gameDisplay.blit(score, (520, 175 + y_change*count))

                count += 1

                if count == 9: #if There are too many player names to display,
                    break # end this loop

                
                
                
            

             #button to close leaderboard
            button("close", 500, 520, 120, 50, button_red, hovered_red, main_menu)
            
            pygame.display.update()
            clock.tick(15)

    def help_menu():
        menu = pygame.image.load("help_menu.png") #image of help menu
        tinter = pygame.image.load("tinter.png")
        
        on = True

        while on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(1)
                                
            gameDisplay.blit(tinter, (0, 0)) #tints the screen
            gameDisplay.blit(menu, (200, 50)) #display help menu
            
            #create button to close help menu
            button("close", 500, 520, 120, 50, button_red, hovered_red, main_menu)

            pygame.display.update()

            clock.tick(15)


    ## MAIN MENU + GAME LOOP ##

    def main_menu():

        global pause
        global account
        global active_account

        player = active_account[0] # the name of the player is the first element of the list active_account
        

        menu = True #menu is true
        pause = False #pause set to false

        while menu: #while user is using the menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(1)
                    
            
            
            #Background
            gameDisplay.fill(dark_green) #fill background
            road(85, 0, 800 - 2 * (85), 600, grey) #create road


            
            
            for i in range(85 * 2 - 2, 800 - 63,  85 - 2):
                 roadlines(i, 0) #make roadlines

            
            #Player profile (top left)
            pygame.draw.rect(gameDisplay, darkish_grey, [0, 0, 250, 50])
            font = pygame.font.Font('8-BIT WONDER .TTF',14)
            text = font.render("Player", True, black) #label
            user = font.render(player, True, blue) #player name
            gameDisplay.blit(text, (10, 5)) #display to screen
            gameDisplay.blit(user, (100, 5))

            hs_label = font.render("High Score", True, black) #show user high score
            hs = font.render(str(active_account[2]), True, light_green)
            gameDisplay.blit(hs_label, (10, 30))
            gameDisplay.blit(hs, (140, 30))
            
            


            #Title
            pygame.draw.rect(gameDisplay, black, [0, 250, 800, 100])
            
            
            largeText = pygame.font.Font('8-BIT WONDER .TTF', 50)
            TextSurf, TextRect = text_objects1("Freeway Terror", largeText)
            TextRect.center = ((display_width/2),(display_height/2))
            gameDisplay.blit(TextSurf, TextRect)
            
            #Music Toggle
            musicToggle(700, 25, 64, 34)

            #Buttons
            button("PLAY", 150, 450, 100, 50, button_green, hovered_green, game_loop)
            button("Exit", 550, 450, 100, 50, button_red, hovered_red, quitgame)
            
            #access leaderboard
            button("leaderboard", 540, 120, 230, 50, gold, hovered_gold, leaderboard)

            #access help menu
            button("HELP", 670, 65, 100, 50, dark_grey, darkish_grey, help_menu)
            car_button(360, 480, 63, 93, car_selection)
            
                   

            
            
            pygame.display.update()
            
            clock.tick(15)
            


    def game_loop():

        global pause
        global active_account

        pause = False

        high_score = active_account[2]
        
        #These define where the car starts
        x = (display_width * 0.45) # (360)
        y = (display_height * 0.8) # (480)

        x_change = 0
        y_change = 0
        dodged = 0
        side_width = 85

        crashed = False

        tick = 0

        xInc = 85 # increment of random x
        xRange = (side_width, display_width - side_width - car_width, xInc)
        
        obstacles = [[pygame.image.load(random.choice(carTypes)), random.randrange(*xRange), -600]] # List of incoming cars
     
        d = 3
        
        thing_speed = 7 #speed originally se to be seven
        line_speed = 4.5 #notice lines move slightly less than cars
        line_y = 0

        

        thing_height = 93
        thing_width = 63
        gameExit = False

        #set variables for explosion
        boomi = 0
        boomx = 0
        boomy = 0

        boomShow = False #do not show explosion gif
        
        while not gameExit:
            
            #DEFINING KEY BINDINGS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    os._exit(1)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: #if left arrow key is pressed
                        x_change = -5 #move to the left
                    elif event.key == pygame.K_RIGHT:
                        x_change = 5
                    if event.key == pygame.K_p: # if P is pressed
                        pause = True #pause game
                        paused()
                        
                if event.type == pygame.KEYUP: #reset once keys are up
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        while x_change != 0:
                            if x_change < 0:
                                x_change += 1
                            else:
                                x_change -= 1


            # x Barriers
            x_moving = False
        
            if x_change < 0:
                if x > side_width: #if x is within the barrier
                    x_moving = True #it can move
            else:
                if x < display_width - car_width - side_width: #if x is within the barrier
                    x_moving = True # it can move

            if x_moving: #if not in barrier
                x += x_change #move  car
            
            gameDisplay.fill(dark_green)
            road(side_width, 0, display_width - 2 * (side_width), display_height, grey)
            
            for i in range(side_width * 2 - 2, display_width - car_width, xInc - 2):
                 roadlines(i, line_y) # create roadlines that move (line_y is increased every tick)


            
            for t in obstacles:
                if t[2] > display_height:
                    t[0] = pygame.image.load(random.choice(carTypes))
                    t[2] = random.randrange(-400, 0, 200) - thing_height #spawn in defined domain
                    t[1] = random.randrange(*xRange) #spawn car between defined range
                    
                    dodged += 1
                    
                    if dodged % 15 == 0: #if player has dodged 15 cars
                        thing_speed += 0.25 # increase speed by 0.25
                        line_speed += 0.1 #increase line speed
                        
                    if dodged % 4 == 0 and dodged != 0: #every four dodged cars
                        if len(obstacles) < 5: 
                            obstacles.append([pygame.image.load(random.choice(carTypes)), random.randrange(*xRange), -600]) #spawn a new car
                    if random.randrange(0, 100) < 50 and len(obstacles) >= 3: #if there are 3 or more cars there is a 50% chance of one despawning
                        for t in obstacles:
                            if t[2] > display_height:
                                obstacles.remove(t)
                things(t[0], t[1], t[2]) ## each parameter is image, x coordinate, y coordinate
                t[2] += thing_speed #increase speed

                #COLLISION
                if y < t[2] + thing_height:
                    # y crossover has occured
                    if t[1] < x + car_width and t[1] + thing_width > x:
                        if t[2] < y + car_width and t[2] + thing_width > y:
                            boomShow = True #reveal explosion
                            boomx = t[1] #move explosion to coordinate of car
                            boomy = t[2]
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound('crash.wav'), maxtime = 600)
                            obstacles.remove(t)
                            d -= 1 # -1 from durability
                
            top_menu() #create top menu
            things_dodged(high_score, dodged) #show score
            durability(d) #check durability

            
            line_y += line_speed #increase line speed
            
            if line_y > 0: #if line touches 0
                line_y = -600 # put it back to y = -600 to maintain flow of lines

            if len(obstacles) == 0:
                obstacles.append([pygame.image.load(random.choice(carTypes)), random.randrange(*xRange), -600])
                
            car(x, y) #spawn car
            


            if boomShow: #if the explosion is to be shown
                boom(boomx, boomy, boomi) #display frame

                #update frame every 2 ticks
                if tick % 2 == 0: 
                    boomi += 1
            
                #once all 12 frames have been played, hide explosion again
                if boomi >= 12:
                    boomShow = False
                    boomi = 0

                tick += 1
            
            pygame.display.update()
            clock.tick(60) #parameter is the FPS


    #Initiate Background Music
    pygame.mixer.init()
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(loops = -1)

    pygame.mixer.Channel(1).set_volume(0.2) #set volume of audio channel 1


    #Initiate Main Menu to start game
    main_menu()

