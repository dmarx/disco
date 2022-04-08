
# import math


# aVocab = []

# intCat = 0
# intIncr = 0

# # //The data stored is pretty simple.  It works like this:
# # //
# # // The aVocab array has sub arrays that are named lists of data.
# # //
# # //aVocab[intCat]= [] - The aVocab Array actually holds other arrays.
# # //aVocab[intCat][0]="FIRST" - This is the name of the list of data in this sub array.  The name helps the program find the data.
# # //aVocab[intCat][1] = [] - Yep, ANOTHER array - this is the array that holds the actual data.
# # # //intIncr += 1
# # aVocab[intCat][1][intIncr] = "First thing <SECOND>"
# # # // See that <SECOND> tag?  Anything in brackets references another list.
# # # //intIncr += 1
# # aVocab[intCat][1][intIncr] = "First thing <THIRD>"
# # # //
# # # // Unless it's the last entry, don't forget to increment and reset the counters!
# # //
# # //intCat = intCat + 1
# # //intIncr=0


# aVocab[intCat] = []
# aVocab[intCat][0] = "FIRST"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "You stand in a <TerrainDesc> <Area> <stuff>.  <Features>.  <Weather>."

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "TerrainDesc"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "broken"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "flat"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "hilly"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "mountainous"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "Area"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "area"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "region"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "terrain"


# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "stuff"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<ObjPop> <stonedesc> <Stone>. It's also <ObjPop> <plants>"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<ObjPop> <plants>"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<ObjPop> <stonedesc> <Stone>"


# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "Features"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "You can see <BFeatures>"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "You can see <WFeatures>"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "You can see <WFeatures> and <BFeatures>"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "BFeatures"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<Structure> <Distance>"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "WFeatures"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<WaterBody> <Distance>"


# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "stonedesc"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<stone-only>"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<ps-desc>"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "stone-only"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "broken"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "crystalline"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "jagged"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "rough"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "smooth"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "weather-worn"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "worn-down"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "ObjPop"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "abounding with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "covered with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "dotted with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "scattered with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "smattered with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "spotted with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "sprinkled with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "strewn with"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "replete with"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "plants"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<softplant>grass"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<softplant>grass and <softplant>wildflowers"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>shrubs and <softplant>grass"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>trees, <plant-desc>shrubs, and <softplant>grass"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>plants"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>shrubs"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>trees and <softplant>wildflowers"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>trees and <softplant>grass"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<plant-desc>trees, <softplant>grass, and <softplant>wildflowers"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<softplant>wildflowers"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "plant-desc"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<woodplant> "
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<allplant> "
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<ps-desc> "
# intIncr += 1
# aVocab[intCat][1][intIncr] = ""

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "softplant"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<allplant> "
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<ps-desc> "
# intIncr += 1
# aVocab[intCat][1][intIncr] = ""

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "allplant"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "colorful"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "dead"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "foul-smelling"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "pleasant-smelling"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "sharp"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "strange-looking"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "woodplant"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "fruit-bearing"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "prickly"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "thorny"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "deciduous"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "evergreen"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "ps-desc"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "diverse"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "gigantic"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "huge"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "small"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "unusual"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "various"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "Stone"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<stonecolor> rocks"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "<stonecolor> stones"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "stonecolor"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "reddish"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "brown"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "pale brown"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "bluish"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "purplish"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "greenish"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "gray"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "dark"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "pale"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "colorful"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "multicolored"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "WaterBody"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a bog"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a<size> lake"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a marsh"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a small body of water"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "the sea"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "the ocean"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a stream"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a<size> river"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a waterfall"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "size"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = " small"
# intIncr += 1
# aVocab[intCat][1][intIncr] = " large"
# intIncr += 1
# aVocab[intCat][1][intIncr] = " huge"
# intIncr += 1
# aVocab[intCat][1][intIncr] = ""
# intIncr += 1
# aVocab[intCat][1][intIncr] = ""

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "Structure"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a castle"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a cave"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a citadel"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a city"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a fort"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a monastery"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a ruin"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a tower"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a town"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a village"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "Distance"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "to the east"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "to the north"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "to the south"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "to the west"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "close by"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "in the distance"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "on the horizon"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "miles away"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "nearby"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "not too far away"


# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "Weather"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "The temperature is <temp> and the sky is <skyconditions>"


# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "temp"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "cold"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "quite cool"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "cool"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "a little cool"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "somewhat warm"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "warm"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "very warm"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "hot"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "skyconditions"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = "clear"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "mostly clear"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "partially cloudy"
# intIncr += 1
# aVocab[intCat][1][intIncr] = "overcast"

# intCat = intCat + 1
# intIncr = 0
# aVocab[intCat] = []
# aVocab[intCat][0] = "THIRD"
# aVocab[intCat][1] = []
# intIncr += 1
# aVocab[intCat][1][intIncr] = ""


# def GenNumber(nRange):
#     iNumGen = math.round((math.random() * nRange))
#     return iNumGen


# def GetFrom(aArray):
#     sReturn = aArray[GenNumber(aArray.length)]
#     if (sReturn == None):
#         sReturn = GetFrom(aArray)
#     return sReturn


# def GetArray(sArrayName):
#     for intLooper in range(0, aVocab.length):
#         if (aVocab[intLooper][0] == sArrayName):
#             return aVocab[intLooper][1]
#             break


# def ScanLine(sLine):
#     iTagStart, iTagEnd
#     sKey

#     if (sLine.indexOf("<") > -1):
#         iTagStart = sLine.indexOf("<")
#         iTagEnd = sLine.indexOf(">")

#         sKey = sLine.substr(iTagStart+1, iTagEnd-(iTagStart+1))

#         sKey = GetFrom(GetArray(sKey))
#         sLine = sLine.substr(0, iTagStart) + sKey + sLine.substr(iTagEnd+1, (sLine.length - iTagEnd))

#     if (sLine.indexOf("<") > - 1):
#         sLine = ScanLine(sLine)

#     return sLine


# def GenPlot():
#     sLine = GetFrom(GetArray("FIRST"))

#     sLine = ScanLine(sLine)

#     # document.GENFORM.STORY.value = sLine
#     print(sLine)