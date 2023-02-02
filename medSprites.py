from baseClasses import Button, ButtonGroup
from classes import BoxGroup, TextBox

fileFinderButtons = []
fileFinderButtons.append(ButtonGroup())
Button((125,50),2,"Back","Back",(255,255,255),(0,0,0),(75,850),fileFinderButtons[0])
Button((125,50),2,"Load","Load",(255,255,255),(0,0,0),(1200,100),fileFinderButtons[0])
for i in range(0,12):
    Button((600,50),2,"",i,(255,255,255),(0,0,0),(800,200+(50*i)),fileFinderButtons[0])
fileFinderBox = BoxGroup()
TextBox((600,50),2,"Search for file","File","Text",(255,255,255),(0,0,0),(800,100),fileFinderBox,True)
# buttons that can be activated
fileFinderButtons.append(ButtonGroup())
Button((100,50),2,"Next","Next",(255,255,255),(0,0,0),(1050,850),fileFinderButtons[1])
fileFinderButtons.append(ButtonGroup())
Button((190,50),2,"Previous","Previous",(255,255,255),(0,0,0),(595,850),fileFinderButtons[2])