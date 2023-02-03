data = {0: [{'Speed': 9.891674955786758, 'Sight': 100.89348605861113, 'FOV': 51.76938098651553, 'Food': 496.9748837677128, 'Size': 994.656235591937}, {'Speed': 10.002454943511687, 'Sight': 99.78709906113686, 'FOV': 43.60205631215312, 'Food': 49.112569769316046, 'Size': 98.91119723905382}], 100: [{'Speed': 9.891674955786758, 'Sight': 100.89348605861113, 'FOV': 51.76938098651553, 'Food': 566.6514809421428, 'Size': 994.656235591937}, {'Speed': 10.04030792418633, 'Sight': 99.6510487038765, 'FOV': 43.706768432000025, 'Food': 65.13922446778368, 'Size': 98.8834108964754}], 200: [{'Speed': 9.891674955786758, 'Sight': 100.89348605861113, 'FOV': 51.76938098651553, 'Food': 611.3280781165737, 'Size': 994.656235591937}, {'Speed': 10.038372989702507, 'Sight': 99.80574830511758, 'FOV': 44.33043417575413, 'Food': 64.40974407649911, 'Size': 98.65790118088451}], 300: [{'Speed': 9.891674955786758, 'Sight': 100.89348605861113, 'FOV': 51.76938098651553, 'Food': 651.0046752910046, 'Size': 994.656235591937}, {'Speed': 10.042148104296606, 'Sight': 100.12020534420317, 'FOV': 44.64395966298239, 'Food': 63.71703952228343, 'Size': 98.54398379565193}], 400: [{'Speed': 9.891674955786758, 'Sight': 100.89348605861113, 'FOV': 51.76938098651553, 'Food': 740.6812724654355, 'Size': 994.656235591937}, {'Speed': 10.054685824136005, 'Sight': 100.27796659832593, 'FOV': 45.969101211748864, 'Food': 63.37993791085858, 'Size': 97.87335353222899}]}

animalNum = 0
dataTypes = ["Speed", "Sight", "FOV", "Food", "Size"]

newData = {}
DataScales = {}
for dataName in dataTypes:
    animalsData = []
    allValues = []
    for animalNum in range(2):
        values = []
        for cycle in data:
            value = data[cycle][animalNum][dataName]
            values.append(value)
            allValues.append(value)
        animalsData.append(values)
    newData[dataName] = animalsData
    DataScales[dataName] = max(allValues)



print(newData)
print(DataScales)