#www.stuffaboutcode.com
#Raspberry Pi, Minecraft Sound - Add some sound effects to minecraft

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import pygame to use the mixer to play wav file
import pygame

# constants
STOPPED = 1
WALKING = 2
FALLING = 3

if __name__ == "__main__":

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()

    #Initialise pygame and the mixer
    pygame.init()
    pygame.mixer.init()

    #load WAVS files
    soundWalking = pygame.mixer.Sound("sounds/walking.wav")
    soundJump = pygame.mixer.Sound("sounds/jump.wav")
    soundFalling = pygame.mixer.Sound("sounds/falling.wav")
    soundBang = pygame.mixer.Sound("sounds/bang.wav")
    soundSword = pygame.mixer.Sound("sounds/sword.wav")

    # setup variables
    lastPlayersState = STOPPED
    playersState = STOPPED
    playerJumped = False
    playerFalling = False
    playerFallDistance = 0

    #get players position
    lastPlayerPos = mc.player.getPos()
    
    mc.postToChat("Minecraft Sound Effects - www.stuffaboutcode.com")
    
    # loop until CTRL C
    try:
        while(True):
            
            # get players position
            currentPlayerPos = mc.player.getPos()

            # has the player moved in either X or Z (are they WALKING?)
            if lastPlayerPos.x != currentPlayerPos.x or lastPlayerPos.z != currentPlayerPos.z:
                # if player is FALLING they cant be WALKING
                if playersState != FALLING:
                    playersState = WALKING

            # has the player moved in positive Y (have they jumped?)
            if int(lastPlayerPos.y) < int(currentPlayerPos.y):
                playerJumped = True

            # has the player moved in negative Y (are they FALLING?)
            if int(lastPlayerPos.y) > int(currentPlayerPos.y):
                playersState = FALLING

            # is the player still falling?
            if playersState == FALLING and lastPlayersState == FALLING:
                # increase the distance they have fallen
                playerFallDistance = playerFallDistance + (lastPlayerPos.y - currentPlayerPos.y)

            # if the player is FALLING but has stopped moving down
            # (have they STOPPED FALLING?)
            if playersState == FALLING and int(lastPlayerPos.y) == int(currentPlayerPos.y):
                playersState = STOPPED

            # has the player STOPPED
            if lastPlayerPos.x == currentPlayerPos.x and lastPlayerPos.z == currentPlayerPos.z:
                playersState = STOPPED

            # if last players state != walking and players state = walking
            # player has started WALKING
            if lastPlayersState != WALKING and playersState == WALKING:
                soundWalking.play(-1)

            # if last players state = walking and players state != walking
            # player has stopped WALKING
            if lastPlayersState == WALKING and playersState != WALKING:
                soundWalking.stop()

            # if the players state = falling and the distance they have fell is greater than 3
            # player has started FALLING
            if playersState == FALLING and playerFallDistance > 3:
                if playerFalling == False:
                    soundFalling.play()
                    playerFalling = True

            # if last players state = falling and the players state != falling
            # player has stopped falling
            if lastPlayersState == FALLING and playersState != FALLING and playerFalling == True:
                soundFalling.stop()
                soundBang.play()
                playerFallDistance = 0
                playerFalling = False
            
            # if player has jumped and the jump sound is not playing
            if playerJumped == True:
                soundJump.play()
                playerJumped = False

            lastPlayerPos = currentPlayerPos
            lastPlayersState = playersState

            #Get the block hit events
            blockHits = mc.events.pollBlockHits()
            # if a block has been hit play sword sound
            if blockHits:
                soundSword.play()
            
            # sleep for a bit
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("stopped")
