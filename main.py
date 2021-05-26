import sys, os
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from PIL import Image

def message(msg):
    print("• " + str(msg))
def failed(msg):
    print("✗ " + str(msg))
    exit()
def success(msg):
    print("✓ " + str(msg))

configur = ConfigParser()
configur.read("config.ini")

metaName    = configur.get('meta', 'name')
metaVersion = configur.get('meta', 'version')
metaAuthor  = configur.get('meta', 'author')
metaLink    = configur.get('meta', 'link')

argAmount = len(sys.argv) - 1
argNeeded = 1
if (argAmount < argNeeded):
    failed("Not enough arguments.")
elif (argAmount > argNeeded):
    failed("Too much arguments.")
file = sys.argv[1]
folder = configur.get('options', 'folder') + '/'

spriteSheet = Image.open("data/" + file + ".png")
xmlTree = ET.parse("data/" + file + ".xml")
xmlRoot = xmlTree.getroot()
xmlFileName = xmlRoot.attrib.get("imagePath").removesuffix(".png")

if (not os.path.exists(folder)):
    try:
        os.mkdir(folder)
    except OSError:
        failed("Couldn't make a directory " + "/" + folder)

print("")
message("Tool started, don't worry! It's in progress!")
message("It may take some time especially for HD sprites.")
print("")

for xml in xmlRoot:
    xmlFrame = xml.attrib

    xmlFrameName = xmlFrame.get("name")
    xmlFrameX = int(xmlFrame.get("x"))
    xmlFrameY = int(xmlFrame.get("y"))
    xmlFrameW = int(xmlFrame.get("width"))
    xmlFrameH = int(xmlFrame.get("height"))

    xmlFrameX2 = xmlFrameX + xmlFrameW
    xmlFrameY2 = xmlFrameY + xmlFrameH
    spriteFrame = spriteSheet
    if (not os.path.exists(folder + xmlFileName)):
        try:
            os.mkdir(folder + xmlFileName)
        except OSError:
            failed("Couldn't make a directory " + "/" + folder + xmlFileName)
    spriteFrame.crop((xmlFrameX, xmlFrameY, xmlFrameX2, xmlFrameY2)).save(folder + xmlFileName + "/" + xmlFrameName + ".png", "PNG")

success("Successfully saved sprite sheet frames at /" + folder + xmlFileName + "/" )
print("")
message("Credits not required, but greatly appriciated!")
message(metaName + " " + metaVersion + " by " + metaAuthor)
message(metaLink)
print("")