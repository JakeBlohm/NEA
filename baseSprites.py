from baseClasses import ButtonGroup, Button, Text, DefaultGroup
# These sprites are used to create classes

textEditorButtons = ButtonGroup()
Button((100,25),1,"Cancel","Cancel",(255,255,255),(0,0,0),(700,500),textEditorButtons)
Button((100,25),1,"Confirm","Confirm",(255,255,255),(0,0,0),(900,500),textEditorButtons)
confirmButtons = ButtonGroup()
Button((100,25),1,"Cancel","Cancel",(255,255,255),(0,0,0),(700,500),confirmButtons)
Button((100,25),1,"Confirm","Confirm",(255,255,255),(0,0,0),(900,500),confirmButtons)
confirmDefault = DefaultGroup()
Text(2,"TEXT",(0,0,0),(800,450),confirmDefault,(475,50),(255,255,255),name="Text")

