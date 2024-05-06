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

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
path = "c:\\users\\faruk\\desktop\\ko-python-bot\\"

karakter_loc = pyautogui.Point(10,10)
ref_loc = pyautogui.Point(10,10)
can = 100
mana = 100
canavar_secili = False
atak_yapiliyor = False
atak_ara_ver = False
canavar_ad = ""

class Nokta:
    def __init__(self, x=0, y=0):
        self.x=x
        self.y=y

    def str(self):
        return str(self.x)+","+str(self.y)

    def __eq__(self, x2):
        return (self.x == x2.x and self.y == x2.y)

def chat():
    chat_loc = pyautogui.locateOnScreen(path+"chat.png",confidence=0.8)
    
    if chat_loc != None:
        chat = pyautogui.center()
        pydirectinput.click(chat.x+60, chat.y)
        #pyautogui.write("afkyim")
        #pyautogui.press("enter")
        #pyautogui.press("esc")
        
def karakteri_bul():
    global karakter_loc
    global ref_loc
    
    ref_box = pyautogui.locateOnScreen(path+"ko_yazi.png",
                                           confidence=0.8)
    if ref_box is not None:
        ref_loc = pyautogui.center(ref_box)
        karakter_loc = pyautogui.Point(ref_loc.x+447,
                                       ref_loc.y+464)
    
def etrafa_bak():
        pydirectinput.mouseDown(duration=5, button='right')
        pydirectinput.moveTo(x=karakter_loc.x+50,
                             y=karakter_loc.y)
        pydirectinput.mouseUp(button='right')
	
def kutu_topla():
    kutu_box = None
    kutu_loc = karakter_loc
    conf = 0.7
    kutu_reg = (ref_loc.x+310,ref_loc.y+280,320, 272)
    
    for i in listdir(path+"kutu5"):
        dosya = path+"kutu5\\"+i
        kutu = pyautogui.locateCenterOnScreen(dosya,
                                              confidence=conf,
                                              region=kutu_reg)
        
        if kutu is not None:
            pydirectinput.mouseDown(kutu.x, kutu.y, button="left")
            pydirectinput.mouseUp(button="left")
            sleep(0.3)
            pydirectinput.move(28, -129)
            pydirectinput.mouseDown(button="left")
            pydirectinput.mouseUp(button="left")
            sleep(0.3)
            pydirectinput.move(0,50)
            pydirectinput.mouseDown(button="left")
            pydirectinput.mouseUp(button="left")
            
            
##            time.sleep(0.3)
##            if pyautogui.locateOnScreen(path+"bos_kutu.png",confidence=0.8):
##                break
##            else:
##                pydirectinput.move(28, -129)
##                pydirectinput.mouseDown(button="left")
##                pydirectinput.mouseUp(button="left")
##                for i in (0,1,2):
##                    if pyautogui.locateOnScreen(path+"bos_kutu.png",confidence=0.8):
##                        break
##                    elif pyautogui.locateOnScreen(path+"kutu_acik.png",confidence=0.8):
##                        pydirectinput.move(0,50)
##                        pydirectinput.mouseDown(button="left")
##                        pydirectinput.mouseUp(button="left")
##                        time.sleep(0.1)
##            break

def town_at():
    pydirectinput.press("enter")
    pyautogui.write("/town")
    pydirectinput.press("enter")
    
def can_bul():
    global can
    
    baslangic=(ref_loc.x-42,ref_loc.y+61)
    bitis=(ref_loc.x+148,ref_loc.y+61)
    imlec = bitis
    
    while True: 
        imlec = (imlec[0]-5, imlec[1])
        
        if (not pyautogui.pixelMatchesColor(int(imlec[0]),int(imlec[1]),(0,0,0))) and imlec[0] >= baslangic[0]:
            can = math.ceil(((imlec[0]-baslangic[0])/(bitis[0]-baslangic[0]))*100)
            print("can:"+str(can))
            break

def mana_bul():
    global mana
    
    baslangic=(ref_loc.x-42,ref_loc.y+65)
    bitis=(ref_loc.x+148,ref_loc.y+65)
    imlec = bitis
    
    while True: 
        imlec = (imlec[0]-5, imlec[1])
        
        if (not pyautogui.pixelMatchesColor(int(imlec[0]),int(imlec[1]),(0,0,0))) and imlec[0] >= baslangic[0]:
            mana = math.ceil(((imlec[0]-baslangic[0])/(bitis[0]-baslangic[0]))*100)
            print("mana: "+str(mana))
            break
        
def canavar_bul():
    global canavar_secili
    global canavar_ad
    
    isim_reg = (ref_loc.x+323,ref_loc.y+13,230, 72)
    conf = 0.8
    
    
    canavar_secili = pyautogui.locateOnScreen(path+canavar_ad+".png",
                                              confidence=conf,
                                              region=isim_reg) is not None
def canavar_bul(canavar_ad):
    isim_reg = (ref_loc.x+323,ref_loc.y+13,230, 72)
    conf = 0.8
    
    
    return pyautogui.locateOnScreen(path+canavar_ad+".png",
                                              confidence=conf,
                                              region=isim_reg) is not None
    

def atak():
    global atak_yapiliyor, canavar_secili, atak_ara_ver
    
    sayac = 0
    
    while canavar_secili and atak_yapiliyor and not atak_ara_ver:
##        pydirectinput.press("r")
##        pydirectinput.press("r")
        pydirectinput.press("1")
        pydirectinput.press("1")
        pydirectinput.press("1")
        pydirectinput.press("1")
        pydirectinput.press("1")
        canavar_bul()
        
        sayac = sayac + 1
        if sayac == 5:
            atak_ara_ver = True
            sayac = 0


skiller = {}

def skil_kaydet(skil,zaman,timestamp,bekleme):
    global skiller
    skiller[skil] = [zaman,timestamp,bekleme]

def skilleri_bas():
    global skiller
    for i in skiller.keys():
        if (time()-skiller[i][1]) >= skiller[i][0]:
            pydirectinput.press(str(i))
            sleep(skiller[i][2])
            skiller[i][1]=time()

def skilleri_bas_2():
    global skiller
    for i in skiller.keys():
        pydirectinput.press(str(i))

def init():
    karakteri_bul()
    print(karakter_loc)

    pydirectinput.moveTo(ref_loc.x,ref_loc.y+30)
    pydirectinput.mouseDown(button="left")
    sleep(0.1)
    pydirectinput.mouseUp(button="left")
    pydirectinput.mouseDown(button="left")
    sleep(0.1)
    pydirectinput.mouseUp(button="left")

def main():
    global canavar_ad, atak_yapiliyor, canavar_secili, can, mana, atak_ara_ver

    canavar_ad = "direwolf"
    
    skil_kaydet(3, 2*60, 0, 0)
    skil_kaydet(4, 40  , 0, 0)

    basla = time()

    while True:
        skilleri_bas()
        
        if not canavar_secili:
            pydirectinput.press("z")
            canavar_bul()
            if canavar_secili:
                print("canavar bulundu")
                print("atak başladı")
                atak_yapiliyor = True
            else:
                print("canavar yok")

        atak()
        
        if canavar_secili:
            print("atak devam ediyor")
        
        if not canavar_secili:
            print("atak bitti")
            atak_yapiliyor = False
            
        if atak_ara_ver and canavar_secili:
            atak_ara_ver = False
       
            
        
        can_bul()
        while can <= 90:
            pydirectinput.press("5")
            can_bul()
        mana_bul()
        if mana <= 60:
            pydirectinput.press("2")
        

            
def rpr_yap(hedef):
    
    konum = None
    ilk = {'x': 0, 'y': 0}
    son = {'x': 0, 'y': 0}
    degisti = {'x': False, 'y': False}
    deneme_sayisi = 0
    hedef_yon = None
    mesafe = {'x':0,'y':0}
    duz_yuru = False
    
    konum = None
    while konum is None:
        pydirectinput.keyDown("w")
        sleep(0.1)
        pydirectinput.keyUp("w")
        
        konum_ss = pyautogui.screenshot().crop((ref_loc.x-30,ref_loc.y+90,
                                                ref_loc.x+120,ref_loc.y+103))
        ilk_konum = pytesseract.image_to_string(konum_ss)
        konum=re.search("[0-9]+.*[0-9]+", ilk_konum)
        if konum is not None:
            print("ilk konum")
            print(konum.group(0))
            try:
                ilk['x'] = int(konum.group(0).split(",")[0])
                ilk['y'] = int(konum.group(0).split(",")[1])
            except:
                konum=None
                continue
##            print(ilk['x'])
##            print(ilk['y'])

    mesafe['x'] = abs(hedef['x'] - ilk['x'])
    mesafe['y'] = abs(hedef['y'] - ilk['y'])
    
    if hedef['y'] < ilk['y']:
        hedef_yon = 7
    else:
        hedef_yon = 5
    print("hedef yön:" + str(hedef_yon))
    
    while mesafe['x'] >= 1:
        konum = None
        deneme_sayisi=0
        bolge = None
        
        while (degisti['x'] == False or degisti['y'] == False) and deneme_sayisi < 2:
            pydirectinput.keyDown("w")
            if bolge == 5 or bolge == 7:
                sleep(0.25*mesafe['x'])
            else:
                sleep(1)
            pydirectinput.keyUp("w")
            
            konum_ss = pyautogui.screenshot().crop((ref_loc.x-30,ref_loc.y+90,
                                                    ref_loc.x+120,ref_loc.y+103))
            son_konum = pytesseract.image_to_string(konum_ss)
            konum=re.search("[0-9]+.*[0-9]+", son_konum)
            if konum is not None:
##                print("son konum")
##                print(konum.group(0))
                try:
                    son['x'] = int(konum.group(0).split(",")[0])
                    son['y'] = int(konum.group(0).split(",")[1])
                except:
                    continue
##                print("son_x:" + str(son['x']))
##                print("son_y:" + str(son['y']))
##                print("ilk_x:" + str(ilk['x']))
##                print("ilk_y:" + str(ilk['y']))
                print("deneme: " + str(deneme_sayisi))
                deneme_sayisi = deneme_sayisi + 1
                
                if son['x'] != ilk['x'] and degisti['x'] == False:
                    degisti['x'] = True
                    print("x değişti")
                if son['y'] != ilk['y'] and degisti['y'] == False:
                    degisti['y'] = True
                    print("y değişti")
                    
        print("\ndevam")
        print(str(son['x'])+" "+str(son['y']))
        print("\n")

        
        if son['x'] > ilk['x'] and son['y'] > ilk['y']:
            bolge = 1
        elif son['x'] < ilk['x'] and son['y'] > ilk['y']:
            bolge = 2
        elif son['x'] < ilk['x'] and son['y'] < ilk['y']:
            bolge = 3
        elif son['x'] > ilk['x'] and son['y'] < ilk['y']:
            bolge = 4
            
        elif son['x'] > ilk['x'] and son['y'] == ilk['y']:
            bolge = 5
        elif son['x'] == ilk['x'] and son['y'] > ilk['y']:
            bolge = 6
        elif son['x'] < ilk['x'] and son['y'] == ilk['y']:
            bolge = 7
        elif son['x'] == ilk['x'] and son['y'] < ilk['y']:
            bolge = 8
        else:
            bogle = 9

        oran = 1
        if son['y'] != ilk['y']:
            oran = abs(son['x']-ilk['x'])/abs((son['y']-ilk['y']))

        print("oran: "+str(oran))
            
        if hedef_yon == 7:
            if bolge == 1:
                pydirectinput.keyDown("a")
                sleep(1+0.2*oran)
                pydirectinput.keyUp("a")
            elif bolge == 2:
                pydirectinput.keyDown("a")
                sleep(0.2)
                pydirectinput.keyUp("a")
            elif bolge == 4:
                pydirectinput.keyDown("d")
                sleep(1+0.2*oran)
                pydirectinput.keyUp("d")
            elif bolge == 3:
                pydirectinput.keyDown("d")
                sleep(0.2)
                pydirectinput.keyUp("d")
        elif hedef_yon == 5:
            if bolge == 1:
                pydirectinput.keyDown("d")
                sleep(0.2)
                pydirectinput.keyUp("d")
            if bolge == 2:
                pydirectinput.keyDown("d")
                sleep(1+0.2*oran)
                pydirectinput.keyUp("d")
            elif bolge == 3:
                pydirectinput.keyDown("a")
                sleep(1+0.2*oran)
                pydirectinput.keyUp("a")
            elif bolge == 4:
                pydirectinput.keyDown("a")
                sleep(0.2)
                pydirectinput.keyUp("a")
            

        ilk['x'] = son['x']
        ilk['y'] = son['y']
        degisti['x'] = False
        degisti['y'] = False
        
        mesafe['x'] = abs(hedef['x'] - ilk['x'])
        mesafe['y'] = abs(hedef['y'] - ilk['y'])
        
        print("bolge: " + str(bolge))
        print("mesafe x: " + str(mesafe['x']))
        print("mesafe y: " + str(mesafe['y']))

def konumu_bul():
    ilk = Nokta()

##    a = time()
    konum_ss = mss.mss().grab({'top': ref_loc.y+90, 'left': ref_loc.x-30,\
                               'width':150, 'height': 13})
    konum_ss = numpy.array(konum_ss)
    konum_ss = numpy.flip(konum_ss[:, :, :3], 2)
    konum_ss = cv2.cvtColor(konum_ss, cv2.COLOR_BGR2RGB)
##    konum_ss = pyautogui.screenshot(region=(ref_loc.x-30,ref_loc.y+90,\
##                                            ref_loc.x+120,ref_loc.y+103))
##    print(time()-a)
##    konum_ss = numpy.array(konum_ss)
##    konum_ss =konum_ss[:, :, ::-1].copy() 


    buyutme_oran = 400
    en = int(konum_ss.shape[1] * buyutme_oran / 100)
    boy = int(konum_ss.shape[0] * buyutme_oran / 100)
    yeni_boyut = (en, boy)
    konum_ss = cv2.resize(konum_ss, yeni_boyut, interpolation = cv2.INTER_CUBIC)
    
    konum = pytesseract.image_to_string(konum_ss)
##    print(konum)
##    cv2.imwrite(r"d:\img.png", konum_ss)
    konum = re.search("[0-9]+, [0-9]+", konum)
##    print(konum)
    
    if konum is not None:
        if len(konum.group(0).split(",")) != 2:
            return None
        else:
            try:
                ilk.x = int(konum.group(0).split(",")[0])
                ilk.y = int(konum.group(0).split(",")[1])
                return ilk
            except:
                return None
    else:
        return None
    

def yuru(sure):
    pydirectinput.keyDown("w")
    sleep(sure)
    pydirectinput.keyUp("w")

def bolgeyi_bul(son=None):
    ilk = konumu_bul()
    while ilk is None:
        yuru(0.3)
        ilk = konumu_bul()
        
    yuru(1)
    if son is None:
        son = konumu_bul()
        while son is None:
            yuru(0.3)
            son = konumu_bul()

    if son['x'] > ilk['x'] and son['y'] >= ilk['y']:
        bolge = 1
    elif son['x'] <= ilk['x'] and son['y'] > ilk['y']:
        bolge = 2
    elif son['x'] < ilk['x'] and son['y'] <= ilk['y']:
        bolge = 3
    elif son['x'] >= ilk['x'] and son['y'] <= ilk['y']:
        bolge = 4
        
##    elif son['x'] > ilk['x'] and son['y'] == ilk['y']:
##        bolge = 5
##    elif son['x'] == ilk['x'] and son['y'] > ilk['y']:
##        bolge = 6
##    elif son['x'] < ilk['x'] and son['y'] == ilk['y']:
##        bolge = 7
##    elif son['x'] == ilk['x'] and son['y'] < ilk['y']:
##        bolge = 8
##    else:
##        bolge = 9

    return bolge

def oran_hesapla(hedef=None):
    konum1 = konumu_bul()
    konum2 = hedef
    if konum2 is None:
        bolgeyi_bul()
        konum2 = konumu_bul()

    print(konum1)
    print(konum2)
    print("oran: " + str(abs((konum2['x']-konum1['x'])/(konum2['y']-konum1['y']))))

    return abs(konum2['x']-konum1['x'])/(konum2['y']-konum1['y'])

def uzaklik(x2, x1):
    return math.sqrt( (x2.x-x1.x)**2 + (x2.y-x1.y)**2)

def aci(a,b,c):
    return math.degrees(math.acos((a**2+b**2-c**2)/(2*a*b)))

def don_derece(derece, yon="a"):
    print(derece)
    pydirectinput.keyDown(yon)
    sleep(5.78*(derece/360))
    pydirectinput.keyUp(yon)

def bolgeyi_esitle(hedef):
    bolgem = bolgeyi_bul()
    hedefin_bolgesi = bolgeyi_bul(hedef)

    print(bolgem)
    print(hedefin_bolgesi)

    if bolgem != hedefin_bolgesi:
        if bolgem+2 == hedefin_bolgesi or bolgem-2 == hedefin_bolgesi:
            pydirectinput.keyDown("a")
            sleep(3)
            pydirectinput.keyUp("a")
        if bolgem+1 == hedefin_bolgesi or bolgem-3 == hedefin_bolgesi:
            pydirectinput.keyDown("a")
            sleep(1.5)
            pydirectinput.keyUp("a")
        if bolgem-1 == hedefin_bolgesi or bolgem+3 == hedefin_bolgesi:
            pydirectinput.keyDown("d")
            sleep(1.5)
            pydirectinput.keyUp("d")

##    konumum = konumu_bul()
##    
##    while hedef != konumum:
##        pydirectinput.keyDown("w")
##        
##        oranim = oran_hesapla()
##        hedefin_orani = oran_hesapla(hedef)
##        donme_orani = abs(hedefin_orani-oranim)
##        
##        if bolgem == 1 or bolgem == 3:
##            if oranim > hedefin_orani:
##                pydirectinput.keyDown("a")
##                sleep(0.02*donme_orani)
##                pydirectinput.keyUp("a")
##            elif oranim < hedefin_orani:
##                pydirectinput.keyDown("d")
##                sleep(0.02*donme_orani)
##                pydirectinput.keyUp("d")
##        if bolgem == 2 or bolgem == 4:
##            if oranim > hedefin_orani:
##                pydirectinput.keyDown("d")
##                sleep(0.02*donme_orani)
##                pydirectinput.keyUp("d")
##            elif oranim < hedefin_orani:
##                pydirectinput.keyDown("a")
##                sleep(0.02*donme_orani)
##                pydirectinput.keyUp("a")
##                
##        konumum = konumu_bul()
##    pydirectinput.keyUp("w")

def hedefe_git(x1=None, x2=None, h = {'x': 802, 'y': 450}):
    if x1 is None:
        x1 = konumu_bul()
        while x1 is None:
            yuru(0.5)
            x1 = konumu_bul()
        

    if x2 is None:
        yuru(2)
        x2 = konumu_bul()
        while x2 is None or x1 == x2:
            yuru(0.5)
            x2 = konumu_bul()
        
    a = uzaklik(x1, h)
    b = uzaklik(x1, x2)
    c = uzaklik(x2, h)

    x1_aci = aci(a,b,c)
    x2_aci = aci(b,c,a)
    h_aci = aci(a,c,b)
    donme_acisi = h_aci + x1_aci

    d = ((h['x']-x1['x'])*(x2['y']-x1['y'])) - ((h['y']-x1['y'])*(x2['x']-x1['x']))

    if d > 0:
        don_derece(donme_acisi, "d")
    elif d < 0:
        don_derece(donme_acisi, "a")

    pydirectinput.keyDown("w")
    sleep(uzaklik(x2,h)*0.222)
    pydirectinput.keyUp("w")

    print("hedef bitti")
    tmp = konumu_bul()
    while tmp is None:
        yuru(0.5)
        tmp = konumu_bul()
    return (tmp,x2)


def run():
    
    noktalar = []
    noktalar.append(Nokta(810,511))
    noktalar.append(Nokta(810,475))
    noktalar.append(Nokta(743,430))
    noktalar.append(Nokta(671,423))
    noktalar.append(Nokta(672,335))
    noktalar.append(Nokta(711,332))

    town_at()
    sleep(2)

    for nokta in noktalar:
        print("hedef: "+nokta.str())
        hedefe_git3(nokta)
    
##    for i in range(1, len(noktalar)):
##        tmp,x2 = hedefe_git(x2,tmp, noktalar[i])

def don_asenk(evt,yon,q):
    while True:
        evt.wait()
        print("dön: "+yon)
        pydirectinput.keyDown(yon)
##        sleep(q.get())
        sleep(5.78*(q.get()/360))
        pydirectinput.keyUp(yon)
        q.task_done()
        evt.clear()

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

def hedefe_git3(h = Nokta(802, 450)):

    q = Queue()
    evt_d = threading.Event()
    evt_a = threading.Event()
    don_d = threading.Thread(target=don_asenk, args=(evt_d,"d",q))
    don_a = threading.Thread(target=don_asenk, args=(evt_a,"a",q))
    don_d.start()
    don_a.start()
    
    
    x2 = konumu_bul()
    x1 = x2
    x_changed = False
    y_changed = False
    
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
    
    while not ((x2.x >= h.x-1 and x2.x <= h.x+1)  and (x2.y >= h.y-1 and x2.y <= h.y+1)):
##        sleep(0.2)
        konum_tmp = konumu_bul()
        x2 = konum_tmp if konum_tmp is not None else x2
        x_changed = True if x_changed is True else x2.x != x1.x
        y_changed = True if y_changed is True else x2.y != x1.y
##        print("x1: "+ x1.str())
##        print("x2: "+ x2.str())
        if x1 != x2 and x_changed and y_changed:
            print("girdi")
            a = uzaklik(x1, h)
            b = uzaklik(x1, x2)
            c = uzaklik(x2, h)

            x1_aci = aci(a,b,c)
            x2_aci = aci(b,c,a)
            h_aci = aci(a,c,b)
            donme_acisi = 0 if (h_aci + x1_aci) <= 15 else h_aci + x1_aci
            print("dönme açısı: " + str(donme_acisi))
##            donme_acisi = 0.2

            d = ((h.x-x1.x)*(x2.y-x1.y)) - ((h.y-x1.y)*(x2.x-x1.x))
            if not ((x2.x >= h.x-1 and x2.x <= h.x+1) \
                and\
                (x2.y >= h.y-1 and x2.y <= h.y+1)):
                print("x1: "+ x1.str())
                print("x2: "+ x2.str())
                if d > 0:
##                    don_derece(donme_acisi, "d")
                    if not evt_d.is_set():
                        q.put(donme_acisi)
                        print("açı q'da: " + str(donme_acisi))
                        evt_d.set()
                elif d < 0:
##                    don_derece(donme_acisi, "a")
                    if not evt_a.is_set():
                        q.put(donme_acisi)
                        print("açı q'da: " + str(donme_acisi))
                        evt_a.set()
            
            
                
##            print("konum1: "+str(konum1.x)+","+str(konum1.y))
##            print("konum2: "+str(konum2.x)+","+str(konum2.y))
            x1 = x2
            x_changed = False
            y_changed = False



##    pydirectinput.keyDown("w")
##    sleep(uzaklik(x2,h)*0.222)
##    pydirectinput.keyUp("w")


if __name__ == "__main__":
    pyautogui.FAILSAFE = True

    print("Başlıyor: ", end="")
    for i in range(1,4):
        sleep(0.4)
        print(i, end=" ")

    init()

    pydirectinput.keyDown("w")
    run()
    pydirectinput.keyUp("w")

    
    
    



