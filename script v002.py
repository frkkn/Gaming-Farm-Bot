import pyautogui
import pydirectinput
from time import sleep,time
from os import listdir
import math
from multiprocessing import Process
from PIL import Image
import pytesseract
import re
import numpy
import cv2
import threading
from queue import Queue
import mss
from win32gui import GetWindowText, GetForegroundWindow

from nokta import Nokta

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
path = "c:\\users\\faruk\\desktop\\ko-python-bot\\"

karakter_loc = pyautogui.Point(10,10)
ref_loc = pyautogui.Point(10,10)
can = 100
mana = 100
canavar_secili = False
atak_yapiliyor = False
atak_ara_ver = False
oyun_acik = False
canavar_ad = "cardinal"
skiller = {}
konum = Nokta()

def town_at():
    pydirectinput.press("enter")
    pyautogui.write("/town")
    pydirectinput.press("enter")

def can_bul():
    global can
    
    baslangic=(ref_loc.x-42,ref_loc.y+61)
    bitis=(ref_loc.x+148,ref_loc.y+61)

    ss = pyautogui.screenshot(region=(ref_loc.x-33,ref_loc.y+61, 191, 1))
    
    imlec = bitis

    yuzde = 100
    for i in range(ss.width-1,-1,-1):
        if ss.getpixel((i,0)) != (0,0,0):
            break
        yuzde = yuzde - (100/191)

    can = yuzde
    
def can_bul_t(events):
    while not events['exit_event'].is_set():
        can_bul()
        sleep(2)

def can_ic_t(events):
    while not events['exit_event'].is_set():
        if can <= 60:
            #events['can_event'].set()
            pydirectinput.press("1")
            #sleep(2)
            #events['can_event'].clear()
    

def mana_bul():
    global mana
    
    baslangic=(ref_loc.x-42,ref_loc.y+65)
    bitis=(ref_loc.x+148,ref_loc.y+65)

    ss = pyautogui.screenshot(region=(ref_loc.x-33,ref_loc.y+65, 191, 1))
    
    imlec = bitis
    
    yuzde = 100
    for i in range(ss.width-1,-1,-1):
        if ss.getpixel((i,0)) != (0,0,0):
            break
        yuzde = yuzde - (100/191)

    mana = yuzde

def mana_bul_t(events):
    while not events['exit_event'].is_set():
        mana_bul()
        sleep(2)
        
def canavar_bul_t(events):
    global canavar_secili
    
    isim_reg = (ref_loc.x+415,ref_loc.y+27,56, 10)
    isim_reg2 = (ref_loc.x+418,ref_loc.y+77,54, 8)
    conf = 0.5

    while not events['exit_event'].is_set():            
        canavar_secili_tmp = canavar_secili
        canavar_secili = pyautogui.locateOnScreen(path+canavar_ad+".png", confidence=conf, region=isim_reg) is not None
        if canavar_secili_tmp is False and canavar_secili is True:
            events['canavar_secildi_event'].set()
            
    canavar_secili = False
        
def canavar_secili_mi_t(events):
    while not events['exit_event'].is_set():
        if canavar_secili is False:
            pydirectinput.press("z")

def canavar_can_t(events):
	while not events['exit_event'].is_set():
		can_sifir = True
		if can_sifir:
			pydirectinput.press("z", presses=5, interval=0.03)
         
def mana_ic_t(events):
    while not events['exit_event'].is_set():
        if mana <= 40:
            pydirectinput.press("4")            

def atak_t(events):
    while not events['exit_event'].is_set():
        while canavar_secili is True: # and not events['can_event'].is_set():
            if events['canavar_secildi_event'].is_set():
                pydirectinput.press("r")
                events['canavar_secildi_event'].clear()
            pydirectinput.press("3", presses=3, interval=0.05)

def exit_t(events):
    while not events['exit_event'].is_set():
        f = open(path+"exit.txt", "r")
        if f.read() == '1':
            events['exit_event'].set()
        f.close()
        sleep(2)

def odaklan():
    global ref_loc
    
    ref_box = pyautogui.locateOnScreen(path+"ko_yazi.png",confidence=0.8)
    if ref_box is not None:
        ref_loc = pyautogui.center(ref_box)
        karakter_loc = pyautogui.Point(ref_loc.x+447,ref_loc.y+464)
        
    pydirectinput.moveTo(ref_loc.x,ref_loc.y+30)
    pydirectinput.mouseDown(button="left")
    sleep(0.1)
    pydirectinput.mouseUp(button="left")
 

def konumu_bul():
    global konum

    konum_ss = mss.mss().grab({'top': ref_loc.y+90, 'left': ref_loc.x-30,\
                               'width':150, 'height': 13})
    konum_ss = numpy.array(konum_ss)
    konum_ss = numpy.flip(konum_ss[:, :, :3], 2)
    konum_ss = cv2.cvtColor(konum_ss, cv2.COLOR_BGR2RGB)

    buyutme_oran = 400
    en = int(konum_ss.shape[1] * buyutme_oran / 100)
    boy = int(konum_ss.shape[0] * buyutme_oran / 100)
    yeni_boyut = (en, boy)
    konum_ss = cv2.resize(konum_ss, yeni_boyut, interpolation = cv2.INTER_CUBIC)
    
    konum_yazi = pytesseract.image_to_string(konum_ss)
    konum_re = re.search("[0-9]+, [0-9]+", konum_yazi)
    
    if konum_re is not None:
        if len(konum_re.group(0).split(",")) == 2:
            try:
                konum.x = int(konum_re.group(0).split(",")[0])
                konum.y = int(konum_re.group(0).split(",")[1])
            except:
                pass

def konumu_bul_t(events):    
    while not events['exit_event'].is_set():
        konumu_bul()

def yuru(sure):
    pydirectinput.keyDown("w")
    sleep(sure)
    pydirectinput.keyUp("w")


def uzaklik(x2, x1):
    return math.sqrt( (x2.x-x1.x)**2 + (x2.y-x1.y)**2)

def aci(a,b,c):
    return math.degrees(math.acos((a**2+b**2-c**2)/(2*a*b)))

def don_derece(derece, yon="a"):
    pydirectinput.keyDown(yon)
    sleep(5.78*(derece/360))
    pydirectinput.keyUp(yon)

def don_t(evt,yon,q):
    while True:
        evt.wait()
        print("dön: "+yon)
        pydirectinput.keyDown(yon)
##        sleep(q.get())
        sleep(5.78*(q.get()/360))
        pydirectinput.keyUp(yon)
        q.task_done()
        evt.clear()

def donme_acisi_ve_yonu(x1,x2,h):
    a = uzaklik(x1, h)
    b = uzaklik(x1, x2)
    c = uzaklik(x2, h)

    x1_aci = aci(a,b,c)
    x2_aci = aci(b,c,a)
    h_aci = aci(a,c,b)
    donme_acisi = h_aci + x1_aci

    d = ((h.x-x1.x)*(x2.y-x1.y)) - ((h.y-x1.y)*(x2.x-x1.x))

    print(str(donme_acisi))
    print(str(d))

def hedefe_git2(h = Nokta(802, 450)):

    q = Queue()
    evt_d = threading.Event()
    evt_a = threading.Event()
    don_d = threading.Thread(target=don_asenk, args=(evt_d,"d",q))
    don_a = threading.Thread(target=don_asenk, args=(evt_a,"a",q))
    don_d.start()
    don_a.start()
    
    
    x2 = konumu_bul()
    x1 = x2
    
##    a = uzaklik(x1, h)
##    b = uzaklik(x1, x2)
##    c = uzaklik(x2, h)
##
##    x1_aci = aci(a,b,c)
##    x2_aci = aci(b,c,a)
##    h_aci = aci(a,c,b)
##    donme_acisi = h_aci + x1_aci
##
##    d = ((h.x-x1.x)*(x2.y-x1.y)) - ((h.y-x1.y)*(x2.x-x1.x))
                                    
##    if d > 0:
##        don_derece(donme_acisi, "d")
##    elif d < 0:
##        don_derece(donme_acisi, "a")
        
    while True:
        sleep(0.2)
        konum_tmp = konumu_bul()
        x2 = konum_tmp if konum_tmp is not None else x2
        print("x1: "+ x1.str())
        print("x2: "+ x2.str())
        if x1 != x2:
            a = uzaklik(x1, h)
            b = uzaklik(x1, x2)
            c = uzaklik(x2, h)

            x1_aci = aci(a,b,c)
            x2_aci = aci(b,c,a)
            h_aci = aci(a,c,b)
            donme_acisi = h_aci + x1_aci
##            donme_acisi = 0.2

            d = ((h.x-x1.x)*(x2.y-x1.y)) - ((h.y-x1.y)*(x2.x-x1.x))
            if (x1.x < h.x and x2.x < x1.x) or \
               (x1.x > h.x and x2.x > x1.x):
                if d > 0:
##                    don_derece(donme_acisi, "d")
                    print("donme açısı: "+str(donme_acisi))
                    q.put(donme_acisi)
                    evt_d.set()
                elif d < 0:
##                    don_derece(donme_acisi, "a")
                    print("donme açısı: "+str(donme_acisi))
                    q.put(donme_acisi)
                    evt_a.set()
            if (x1.y < h.y and x2.y < x1.y) or \
               (x1.y > h.y and x2.y > x1.y):
                if d > 0:
##                    don_derece(donme_acisi, "d")
                    print("donme açısı: "+str(donme_acisi))
                    q.put(donme_acisi)
                    evt_d.set()
                elif d < 0:
##                    don_derece(donme_acisi, "a")
                    print("donme açısı: "+str(donme_acisi))
                    q.put(donme_acisi)
                    evt_a.set()
            
                
##            print("konum1: "+str(konum1.x)+","+str(konum1.y))
##            print("konum2: "+str(konum2.x)+","+str(konum2.y))
            x1 = x2
        



##    pydirectinput.keyDown("w")
##    sleep(uzaklik(x2,h)*0.222)
##    pydirectinput.keyUp("w")

def hedefe_git3(h):

    while konum == Nokta(0,0):
        pass
    x2 = konum
    x1 = x2
##    x_changed = False
##    y_changed = False
    
##    a = uzaklik(x1, h)
##    b = uzaklik(x1, x2)
##    c = uzaklik(x2, h)
##
##    x1_aci = aci(a,b,c)
##    x2_aci = aci(b,c,a)
##    h_aci = aci(a,c,b)
##    donme_acisi = h_aci + x1_aci
##
##    d = ((h.x-x1.x)*(x2.y-x1.y)) - ((h.y-x1.y)*(x2.x-x1.x))
                                    
##    if d > 0:
##        don_derece(donme_acisi, "d")
##    elif d < 0:
##        don_derece(donme_acisi, "a")
    print(x1.str())
    while x2 != h:
        sleep(0.5)
        x2 = konum
##        x_changed = True if x_changed is True else x2.x != x1.x
##        y_changed = True if y_changed is True else x2.y != x1.y
##        print("x1: "+ x1.str())
##        print("x2: "+ x2.str())
        print(x2.str())
        if x1 != x2: #and x_changed and y_changed:
            print("girdi")
##            a = uzaklik(x1, h)
##            b = uzaklik(x1, x2)
##            c = uzaklik(x2, h)
##
##            x1_aci = aci(a,b,c)
##            x2_aci = aci(b,c,a)
##            h_aci = aci(a,c,b)
##            donme_acisi = 0 if (h_aci + x1_aci) <= 15 else h_aci + x1_aci
##            print("dönme açısı: " + str(donme_acisi))
####            donme_acisi = 0.2
##
##            d = ((h.x-x1.x)*(x2.y-x1.y)) - ((h.y-x1.y)*(x2.x-x1.x))
##            if not ((x2.x >= h.x-1 and x2.x <= h.x+1) \
##                and\
##                (x2.y >= h.y-1 and x2.y <= h.y+1)):
##                print("x1: "+ x1.str())
##                print("x2: "+ x2.str())
##                if d > 0:
####                    don_derece(donme_acisi, "d")
##                    if not evt_d.is_set():
##                        q.put(donme_acisi)
##                        print("açı q'da: " + str(donme_acisi))
##                        evt_d.set()
##                elif d < 0:
####                    don_derece(donme_acisi, "a")
##                    if not evt_a.is_set():
##                        q.put(donme_acisi)
##                        print("açı q'da: " + str(donme_acisi))
##                        evt_a.set()
            
            
                
##            print("konum1: "+str(konum1.x)+","+str(konum1.y))
##            print("konum2: "+str(konum2.x)+","+str(konum2.y))
            x1 = x2
            x_changed = False
            y_changed = False

def hedefe_git4_t(events):
    while (not events['exit_event'].is_set()) or \
          konum == Nokta(0,0):
        pass
    konum1 = konum
    konum2 = konum1

    print(konum1.str())
    print(konum2.str())
    while not events['exit_event'].is_set():
        print(konum.str())
        if konum != Nokta(0,0) and konum2 != konum1:
            konum2 = konum

    print(konum1.str())
    print(konum2.str())

def oyun_acik_mi_t(events):
    global oyun_acik
    
    while not events['exit_event'].is_set():
        oyun_acik_tmp = oyun_acik
        oyun_acik = GetWindowText(GetForegroundWindow()).lower() == 'knight online client'
        if oyun_acik_tmp is False and oyun_acik is True:
            events['oyun_acildi'].set()


def run():
    
    noktalar = []
    noktalar.append(Nokta(810,511))
    noktalar.append(Nokta(810,475))
    noktalar.append(Nokta(743,430))
    noktalar.append(Nokta(671,423))
    noktalar.append(Nokta(672,335))
    noktalar.append(Nokta(711,332))

##    town_at()
##    sleep(2)

##    for nokta in noktalar:
##        print("hedef: "+nokta.str())
##        hedefe_git3(nokta)

    hedefe_git3(Nokta(798,452))
    
def kontrol(timeout):
    events = {}
    events['can_event'] = threading.Event()
    events['exit_event'] = threading.Event()
    events['canavar_secildi_event'] = threading.Event()
    events['oyun_acik_event'] = threading.Event()
    
    
    exit_timer = threading.Timer(timeout, lambda x: x['exit_event'].set(), (events,))

    functions = [#konumu_bul_t,
                 can_bul_t,
                 can_ic_t,
                 mana_bul_t,
                 mana_ic_t,
                 canavar_bul_t,
                 canavar_secili_mi_t,
                 atak_t
                 #exit_t
                 ]
    threads = []
	
    for i in range(len(functions)):
        threads.append( threading.Thread(target=functions[i], args=(events,)) )
    
    for t in threads:
        t.start()

    exit_timer.start()


    for t in threads:
        t.join()

if __name__ == "__main__":
    pyautogui.FAILSAFE = True

    print("Başlıyor: ", end="")
    for i in range(1,4):
        sleep(0.4)
        print(i, end=" ")

    

    odaklan()

    kontrol(60*1)


    

    print("bitti")


    
    
    



