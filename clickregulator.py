import pyautogui
from time import sleep
import traceback
import datetime
import os
import pickle
import tempfile
import sys
#import timeit
import logging
#pyautogui.alert("this thing works")
#var = pyautogui.prompt("Type something here")

#logging.info(var)
#i = 0
#while (i < 5):
#    logging.info(pyautogui.position())
#    i += 1
#    time.sleep(2)
#logging.info(pyautogui.size())
#logging.basicConfig(filename='log0.log', level=logging.INFO)
dir = './clickregulator/resources/'
im = pyautogui.screenshot(dir+'screencapture01.png',region=(405,135,1252,740))
explorertimedict = {}
buffcooldownsdict = {}


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

logging.basicConfig(handlers=[logging.StreamHandler(), logging.FileHandler('log0.log')],format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')


def createxplorerdict():
    try:
        with open(os.path.join('data', 'memorydict'), "rb") as fd:
            explorertimedict = pickle.load(fd)
        logging.info("memorydict Loaded Successfully")
    except OSError:
        logging.info("memorydict Not Found - Looking for Backup")
        try:
            with open(os.path.join('data', 'memorydict_backup'), "rb") as fd:
                explorertimedict = pickle.load(fd)
            logging.info("memorydict Backup Loaded Successfully")
        except OSError:
            logging.info("memorydict Backup Not Found - Creating New memorydict")
            explorertimedict = {}
            with open(os.path.join('data', 'memorydict'), "wb") as fd:
                pickle.dump(explorertimedict, fd, -1)
            logging.info("memorydict Created")
    return explorertimedict

def savexplorerdict():
    with tempfile.NamedTemporaryFile('wb', dir=os.path.dirname(os.path.join('data', 'memorydict')), delete=False) as tf:
        pickle.dump(explorertimedict, tf, -1)
        tempname = tf.name
    try:
        os.remove(os.path.join('data', 'memorydict_backup'))
    except OSError as e:
        pass
    try:
        os.rename(os.path.join('data', 'memorydict'), os.path.join('data', 'memorydict_backup'))
    except OSError as e:
        print("unknown error " + e)
    os.rename(tempname, os.path.join('data', 'memorydict'))

explorertimedict = createxplorerdict()

def createbuffcooldownsdict():
    try:
        with open(os.path.join('data', 'buffdict'), "rb") as fd:
            explorertimedict = pickle.load(fd)
        logging.info("buffdict Loaded Successfully")
    except OSError:
        logging.info("buffdict Not Found - Looking for Backup")
        try:
            with open(os.path.join('data', 'buffdict_backup'), "rb") as fd:
                explorertimedict = pickle.load(fd)
            logging.info("buffdict Backup Loaded Successfully")
        except OSError:
            logging.info("buffdict Backup Not Found - Creating New buffdict")
            explorertimedict = {}
            with open(os.path.join('data', 'buffdict'), "wb") as fd:
                pickle.dump(explorertimedict, fd, -1)
            logging.info("buffdict Created")
    return explorertimedict

def savebuffcoolownsdict():
    with tempfile.NamedTemporaryFile('wb', dir=os.path.dirname(os.path.join('data', 'buffdict')), delete=False) as tf:
        pickle.dump(explorertimedict, tf, -1)
        tempname = tf.name
    try:
        os.remove(os.path.join('data', 'buffdict_backup'))
    except OSError as e:
        pass
    try:
        os.rename(os.path.join('data', 'buffdict'), os.path.join('data', 'buffdict_backup'))
    except OSError as e:
        print("unknown error " + e)
    os.rename(tempname, os.path.join('data', 'buffdict'))

buffcooldownsdict = createbuffcooldownsdict()

def refreshchrome():
    clickpicfromfile('chromerefresh.png')
    sleep(20)
    waitforgametoload()

def waitforgametoload():
    while True:
        if verifyimageonscreen('loadscreensoccer0.png'):
            sleep(20)
        if verifyimageonscreen('loadscreensoccer1.png'):
            sleep(10)
        if verifyimageonscreen('moreinfomark.png'):
            clickpicfromfile('advgreencheck.png')
        if verifyimageonscreen('starmenu00.png'):
            clickpicfromfileOnce('starmenu00.png', double=True)
            loopexplchecks(False)
            return
        sleep(10)


def getcollectibleimages(partname):
    filelist = []
    files = os.listdir(dir)
    for filename in files:
        if partname in filename:
            filelist.append(filename)
    return filelist


def allpicsmallwindow(haystackImage, name, valor=None):
    listcoords = []
    needleImage = name
    confidence = 0.99 if valor is None else valor
    try:
        picturelocations = pyautogui.locateAll(needleImage, haystackImage, grayscale=False, confidence=confidence)
        for picturelocation in picturelocations:
            #logging.info(picturelocation)
            picturepoint = pyautogui.center(picturelocation)
            pic_x, pic_y = picturepoint
            pic_x += 405
            pic_y += 135
            listcoords.append([pic_x,pic_y])
            ##logging.info(str(pic_x) + ',' + str(pic_y))
            sleep(0.3)
        return listcoords
    except:
        #logging.info(traceback.print_exc())
        logging.info("there was an error with locating image: " + needleImage)
        return listcoords

def clickpicsmallwindow(haystackImage, name, valor=0.99, double=True):
    needleImage = name
    confidence = valor
    try:
        picturelocation = pyautogui.locate(needleImage, haystackImage, grayscale=False, confidence=confidence)
        if picturelocation == None:
            logging.info("Couldn't locate on screen: " + needleImage)
            return False
        picturepoint = pyautogui.center(picturelocation)
        pic_x, pic_y = picturepoint
        pic_x += 405
        pic_y += 135
        if double is True:
            pyautogui.doubleClick(pic_x, pic_y, interval=0.1)
        else:
            pyautogui.click(pic_x, pic_y)
        #logging.info(str(pic_x) + ',' + str(pic_y))
        logging.info("click successful: " + needleImage)
        sleep(0.3)
        return True
    except:
        logging.info("there was an error with locating image: " + needleImage)
        return False

def movearoundimage(haystackImage, name, valor=None, moveOnce=False):
    needleImage = name
    confidence = 0.99 if valor is None else valor
    try:
        picturelocation = pyautogui.locate(needleImage, haystackImage, grayscale=False, confidence=confidence)
        if picturelocation == None:
            logging.info("Couldn't locate on screen: " + needleImage)
            return False
        picturepoint = pyautogui.center(picturelocation)
        pic_x, pic_y = picturepoint
        pic_x += 405
        pic_y += 135
        if moveOnce is True:
            pyautogui.moveTo(pic_x, pic_y)
        else:
            for i in range(0,2):
                pyautogui.moveTo(pic_x+2, pic_y+2)
                pyautogui.moveTo(pic_x, pic_y)
                pyautogui.moveTo(pic_x-2, pic_y-2)
        #logging.info(str(pic_x) + ',' + str(pic_y))
        logging.info("move around successful: " + needleImage)
        return True
    except:
        logging.info("there was an error with locating image: " + needleImage)
        return False


def clickpicfromfile(name, confidence=0.95, attempts = 7):
    filename = name
    fail = 0
    try:
        while True:
            picturelocation = pyautogui.locateOnScreen(image=dir+filename, minSearchTime=5, confidence=confidence)
            if picturelocation == None:
                logging.info("Couldn't locate on screen: " + filename)
                fail += 1
                if fail > attempts: return False
            else: break

        #logging.info(pos)
        picturepoint = pyautogui.center(picturelocation)
        pic_x, pic_y = picturepoint
        pyautogui.click(pic_x, pic_y)
        #logging.info(str(pic_x) + ',' + str(pic_y))
        logging.info("click successful: " + filename)
        sleep(0.2)
        return True


    except:
        logging.info("there was an error with locating image: " + filename)
        #logging.info(traceback.print_exc())
        return False

def clickpicfromfileOnce(name, confidence=0.85, double=False):
    filename = name
    fail = 0
    try:
        picturelocation = pyautogui.locateOnScreen(image=dir+filename, minSearchTime=2, confidence=confidence)
        if picturelocation == None:
            logging.info("Couldn't locate on screen: " + filename)
            return False

        #logging.info(pos)
        picturepoint = pyautogui.center(picturelocation)
        pic_x, pic_y = picturepoint
        if double:
            pyautogui.doubleClick(pic_x, pic_y, interval=0.2)
        else:
            pyautogui.click(pic_x, pic_y)
        #logging.info(str(pic_x) + ',' + str(pic_y))
        logging.info("click successful: " + filename)
        sleep(0.3)
        return True


    except:
        logging.info("there was an error with locating image: " + filename)
        return False

def doubleclickpicfromfile(name):
    filename = name
    fail = 0
    try:
        while True:
            picturelocation = pyautogui.locateOnScreen(image=dir+filename, minSearchTime=5)
            if picturelocation == None:
                logging.info("Couldn't locate on screen: " + filename)
                fail += 1
                if fail > 7: break
            else: break

        #logging.info(pos)
        picturepoint = pyautogui.center(picturelocation)
        pic_x, pic_y = picturepoint
        pyautogui.doubleClick(pic_x, pic_y, interval=0.1)
        #logging.info(str(pic_x) + ',' + str(pic_y))
        logging.info("click successful: " + filename)
        sleep(0.5)
        return True


    except:
        logging.info("there was an error with locating image: " + filename)
        #logging.info(traceback.print_exc())
        return False
#questcompletelocation = pyautogui.locateAllOnScreen(dir+'savage00.png')
#for pos in questcompletelocation:
#    logging.info(pos)
#questcompletepoint = pyautogui.center(questcompletelocation)
#logging.info(questcompletepoint)
#qc_x, qc_y = questcompletepoint
#pyautogui.click(qc_x, qc_y)

#steps to follow :
# step1 - find picture on screen - if not then loop until found
# step1 - confirm picture on screen & click
# step1 -

def shortTreasureSearchclicks(haystackImage):
    if clickpicfromfile('treasuresearch00.png'):
        movearoundimage(haystackImage, 'specialtab01.png', moveOnce=True)
        if clickpicfromfile('shorttreasure00.png'):
            clickpicfromfile('greencheckexplorer00.png')

def clickPin():
    if clickpicfromfileOnce('pin00.png'):
        logging.info('pin true')
    else:
        pyautogui.click(1318, 361)
        logging.info("click pin defaults")

def findclickfromlist(list):
    fail = 0
    while True:
        for pic in list:
            if (clickpicfromfileOnce(pic)):
                return True
        fail += 1
        if fail > 3: return False


def pinStar():
    clickpicfromfile('starmenu00.png')
    clickpicfromfileOnce('specialtab00.png')
    clickpicfromfile('specialtab01.png')
    clickPin()

def findpicturecoordinates(name):
    filename = name
    fail = 0
    try:
        while True:
            picturelocation = pyautogui.locateOnScreen(image=dir+filename, minSearchTime=5, confidence=0.95)
            if picturelocation == None:
                logging.info("Couldn't locate on screen: " + filename)
                fail += 1
                if fail > 7: return None
            else: break

        #logging.info(pos)
        picturepoint = pyautogui.center(picturelocation)
        pic_x, pic_y = picturepoint
        coords = [pic_x, pic_y]
        #pyautogui.click(pic_x, pic_y)
        #logging.info(str(pic_x) + ',' + str(pic_y))
        logging.info("click successful: " + filename)
        return coords


    except:
        logging.info("there was an error with locating image: " + filename)
        #logging.info(traceback.print_exc())
        return None

def checkexplorereturns(explorerlist, explorerimage, stringtype):
    if not verifyimageonscreen('starmenu00.png'):
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        clickpicfromfileOnce('chromealttab00.png')
        pyautogui.keyUp('alt')
    if not verifyimageonscreen('ecoverview.png'):
        clickpicfromfileOnce('downarrowstar.png')
        clickpicfromfileOnce('returnhomebar.png')
        awaitmapload()
        clickpicfromfileOnce('uparrowstar.png')
    check = False
    pinStar()
    textbarcoords = findpicturecoordinates('textbar00.png')
    if textbarcoords is not None:
        pyautogui.click(textbarcoords[0],textbarcoords[1])
        pyautogui.typewrite(stringtype)
        sleep(0.5)
        check = verifyimageonscreen(explorerimage)
        if check:
            logging.info(print("launching " + explorerimage))
            executeSearch(explorerlist)
            sleep(3)
            for image in explorerlist:
                if verifyimageonscreen(image):
                    executeSearch(explorerlist)
            explorertimedict[explorerimage] = datetime.datetime.now()
            savexplorerdict()
        else:
            logging.info(print(explorerimage + " not returned yet"))
        pyautogui.doubleClick(textbarcoords[0], textbarcoords[1],interval=0.1)
        pyautogui.press('delete')
    clickpicfromfileOnce('starmenu00.png')
    return check

def investigatestarmenu(image,string):
    check = False
    if clickpicfromfileOnce('starmenu00.png'):
        clickpicfromfileOnce('alltab00.png')
        clickpicfromfileOnce('alltab01.png')
    textbarcoords = findpicturecoordinates('textbar00.png')
    if textbarcoords is not None:
        pyautogui.click(textbarcoords[0],textbarcoords[1])
        pyautogui.typewrite(string)
        sleep(0.5)
        check = verifyimageonscreen(image, 0.85)
        pyautogui.doubleClick(textbarcoords[0], textbarcoords[1], interval=0.1)
        pyautogui.press('delete')
    clickpicfromfileOnce('starmenu00.png')
    return check


def startAdv(advname):
    filename = advname + '.png'
    fail = 0
    while True:
        if verifyimageonscreen(advname + 'map.png'):
            logging.info('adventure already open')
            return
        openstarbuffstab()
        if clickpicfromfile('advtab.png'):
            logging.info('adv tab open')
        else:
            clickpicfromfile('advtab2.png')
        textbarcoords = findpicturecoordinates('textbar00.png')
        if textbarcoords is not None:
            pyautogui.doubleClick(textbarcoords[0],textbarcoords[1])
            pyautogui.typewrite(advname)
            if clickpicfromfile(filename):
                pass
            if verifyimageonscreen('rotmheader.png'):
                if verifyimageonscreen('advgreencheck.png'):
                    clickpicfromfile('advgreencheck.png')
                    clickpicfromfile('greencheckexplorer00.png')
                    clickpicfromfileOnce('starmenu00.png')
                    if verifyimageonscreen(filename):
                        pyautogui.doubleClick(textbarcoords[0],textbarcoords[1], interval=0.1)
                        pyautogui.press('delete')
                    sleep(6)
                else:
                    clickpicfromfile('advcancel.png')
                    continue
        else: continue
        fail += 1
        if fail % 10 == 9:
            failsafe(True)

def createProvBuff(name, amount=1):
    try:
        quantity = amount
        clickpicfromfile(name)
        if quantity != 1:
            pyautogui.typewrite(quantity)
        if clickpicfromfile('greencheckexplorer00.png'):
            logging.info("Buff " + name + " created successfully!")
            return True
    except:
        logging.info("unsuccessful creating buff " + name)
        return False

def tryUntilTrue(methodToRun, param1, *param2):
    while True:
        check = methodToRun(param1, *param2)
        if check is True:
            return

def openprovisionhouseriches():
    while True:
        clickpicfromfileOnce('ecoverview.png')
        pyautogui.press('p')
        clickpicfromfileOnce('richesprovtab.png', double=True)
        if verifyimageonscreen('richesprovtabconfirm.png'):
            clickpicfromfileOnce('richesprovtabconfirm.png', double=True)
            return
        else: continue

def makestartBuffsRiches(): # need to edit
    fail = 0
    awaitadvstart('riches')
    while True:
        openprovisionhouseriches()
        if verifyimageonscreen('provmenu.png'):
            tryUntilTrue(createProvBuff,'tavern.png')
            tryUntilTrue(createProvBuff,'shovel.png', '2')
            tryUntilTrue(createProvBuff,'storage.png')
            tryUntilTrue(createProvBuff,'mason.png', '3')
            break
        else:
            fail += 1
            if fail % 10 == 9:
                failsafe(home=True)
            continue

def makefirstvisitbuffsRiches():
    while True:
        openprovisionhouseriches()
        if verifyimageonscreen('provmenu.png'):
            tryUntilTrue(createProvBuff,'pureore.png')
            tryUntilTrue(createProvBuff,'dynamite.png', '4')
            tryUntilTrue(createProvBuff,'dynpack.png', '5')
            tryUntilTrue(createProvBuff,'glue.png', '10')
            tryUntilTrue(createProvBuff,'special.png', '2')
            tryUntilTrue(createProvBuff,'food.png', '2')
            tryUntilTrue(createProvBuff,'explo.png')
            break
        else: continue
    loopexplchecks(False)
    awaitbuffproductioncomplete('dynpackstar.png',30)

def makesecondvisitbuffsRiches():
    openprovisionhouseriches()
    tryUntilTrue(createProvBuff,'shaft.png')
    awaitbuffproductioncomplete('shaft1.png',12)

def dropbuff(firstselect, secondselect, pause=3, amount=1, star=False):
    fail = 0
    while True:
        haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
        if star:
            openstarbuffstab()
        if clickpicsmallwindow(haystackImage, firstselect):
            if verifyimageonscreen(secondselect):
                clickpicfromfileOnce(secondselect, double=True)
                    #if not investigatestarmenu(firstselect, firstselect[4:7]):
                break
        else:
            if verifyimageonscreen('starcancel.png'):
                clickpicfromfileOnce('starcancel.png')
            else:
                clickpicfromfileOnce('starmenu00.png')
            return False
        fail += 1
        if fail % 10 == 9:
            failsafe()
    sleep(pause)


def verifybuffmovecomplete(moveselect, secondselect):
    if verifyimageonscreen(moveselect, 0.85):
        return False
    if investigatestarmenu(secondselect, secondselect[0:3]):
        return False
    else: return True


def dropbuffmove(moveselect, secondselect, firstselect, movearoundconfidence=0.95): #second select is starmenu buff
    fail = 0
    while True:
        clickonmap()
        movehaystack = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
        movearoundimage(movehaystack, moveselect, movearoundconfidence)
        haystackImage = pyautogui.screenshot(dir + 'screencapture02.png', region=(405, 135, 1252, 740))
        if verifyimageonscreen(firstselect, 0.75):
            clickpicsmallwindow(haystackImage, firstselect, 0.75)
            sleep(0.1)
            for i in range(0,7):
                if verifyimageonscreen(secondselect, 0.75):
                    if clickpicfromfile(secondselect, 0.75):
                        sleep(0.1)
                        return True
        fail += 1
        print("failed " + str(fail))
        if fail > 1:
            return False
        if fail % 10 == 9:
            failsafe()


def visitMap(mapname):
    check = False
    fail = 0
    while True:
        clickpicfromfile(mapname + 'map.png')
        if verifyimageonscreen('visitselect.png'):
            clickpicfromfile('visitselect.png')
            if awaitmapload():
                return True
        elif verifyimageonscreen('returnhomeselect.png'):
            return False
        else:
            clickpicfromfileOnce('starmenu00.png', double=True)
            fail += 1
            if fail % 10 == 9:
                failsafe()
            continue


def returnHome(mapname):
    clickpicfromfile(mapname + 'map.png')
    clickpicfromfile('returnhomeselect.png')
    awaitmapload()

def collectiblehunt():
    while True:
        if verifyimageonscreen('pirateship0.png'):
            if findAllCollectibles():
                return
            else:
                returnHome('riches')
                loopexplchecks(False)
                visitMap('riches')
        elif verifyimageonscreen('ecoverview.png'):
            visitMap('riches')
        else: failsafe()


def findAllCollectibles():
    fail = 0
    pinksquares = getcollectibleimages('pinksquare')
    mainsquares = getcollectibleimages('mainsquare')
    clickonmap()
    gatheredlocations = []
    mainlocations = []
    while True:
        haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
        if clickpicsmallwindow(haystackImage, 'questcomplete00.png', 0.95, double=False):
            break
        if clickpicsmallwindow(haystackImage, 'questcomplete01.png', 0.95, double=False):
            break
        clickpicsmallwindow(haystackImage, 'closequestbook.png')
        if fail % 2 == 0:
            for main in mainsquares:
                mainsquarelocations = allpicsmallwindow(haystackImage, main)
                logging.info(main + ' found ' + str(len(mainsquarelocations)))
                if len(mainsquarelocations) > 0:
                    mainlocations.append(mainsquarelocations)
            logging.info(mainlocations)
            for lists in mainlocations:
                for coords in lists:
                    pyautogui.click(coords[0],coords[1])
        if fail % 2 == 1:
            for pink in pinksquares:
                #clickpicsmallwindow(haystackImage, pink)
                pinksquarelocations = allpicsmallwindow(haystackImage, pink)
                logging.info(pink + ' found ' + str(len(pinksquarelocations)))
                if len(pinksquarelocations) > 0:
                    gatheredlocations.append(pinksquarelocations)
            logging.info(gatheredlocations)
            for lists in gatheredlocations:
                for coords in lists:
                    pyautogui.click(coords[0],coords[1])
        if fail % 4 == 3:
            if openstarbuffstab():
                clickpicfromfileOnce('fairydust.png')
                clickpicfromfileOnce('advgreencheck.png')
                sleep(6)
        fail += 1
        if fail == 10:
            return False
        clickpicfromfileOnce('openquestbook.png')
        if clickpicfromfileOnce('collectionquest.png'):
            if clickpicfromfileOnce('advgreencheck.png'):
                break
        if clickpicfromfileOnce('collectionquest1.png'):
            if clickpicfromfileOnce('advgreencheck.png'):
                break
        clickpicfromfile('closequestbook.png')
    clickpicfromfileOnce('collectionquest1.png')
    clickpicfromfileOnce('collectionquest.png')
    clickpicfromfileOnce('advgreencheck.png')
    clickpicfromfile('closequestbook.png')
    return True

def clickeverywhere():
    logging.info("come back to this function later")

class RichesAdv():
    def __init__(self):
        self.name = 'riches'
        self.mainQuest = False
        self.purityquest = False
        self.areaquest = False
        self.miningquest = False
        self.collect1 = False
        self.collect2 = False
        self.collect3 = False
        self.foodquest = False
        self.shaftquest = False
        self.sabotagequest = False
        self.startupbuffs = False
        self.firstvisitbuffs = False
        self.secondvisitbuffs = False

def dropbuffrichesnostarfirstvisit(): #remove looping when fail
    fail = 0
    haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
    while True:
        if verifyimageonscreen('shovelmapselect.png'):
            dropbuffmove('shovelmapselect.png', 'shovelbuffselect.png', 'shovelmoveselect.png', 0.85)
        elif verifyimageonscreen('shovelmapselect3.png'):
            dropbuffmove('shovelmapselect3.png', 'shovelbuffselect.png', 'shovelmoveselect.png', 0.85)
        if verifyimageonscreen('shovelmapselect2.png'):
            dropbuffmove('shovelmapselect2.png', 'shovelbuffselect.png', 'shovelmoveselect.png', 0.85)
        elif verifyimageonscreen('shovelmapselect4.png'):
            dropbuffmove('shovelmapselect4.png', 'shovelbuffselect.png', 'shovelmoveselect.png', 0.85)
        dropbuffmove('dynamitemapselect.png', 'dynamitebuffselect.png', 'dynamitemoveselect.png')
        dropbuffmove('dynamitemapselect2.png', 'dynamitebuffselect.png', 'dynamitemoveselect.png')
        dropbuffmove('dynamitemapselect3.png', 'dynamitebuffselect.png', 'dynamitemoveselect.png')
        #dropbuffmove('dynamitemapselect5.png', 'dynamitebuffselect.png', 'dynamitemoveselect.png')
        dropbuffmove('dynamitemapselect4.png', 'dynamitebuffselect.png', 'dynamitemoveselect.png')
        sleep(6)
        clickpicfromfileOnce('openquestbook.png')
        if verifyimageonscreen('areaquest.png') or verifyimageonscreen('areaquest1.png'):
            if hitcomplete('areaquest.png'):
                break
            elif hitcomplete('areaquest1.png'):
                break
            else:
                clickpicfromfileOnce('closequestbook.png')
                continue
        fail += 1
        if fail == 10:
            failsafe()
    clickpicfromfileOnce('closequestbook.png')


def test():
    dynpack = 'dynpackbuffselect.png'
    if investigatestarmenu(dynpack, dynpack[0:3]):
        print("in star")
        return False

def dropbuffsfromrichesnostarsecondvisit():
    #haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
    fail = 0
    while True:
        dropbuffmove('dynpackmountainselect.png', 'dynpackbuffselect.png', 'dynpackmapselect.png')
        dropbuffmove('sabotagemapselect.png', 'gluebuffselect.png', 'gluemapselect.png')
        dropbuffmove('sabotagemapselect.png', 'specialbuffselect.png', 'specialmapselect.png')
        dropbuffmove('sabotagemapselect.png', 'explobuffselect.png', 'explomapselect.png')
        dropbuffmove('sabotagemapselect.png', 'specialbuffselect2.png', 'specialmapselect2.png')
        if verifyimageonscreen('dynpackmountainselect.png'):
            continue
        sleep(6)
        if verifyimageonscreen('sabotagemapselect.png'):
            continue
        if verifyimageonscreen('nosabotagebuilding.png'):
            break
        fail += 1
        if fail == 10:
            failsafe()


def openstarbuffstab():
    if (clickpicfromfile('starmenu00.png')):
        if clickpicfromfileOnce('starbufftab00.png'):
            return True
        elif clickpicfromfileOnce('starbufftab01.png'):
            return True


def droppuritybuff():
    fail = 0
    while True:
        if openstarbuffstab():
            dropbuff('pureorestar.png', 'shipselectmap1.png')
        clickpicfromfileOnce('openquestbook.png')
        if verifyimageonscreen('mainquesthide.png', 0.93):
            clickpicfromfileOnce('mainquesthide.png', 0.93)
        if verifyimageonscreen('purityquest.png'):
            if hitcomplete('purityquest.png'):
                break
        elif verifyimageonscreen('purityquest1.png'):
            if hitcomplete('purityquest1.png'):
                break
        else:
            clickpicfromfileOnce('closequestbook.png')
            continue
        fail +=1
        if fail == 10:
            failsafe()
    clickpicfromfileOnce('closequestbook.png')
    return True

def dropconstructionbuffs():
    fail = 0
    buffstodrop = []
    buffstodrop.append(['storagestar.png','groundselect3.png'])
    buffstodrop.append(['tavernstar.png','groundselect4.png'])
    buffstodrop.append(['masonstar.png','groundselect4.png'])
    buffstodrop.append(['masonstar.png','groundselect4.png'])
    while True:
        clickpicfromfileOnce('closequestbook.png')
        for item in buffstodrop:
            if openstarbuffstab():
                logging.info(dropbuff(item[0],item[1]))
        sleep(5)
        clickpicfromfileOnce('openquestbook.png')
        if verifyimageonscreen('mainquesthide.png', 0.93):
            clickpicfromfileOnce('mainquesthide.png',0.93)
        if verifyimageonscreen('miningquest.png'):
            if hitcomplete('miningquest.png'):
                break
        elif verifyimageonscreen('miningquest1.png'):
            if hitcomplete('miningquest1.png'):
                break
        else:
            continue
        fail +=1
        if fail == 10:
            failsafe()
    clickpicfromfileOnce('closequestbook.png')



def dropbuffrichesfromstarfirstvisit():#deprecated
    buffstodrop = []
    buffstodrop.append(['pureorestar.png', 'shipselectmap1.png'])
    buffstodrop.append(['storagestar.png','groundselect3.png'])
    buffstodrop.append(['tavernstar.png','groundselect4.png',10])
    buffstodrop.append(['masonstar.png','groundselect4.png',10])
    buffstodrop.append(['masonstar.png','groundselect4.png',10])
    #buffstodrop.append(['buildmasonstar.png','groundselect4.png',10])
    for item in buffstodrop:
        if openstarbuffstab():
            logging.info('staropen')
            if len(item) < 3:
                logging.info(dropbuff(item[0],item[1]))
            else: logging.info(dropbuff(item[0],item[1],item[2]))

def dropbuffrichesfromstarsecondvisit():
    fail = 0
    while True:
        clickpicfromfileOnce('closequestbook.png')
        if openstarbuffstab():
            dropbuff('shaftstar.png', 'shaftselection.png')
        clickpicfromfileOnce('openquestbook.png')
        sleep(5)
        if verifyimageonscreen('mainquesthide.png', 0.93):
            clickpicfromfileOnce('mainquesthide.png',0.93)
        if verifyimageonscreen('shaftquest.png'):
            if hitcomplete('shaftquest.png'):
                break
        elif verifyimageonscreen('shaftquest1.png'):
            if hitcomplete('shaftquest1.png'):
                break
        else:
            continue
        fail += 1
        if fail == 10:
            failsafe()
    clickpicfromfileOnce('closequestbook.png')


#buffstodrop = []
    #buffstodrop.append(['shaftstar.png', 'shaftselection.png'])
    #for item in buffstodrop:
    #    if openstarbuffstab():
    #        logging.info('staropen')
    #        if len(item) < 3:
    #            logging.info(dropbuff(item[0],item[1]))
    #        else: logging.info(dropbuff(item[0],item[1],item[2]))

def dropbuffrichesfoodquest():
    logging.info('starting Food drops')
    fail = 0
    buffstodrop = []
    buffstodrop.append(['foodstar.png', 'tavernmapselect.png',10])
    buffstodrop.append(['foodstar.png', 'masonmapselect.png',2])
    haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
    while True:
        if clickpicfromfile('openquestbook.png'):
            if verifyimageonscreen('mainquesthide.png', 0.93):
                clickpicfromfileOnce('mainquesthide.png',0.93)
            if verifyimageonscreen('cateringquestverify.png', 0.75) or verifyimageonscreen('cateringquestverify1.png', 0.75) or verifyimageonscreen('cateringquestverify3.png', 0.75):
                clickpicfromfile('closequestbook.png')
                for item in buffstodrop:
                    if openstarbuffstab():
                        logging.info('staropen')
                        if len(item) < 3:
                            logging.info(dropbuff(item[0], item[1]))
                        elif len(item) < 4:
                            logging.info(dropbuff(item[0], item[1], item[2]))
                        else:
                            logging.info(dropbuff(item[0], item[1], item[2], item[3]))
        if checksinglequeststatus('food'):
            sleep(3)
            return
        fail += 1
        if fail % 15 == 14:
            failsafe()



def verifyimageonscreen(imagename, confidence=0.85, grayscale=False):
    haystackImage = pyautogui.screenshot(dir + 'screencapture03.png', region=(405, 135, 1252, 740))
    picturelocation = pyautogui.locate(imagename, haystackImage, grayscale=grayscale, confidence=confidence)
    if picturelocation == None:
        logging.info("Couldn't locate on screen: " + imagename)
        return False
    else:
        logging.info('found ' +imagename)
        return True

def hitcomplete(questname):
    haystackImage = pyautogui.screenshot(dir + 'screencapture03.png', region=(405, 135, 1252, 740))
    clickpicsmallwindow(haystackImage, questname, 0.90)
    if verifyimageonscreen('advgreencheck.png'):
        if clickpicfromfile('advgreencheck.png', attempts=3):
            return True
    else: return False

def checksinglequeststatus(questname):
    check = False
    questnamefile = questname+'quest.png'
    questnamefile2 = questname+'quest1.png'
    haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
    if (clickpicsmallwindow(haystackImage, 'openquestbook.png')):
        if verifyimageonscreen(questnamefile):
            if hitcomplete(questnamefile):
                check = True
        else:
            if os.path.isfile(questnamefile2):
                if verifyimageonscreen(questnamefile2):
                    if hitcomplete(questnamefile2):
                        check = True
    if verifyimageonscreen('greencheckexplorer00.png'):
        check = clickpicfromfile('greencheckexplorer00.png')
        sleep(6)
    if verifyimageonscreen('advfinishreturn.png'):
        clickpicfromfile('advfinishreturn.png')
        return check
    clickpicfromfile('closequestbook.png')
    return check

def checkqueststatusfirstvisit():#deprecated
    Riches = RichesAdv()
    haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
    if (clickpicsmallwindow(haystackImage, 'openquestbook.png')):
        if verifyimageonscreen('mainquesthide.png',0.93):
            clickpicfromfileOnce('mainquesthide.png',0.93)
        if verifyimageonscreen('purityquest.png'):
            if hitcomplete('purityquest.png'):
                Riches.purityquest= True
            else:
                Riches.purityquest = droppuritybuff()
        if verifyimageonscreen('areaquest.png'):
            Riches.areaquest = True
            hitcomplete('areaquest.png')
        if verifyimageonscreen('miningquest.png'):
            Riches.miningquest = True
            hitcomplete('miningquest.png')
    clickpicfromfile('closequestbook.png')
    if Riches.areaquest is True and Riches.miningquest is True and Riches.purityquest is True:
        return True

def adjustMap():
    clickonmap()
    pyautogui.press(['-'], 10)
    pyautogui.keyDown('left')
    sleep(1.1)
    pyautogui.keyUp('left')
    pyautogui.keyDown('up')
    sleep(0.9)
    pyautogui.keyUp('up')
    sleep(2)
    if verifyimageonscreen('topright.png') and verifyimageonscreen('bottomleft.png'):
        return
    else:
        resetmap()
        adjustfromreset()

def adjustfromreset():
    clickonmap()
    pyautogui.press(['-'], 10)
    pyautogui.keyDown('left')
    sleep(4.8)
    pyautogui.keyUp('left')
    pyautogui.keyDown('up')
    sleep(2.5)
    pyautogui.keyUp('up')
    sleep(2)

def resetmap():
    clickonmap()
    pyautogui.press(['-'], 8)
    pyautogui.keyDown('right')
    sleep(8)
    pyautogui.keyUp('right')
    pyautogui.keyDown('down')
    sleep(8)
    pyautogui.keyUp('down')

def awaitadvstart(advname):
    mapname = advname+'map.png'
    while True:
        sleep(2)
        if verifyimageonscreen(mapname):
            return
        else: sleep(2)

def awaitbuffproductioncomplete(imagename, pause):
    string = imagename[0:3]
    while True:
        sleep(pause)
        if investigatestarmenu(imagename, string):
            return


def awaitmapload():
    fail = 0
    while True:
        sleep(2)
        if verifyimageonscreen('mapload.png'):
            sleep(5)
        else: return True
        fail += 1
        if fail == 20:
            refreshchrome()
            return False

def clickonmap():
    if clickpicfromfileOnce('openquestbook.png'):
        clickpicfromfileOnce('closequestbook.png')
        clickpicfromfileOnce('skeleton.png')
        return
    elif clickpicfromfileOnce('shaftselection.png', double=True):
        return
    elif clickpicfromfileOnce('masonmapselect.png', double=True):
        return
    elif clickpicfromfileOnce('skeleton.png', double=True):
        return
    else : clickpicfromfileOnce('starmenu00.png', double=True)

def loopexplchecks(loop=True):
    savages = ['courage00.png', 'experienced00.png', 'intrepid00.png', 'lovely00.png', 'savage00.png']
    savagesstring = 'age|peri|repi|love'
    advent = ['advent00.png']
    adventstring = 'advent'
    luckystring = 'lucky|zoe'
    luckies = ['lucky00.png', 'zoe00.png']
    explorerstring = 'expl'
    explorers = ['candid00.png','explorer00.png']


    while True:
        if explorertimechecks('advent00.png'):
            checkexplorereturns(advent, 'advent00.png', adventstring)
        if explorertimechecks('lucky00.png'):
            checkexplorereturns(luckies, 'lucky00.png', luckystring)
        if explorertimechecks('explorer00.png'):
            checkexplorereturns(explorers, 'explorer00.png', explorerstring)
        if explorertimechecks('savage00.png'):
            checkexplorereturns(savages, 'savage00.png', savagesstring)
        if not loop:
            return
        sleep(60)

#startAdv('riches')
#makestartBuffsRiches()
#visitMap('riches')
#adjustMap() # need more involvement here - worked 1/2 times


#findAllCollectibles()
#returnHome('riches')
#makefirstvisitbuffsRiches()
#visitMap('riches')
#dropbuffrichesnostarfirstvisit()
#dropbuffrichesfromstarfirstvisit()

#if checkqueststatusfirstvisit():
#    phase2 = True
#if False:
#findAllCollectibles()
#returnHome('riches')
#makesecondvisitbuffsRiches()
#visitMap('riches')
#dropbuffsfromrichesnostarsecondvisit() # -needs work


#dropbuffrichesfromstarsecondvisit()
#checksinglequeststatus('shaft')
#dropbuffrichesfoodquest()
#checksinglequeststatus('food')
#findAllCollectibles()
#checksinglequeststatus('richesfinal')


#make definition for placing remaining final buffs


def runRichesLoop():
    count = 0
    fail = 0
    while True:
        if verifyimageonscreen('advfinishreturn.png'):
            clickpicfromfile('advfinishreturn.png')
            awaitmapload()
        if not verifyimageonscreen('advfinishreturn.png'):
            if verifyimageonscreen('ecoverview.png'):
                if not verifyimageonscreen('richesmap.png'):
                    runRiches()
                    count +=1
                    logging.info(str(count) + ' completed')
                    if count % 4 == 0:
                        refreshchrome()
        fail +=1
        if fail > 20:
            refreshchrome()


def runRiches():
    phase2 = False
    loopexplchecks(False)
    startAdv('riches')
    makestartBuffsRiches()
    visitMap('riches')
    adjustMap() # need more involvement here - worked 1/2 times

    collectiblehunt()
    returnHome('riches')
    makefirstvisitbuffsRiches()
    visitMap('riches')
    droppuritybuff()
    dropbuffrichesnostarfirstvisit()
    dropconstructionbuffs()

    #checkqueststatusfirstvisit()

    collectiblehunt()
    returnHome('riches')
    makesecondvisitbuffsRiches()
    loopexplchecks(False)
    visitMap('riches')
    dropbuffsfromrichesnostarsecondvisit()  # -needs work

    dropbuffrichesfromstarsecondvisit()

    dropbuffrichesfoodquest()
    collectiblehunt()
    checksinglequeststatus('sabotage')
    checksinglequeststatus('richesfinal')
    awaitmapload()




#--------------------------------------------------

#while True:
 #   verifyimageonscreen('specialbuffselect.png')
  #  sleep(2)
#while True:
    #logging.info(pyautogui.position())
    #sleep(3)
    #movearoundimage(im, 'mountainselect.png')
    #clickpicfromfileOnce('groundselect3.png')
    #clickpicfromfileOnce('groundselect4.png')

def executeSearch(explorerlist):
    haystackImage = pyautogui.screenshot(dir + 'screencapture01.png', region=(405, 135, 1252, 740))
    gatheredlocations = []
    for explorer in explorerlist:
        explorerlocations = allpicsmallwindow(haystackImage, explorer)
        if len(explorerlocations) > 0:
            gatheredlocations.append(explorerlocations)

    logging.info(gatheredlocations)
    for lists in gatheredlocations:
        for coords in lists:
            pyautogui.click(coords[0],coords[1])
            movearoundimage(haystackImage,'specialtab01.png', moveOnce=True)
            shortTreasureSearchclicks(haystackImage)

    #logging.info(gatherlocations)


#executeSavageSearch()
#runRichesLoop()
#runRiches()
#loopexplchecks(500)




#logging.info(timeit.timeit(stmt = explorerSearch(),number = 10000))


# notes - loop for pink collectibles, in loop check if quest exists, continue to next step

def explorertimechecks(explorerimage):
    explorercooldownspremfriend = {"test00.png":10,"savage00.png":111,"lucky00.png":74,"advent00.png":55,"explorer00.png":222}
    explorercooldowns = {"test00.png":10,"savage00.png":139,"lucky00.png":94,"advent00.png":69,"explorer00.png":279}
    time_now = datetime.datetime.now()
    if explorerimage in explorertimedict.keys():
        time_last_sent = explorertimedict[explorerimage]
    else: return True
    time_cooldown = time_last_sent - datetime.timedelta(minutes=-explorercooldowns[explorerimage], seconds=-43)
    savexplorerdict()
    if (time_now > time_cooldown):
        return True
    else: return False


def incompletequestinvestigation():
    return

def failsafe(home=False):
    if verifyimageonscreen('playnow.png'):
        clickpicfromfile('playnow.png')
        waitforgametoload()
    else:
        refreshchrome()
    failsafeislandadjust(home)
    sleep(20)

def failsafeislandadjust(home=False):
    visitMap('riches')
    resetmap()
    adjustfromreset()
    if home is True:
        returnHome('riches')

def adjustislandformarket():
    pyautogui.press(['-'],20)
    pyautogui.press(['2'],1)
    sleep(0.5)
    pyautogui.press(['+'],4)


def activatexmasmarket():
    time_now = datetime.datetime.now()

    if verifyimageonscreen('avatar.png'):
        if verifyimageonscreen('ecoverview.png'):
            clickpicfromfileOnce('avatar.png')
            adjustislandformarket()
            sleep(0.5)
    if verifyimageonscreen('elitestable.png'):
        clickpicfromfileOnce('elitestable.png', double=True)
        sleep(0.5)
        if verifyimageonscreen('xmasactive.png'):
            print("elite stable on screen & buff active")
        elif verifyimageonscreen('xmasmarketselect.png'):
            clickpicfromfileOnce('xmasmarketselect.png', double=True)
            if verifyimageonscreen('xmas4.png'):
                clickpicfromfileOnce('xmas4.png')
                if verifyimageonscreen('xmas4selected.png'):
                    if verifyimageonscreen('xmasgreencheck.png'):
                        clickpicfromfileOnce('xmasgreencheck.png')
