
nameDic= {"a":1,"b":2,"c":3,"d":4,"e":5}
quantity = 2
page = 1

buttonList = [[]]
for name in nameDic:
    if len(buttonList[-1]) < quantity:
        buttonList[-1].append([name,nameDic[name]])

    else:
        buttonList.append([[name,nameDic[name]]])

print(buttonList)

buttonText = {}
numText = {}
for i in range(len(buttonList[page])):
    buttonText[i] = buttonList[page][i][0]
    numText[i] = str(buttonList[page][i][1])
for j in range(i+1 ,quantity):
    buttonText[j] = ""
    numText[j] = ""
amountOfPages = len(buttonList)-1
# change the button text to match
print(buttonText, " - Buttion")
print(numText, " - Num")
