#Jason Tse
#CST 205 Final Project

#---------------------------------------------
#----- MODULE IMPORT AND MEDIA DIRECTORY -----
#---------------------------------------------
import time    #imported for animations
import random  #imported for random generation of game elements
import thread  #imported for running concurrent events
currentDirectory = __file__[:-13] #removes this file's name from file path to get current directory
setMediaFolder(currentDirectory)


#------------------------
#----- PLAYER CLASS -----
#------------------------
class Player:
  def __init__(self):
    self.sprite = makePicture("images/player_sprite.jpg")
    self.x = 0  
    self.y = 0
  
        
#--------------------------
#----- MAIN GAME LOOP -----
#--------------------------
def main():
  #--- INITIALIZATION ---
  """
    Initialization sets up the first screen the player sees.
    The gameMap with tiles and obstacles will not change during gameplay.
    An updateMap will be used for placing sprites.
    The hitMap image will be updated to reflect the location of game elements.
  """
  #loading window and tutorial
  nowLoadingMsg = "Please Wait ... Now Loading\n"
  tutorialMsg = "Tutorial coming soon"
  thread.start_new_thread(showInformation, (nowLoadingMsg + tutorialMsg,))

  #create turtle renderer to output graphics
  renderOutput = makeWorld(800, 600)
  renderCoord = makeTurtle(renderOutput)
  renderCoord.penUp()         #stop turtle pen trail
  renderCoord.hide()          #hide turtle icon
  moveTo(renderCoord, 0 , 0)  #move to render full screen image
  
  #generate random map
  #map is actively 800 x 544 broken into 25 x 17 cells of 32 pixel width squares
  #map will be randomized for every game instance
  unit = 32
  rockSpawnCount = 4                             #determines number of rocks spawned on map
  rockTile = makePicture("images/rock_tile.jpg")
  treeSpawnCount = 8                             #determines number of trees spawned on map
  treeTile = makePicture("images/tree_tile.jpg")
  spawnX = random.randrange(0, 778, 32)          #initial spawn point set at random
  spawnY = random.randrange(32, 512, 32)
  
  gameMap = makeEmptyPicture(800, 600, black)    #gameMap is the initial game layout
  updateMap = makeEmptyPicture(800, 600)         #updateMap is the rendered image for imposing sprites
  hitMap = makeEmptyPicture(800, 600, white)     #hitMap is used for collision detections
  
  #add frame to hitMap
  for pixels in getPixels(hitMap):
    if getY(pixels) < 32 or getY(pixels) > 544:
      setColor(pixels, black)
  #generate grass tiles
  for x in range(0, 800, unit):
    for y in range(32, 544, unit):
      tileNum = random.randint(1, 5)                                             #get random grass tile (5 different tiles)
      grassTile = makePicture("images/grass_tiles" + str(tileNum) + ".jpg")
      pasteToMap(gameMap, grassTile, x, y)
  #generate rock obstacles
  for i in range(rockSpawnCount):
    while collisionCheck(hitMap, rockTile, spawnX, spawnY, black):               #loop until free space found
      spawnX = random.randrange(0, 778, 32)
      spawnY = random.randrange(32, 512, 32)
    pasteToMap(gameMap, rockTile, spawnX, spawnY)                                #update gameMap
    pasteToMap(hitMap, makeEmptyPicture(32, 32, black), spawnX, spawnY)          #update hitMap
  #generate tree obstacles
  for i in range(treeSpawnCount):
    while collisionCheck(hitMap, treeTile, spawnX, spawnY, black): 
      spawnX = random.randrange(0, 778, 32)
      spawnY = random.randrange(32, 480, 32)
    pasteToMap(gameMap, treeTile, spawnX, spawnY)
    pasteToMap(hitMap, makeEmptyPicture(32, 64, black), spawnX, spawnY)
    
  #clone gameMap to updateMap
  cloneMap(gameMap, updateMap)
    
  #spawn player
  player = Player()                                                              #creates Player object
  while collisionCheck(hitMap, player.sprite, spawnX, spawnY, black):    
    spawnX = random.randrange(0, 778, 32)
    spawnY = random.randrange(32, 512, 32)
  player.x = spawnX
  player.y = spawnY                                                              #set player's starting coordinates
  pasteToMap(updateMap, player.sprite, player.x, player.y, white)                #add sprite to update map    
  
  #render map
  drop(renderCoord, updateMap)
  #DEBUG: show hit map
  #show(hitMap)
      
      
#---------------------------      
#----- OTHER FUNCTIONS -----
#---------------------------
#Pastes a tile or sprite to given map.
#If chromaKey color is passed, will only copy pixels not the same as chromaKey.
def pasteToMap(map, tile, mapX, mapY, chromaKey = 0):        #chromakey is an optional parameter that will default to 0
  tileX = 0                                                     
  tileY = 0
  for x in range(mapX, mapX + getWidth(tile)):
    for y in range(mapY, mapY + getHeight(tile)):
      inputPixel = getPixel(tile,tileX,tileY)
      outputPixel = getPixel(map, x, y)
      if type(chromaKey) is not int:                         #if chromaKey is defined, only copy pixels not similar to chromaKey
        if distance(getColor(inputPixel), chromaKey) > 60:
          setColor(outputPixel, getColor(inputPixel))
      else:                                                  #else chromaKey isn't defined, copy all pixels.
        setColor(outputPixel, getColor(inputPixel))
      tileY += 1
      
    tileX += 1
    tileY = 0

  
#Checks if given object collides on hitMap and 
#return boolean true if collision detected, otherwise false
#Does not alter hitMap
#targetColor definitions:
#black = obstacles, uninteractive
#red = player's character
#blue = enemy character
#green = item
def collisionCheck(hitMap, object, objectX, objectY, targetColor):
  for x in range(objectX, objectX + getWidth(object)):
    for y in range(objectY, objectY + getHeight(object)):
      pixel = getPixel(hitMap, x, y)
      if getColor(pixel) == targetColor:
        return true
  return false
  
#clones map to map
def cloneMap(copyFromMap, copyToMap):
  for pixels in getPixels(copyFromMap):
    outputPixel = getPixel(copyToMap, getX(pixels), getY(pixels))
    setColor(outputPixel, getColor(pixels))
 
  
#-------------------------  
#----- FUNCTION CALL -----
#-------------------------
main()
  