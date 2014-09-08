
import pygame, os, sys, time, random
from pygame.locals import *

           #R    G    B
BLUE =     (0,   0,   255)
GREEN =    (0,   128, 0)
PURPLE =   (128, 0,   128)
RED =      (255, 0,   0)
YELLOW =   (255, 255, 0)
NAVYBLUE = (0,   0,   128)
WHITE =    (255, 255, 255)
BLACK =    (0,   0,   0)
ALPHA =    (255, 0,   255)

def PokemonStrip(targetFile):
  with open(targetFile, 'r') as f:
    fileString = f.read()
    fileList = fileString.split('\n')
    i = 0
    targetList = []
    while i<11:
      targetList.append(fileList[i])
      i += 1
    f.close()
  return targetList
  
def MoveStrip(pokemonList, moveNumber):
  moveName = pokemonList[moveNumber+3].lower() + '.txt' 
  with open(moveName, 'r') as f:
    fileString = f.read()
    fileList = fileString.split('\n')
    i = 0
    moveList = []
    while i<6:
      moveList.append(fileList[i])
      i += 1
    f.close()
  return moveList
  
def PlayerChoice(targetFile):
  pPokemon = []
  pPokemon = PokemonStrip(targetFile)
  moveNumber = 1
  pAttackList = []
  while moveNumber<5:
    pAttackList.append(MoveStrip(pPokemon, moveNumber))
    moveNumber += 1
  return [pPokemon, pAttackList]

def ComputerChoice(choices):
  choice = random.randint(0,1)
  if choices[choice] == "Charmander":
    computerImgList = charImages
  elif choices[choice] == "Bulbasaur":
    computerImgList = bulbImages
  elif choices[choice] == "Squirtle":
    computerImgList = squirtImages
  targetFile = choices[choice].lower() + '.txt'
  cPokemon = []
  cPokemon = PokemonStrip(targetFile)
  moveNumber = 1
  cAttackList = []
  while moveNumber<5:
    cAttackList.append(MoveStrip(cPokemon, moveNumber))
    moveNumber += 1
  return [cPokemon, cAttackList, computerImgList]
  
def redraw():
  DISPLAYSURF.blit(playerImgList[1], (0,200))
  drawText(pPokemon[0], font, DISPLAYSURF, 200, 325, WHITE)
  playerBar.drawRects()
  DISPLAYSURF.blit(computerImgList[0], (200, 0))
  drawText(cPokemon[0], font, DISPLAYSURF, 10, 45, WHITE)
  computerBar.drawRects()
  pygame.display.update()

def displayMessage(message):
  drawText(message, font, DISPLAYSURF, 10,400, WHITE)
  time.sleep(1)
  DISPLAYSURF.fill(BLACK)
  redraw()
  
def Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList):
  pStats = [1, 1]
  cStats = [1, 1]
  fainted = False
  
  playerBar = HealthBar()
  playerBar.init(200,315)
  computerBar = HealthBar()
  computerBar.init(10,35)
  
  while fainted != True:
    DISPLAYSURF.fill(BLACK)
    drawText(pPokemon[0].upper() + "! I choose you!", font, DISPLAYSURF, 10,400, WHITE) 
    time.sleep(1)
    DISPLAYSURF.blit(playerImgList[1], (0,200))
    drawText(pPokemon[0], font, DISPLAYSURF, 200, 325, WHITE)
    playerBar.drawRects()
    time.sleep(1)
    DISPLAYSURF.fill(BLACK)
    drawText("Computer sent out " + cPokemon[0], font, DISPLAYSURF, 10,400, WHITE)
    time.sleep(1)
    redraw()
    
    pMove = pMoveSelect(pMoveList)
    cMove = cMoveSelect(cMoveList)
    ClearTerminal()
    
    if pPokemon[2] < cPokemon[2]:
      pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
      computerBar.updateBar(cPokemon)
      if cPokemon[1] <= 0:
        fainted = True
        winner = "Player"
        break
      time.sleep(.5)
      cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
      playerBar.updateBar(pPokemon)
      if pPokemon[1] <= 0:
        fainted = True
        winner = "Computer"
        break
      time.sleep(.5)
    else:
      cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
      playerBar.updateBar(pPokemon)
      if pPokemon[1] <= 0:
        fainted = True
        winner = "Computer"
        break
      time.sleep(.5)
      pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
      computerBar.updateBar(cPokemon)
      if cPokemon[1] <= 0:
        fainted = True
        winner = "Player"
        break
      time.sleep(.5)
    print pPokemon[0] + "'s health is:", pPokemon[1]
    print cPokemon[0] + "'s health is:", cPokemon[1]
  print "Ther winner is: " + winner
  
def pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats):
  displayMessage(pPokemon[0] + " used " + pMove[5])
  print pPokemon[0] + " used " + pMove[5] + "."
  print ""
  mode = pMove[0]
  if mode == "1":
    cPokemon = DamageMod(pPokemon, pMove, cPokemon, pStats, cStats)
  elif mode == "21":
    pStats = StatMod(pMove, pStats, pStats)
  elif mode == "22":
    cStats = StatMod(pMove, pStats, cStats)

def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats):
  displayMessage(cPokemon[0] + " used " + cMove[5] + ".")
  print ""
  mode = cMove[0]
  if mode == "1":
    pPokemon = DamageMod(cPokemon, cMove, pPokemon, cStats, pStats)
  elif mode == "21":
    cStats = StatMod(cMove, cStats, cStats)
  elif mode == "22":
    pStats = StatMod(cMove, cStats, pStats)
    
def DamageMod(attacker, attack, target, attackerStats, targetStats):
  typeAdvantage = AdvantageCalc(attack, target)
  DMG = int(attack[2])
  aATK = StatIndex(attackerStats, "A")
  tDEF = StatIndex(targetStats, "D")
  effect = DMG*(aATK/tDEF)*typeAdvantage
  target[1] = int(target[1]) - effect
  print attacker[0] + " dealt", effect, "damage!"
  print ""
  return target
  
def StatMod(move, attackerStats, targetStats):
  targetStat = move[4]
  effect = move[3]
  if targetStat == "A":
    if effect == "-":
      targetStats[0] -= 1
      return targetStats
    else:
      targetStats[0] += 1
      return targetStats
  else:
    if effect == "-":
      targetStats[0] -= 1
      return targetStats
    else:
      targetStats[0] += 1
      return targetStats

def StatIndex(stats, statType):
  statIndex = [(1.0/4),(2.0/7),(1.0/3),(2.0/5),(1.0/2),(2.0/3), 1, 1.5, 2, 2.5, 3, 3.5, 4]
  if statType == "A":
    statInQuestion = stats[0]
  else:
    statInQuestion = stats[1]
  trueStat = statIndex[statInQuestion+5]
  return trueStat

def AdvantageCalc(attack, target):
  combo = attack[1] + target[3]
  if combo == "FG":
    typeAdvantage = 2
  elif combo == "FW":
    typeAdvantage = .5
  elif combo == "FN":
    typeAdvantage = 1
  elif combo == "WF":
    typeAdvantage = 2
  elif combo == "WG":
    typeAdvantage = .5
  elif combo == "WN":
    typeAdvantage = 1
  elif combo == "GF":
    typeAdvantage = .5
  elif combo == "GW":
    typeAdvantage = 2
  elif combo == "GN":
    typeAdvantage = 1
  elif combo == "NF":
    typeAdvantage = 1
  elif combo == "NW":
    typeAdvantage = 1
  elif combo == "NG":
    typeAdvantage = 1
  return typeAdvantage
  
def cMoveSelect(cMoveList):
  cMove = cMoveList[random.randint(0,3)]
  return cMove
  
def pMoveSelect(pMoveList):
  print "What will " + pPokemon[0] + " do?"
  time.sleep(1)
  print "Your choices are... "
  PrintMoves(pMoveList)
  pMoveChoice = raw_input("")
  tracker = 0
  for x in pMoveList:
    if x[5] == pMoveChoice:
      pMove = pMoveList[tracker]
      break
    else:
      tracker += 1
  return pMove

def PrintMoves(moveList):
  for x in moveList:
    print x[5]
  print ""

def PrintChoices(choices):
  for x in choices:
    print x
  print ""

def ClearTerminal():
  os.system('cls' if os.name=='nt' else 'clear')

def drawText(text, font, surface, x, y, color):
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  
  textobj1 = font.render(textLine1,1,color)
  textrect1 = textobj1.get_rect()
  textrect1.topleft = (x,y)
  surface.blit(textobj1,textrect1)
  pygame.display.update()
  
  textobj2 = font.render(textLine2,1,color)
  textrect2 = textobj2.get_rect()
  textrect2.topleft = (x,y+10)
  surface.blit(textobj2,textrect2)
  pygame.display.update()
    
def animateText(text, font, surface, x, y, color):
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  i = 0
  for letter in textLine1:
    realLine1 = textLine1[:i]
    textobj1 = font.render(realLine1,1,color)
    textrect1 = textobj1.get_rect()
    textrect1.topleft = (x,y)
    surface.blit(textobj1,textrect1)
    pygame.display.update()
    fpsClock.tick(FPS)
    i += 1
  j = 0
  for letter in textLine2:
    realLine2 = textLine2[:j]
    textobj2 = font.render(textLine2,1,color)
    textrect2 = textobj2.get_rect()
    textrect2.topleft = (x,y+10)
    surface.blit(textobj2,textrect2)
    pygame.display.update()
    j += 1
  
class Button():
  def assignImage(self, picture):
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
    self.rect.topleft = x,y
  def drawButton(self, picture):
    DISPLAYSURF.blit(picture, self.rect)
  def pressed(self,mouse):
    if self.rect.collidepoint(mouse) == True:
      return True

class HealthBar():
  def init(self,x,y):
    self.position = x,y
    self.negDimensions = (150,5)
    self.posDimensions = [150,5]
  def drawRects(self):
    #(x,y,width,height)
    pygame.draw.rect(DISPLAYSURF, RED, (self.position, self.negDimensions))
    pygame.draw.rect(DISPLAYSURF, GREEN, (self.position, self.posDimensions))
    pygame.display.update()
  def updateBar(self, pokemonList):
    maxHealth = pokemonList[8]
    currentHealth = pokemonList[1]
    healthProportion = int(currentHealth)/float(maxHealth)
    newDimension = healthProportion*self.negDimensions[0]
    self.posDimensions[0] = newDimension
    
def BulbImages():
  fileNames = ["bulbasaurFront.png","bulbasaurBack.png"]
  bulbArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    bulbArray.append(newImg)
  return bulbArray
  
def CharImages():
  fileNames = ["charmanderFront.png","charmanderBack.png"]
  charArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    charArray.append(newImg)
  return charArray
  
def SquirtImages():
  fileNames = ["squirtleFront.png","squirtleBack.png"]
  squirtArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    squirtArray.append(newImg)
  return squirtArray

if __name__ == '__main__':
  pygame.init()
  fpsClock = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((400, 600))
  TEXTSURF = pygame.display.set_mode((400,600))
  TEXTSURF.set_colorkey(ALPHA)
  pygame.display.set_caption('Pykemon')
  FPS = 15
  font = pygame.font.SysFont(None, 20)
  
  bulbImages = BulbImages()
  bulbFront = bulbImages[0]
  bulbBack = bulbImages[1]
  squirtImages = SquirtImages()
  squirtFront = squirtImages[0]
  squirtBack = squirtImages[1]
  charImages = CharImages()
  charFront = charImages[0]
  charBack = charImages[1]
  transparent = pygame.image.load("transparent.png")
  
  message = "Choose your Pokemon!"
  
  charButton = Button()
  charButton.assignImage(charFront)
  charButton.setCoords(0, 200)
  squirtButton = Button()
  squirtButton.assignImage(squirtFront)
  squirtButton.setCoords(200, 200)
  bulbButton = Button()
  bulbButton.assignImage(bulbFront)
  bulbButton.setCoords(100, 400)
          
  charButton.drawButton(charFront)
  squirtButton.drawButton(squirtFront)
  bulbButton.drawButton(bulbFront)
    
  drawText("This is visible", font, TEXTSURF, 120, 100, WHITE)
  drawText("This shouldn't be.", font, TEXTSURF, 120, 120, ALPHA)
  drawText("Control", font, TEXTSURF, 120, 140, WHITE)
     
  pygame.display.update()
  
  choices = ['Charmander', 'Squirtle', 'Bulbasaur']

  picked = 0
  while picked == 0:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if charButton.pressed(mouse) == True:
          choice = "Charmander"
          playerImgList = charImages
          picked = 1
        if squirtButton.pressed(mouse) == True:
          choice = "Squirtle"
          playerImgList = squirtImages
          picked = 1
        if bulbButton.pressed(mouse) == True:
          choice = "Bulbasaur"
          playerImgList = bulbImages
          picked = 1
#  print 'Your choices are: '
#  PrintChoices(choices)
#  choice = raw_input('Which Pokemon will you choose?... ')
  targetFile = choice.lower() + '.txt'
  choices.remove(choice)
 
  playerChoice = PlayerChoice(targetFile)
  pPokemon = playerChoice[0]
  pMoveList = playerChoice[1]
  ClearTerminal()
  print pPokemon[0].upper() + "! I choose you!"
  print ""
  time.sleep(.5)
  computerChoice = ComputerChoice(choices)
  cPokemon = computerChoice[0]
  cMoveList = computerChoice[1]
  computerImgList = computerChoice[2]
  print "Computer sent out " + cPokemon[0]
  print ""
  
  playerBar = HealthBar()
  playerBar.init(200,315)
  computerBar = HealthBar()
  computerBar.init(10,35)
  
  Battle(pPokemon, pMoveList, cPokemon, cMoveList, playerImgList, computerImgList)

  
  
