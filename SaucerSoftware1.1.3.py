from Tkinter import *
import tkFont
import RPi.GPIO as GPIO
import time
import sys
import serial

import RPi.GPIO as GPIO
from time import sleep
import datetime
from firebase import firebase
import Adafruit_DHT

import urllib2, urllib, httplib
import json
import os 
from functools import partial

#This starts the serial port for the scale
ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600

GPIO.setmode(GPIO.BCM)
#inside motor
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, GPIO.HIGH)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)

#10 inch motor
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)

#12 inch motor
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)

#14 inch motor
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)

#base motor
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)

#hx = HX711(6,13)

win = Tk()

win.overrideredirect(1)
win.geometry('800x480')

firebase = firebase.FirebaseApplication('https://saucerdatabase.firebaseio.com/', None)

myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
myFontSmall = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')
myFontMed = tkFont.Font(family = 'Helvetica', size = 20, weight = 'bold')



sauceAmt = StringVar()
sauceAmt.set("Normal")
pizzasCompleted = IntVar()
pizzasCompleted.set(0)
scaleWeight = DoubleVar()

#sauceWeightTotal = DoubleVar()

#pizzaSize = IntVar()
#pizzaSize.set(1)



# This function updates firebase

def update_firebase():
    
        sauceWeightTotal = '0.44'

        pizzaSize = '14'
    
    
        data = {"Sauce Weight = ": sauceWeightTotal, "Pizza Size": pizzaSize}
        firebase.post('/sensor/scaleWeight', data)



#This function updates the weight on the scale screen

def readWeight():
    if ser.isOpen():
        try:
            if ser.in_waiting >= 9:
                b = ser.read_all()
                b2 = b.decode("utf-8")
                if b2[b2.find(":") + 1] == "-":
                    fac = -1
                else:
                    fac = 1
                b3 = b2[b2.find(":") + 2:b2.find(":") + 9].strip()
                
                try:
                    x = round(float(b3) * fac * 2.20462,2)
                    scaleWeight.set(x)
                except ValueError:
                    pass
            else:
                pass
            win.after(200, readWeight)
        except serial.serialutil.SerialException:
            serial_open()
            win.after(200, readWeight)
    else:
        serial_open()
        win.after(200, readWeight)
        
        
#This function opens the serial port and starts recieving data from scale

def serial_open():
    try:
        ser.open()
        ser.flush()
    except serial.serialutil.SerialException:
       pass
    
    

#This function adds ten percent more sauce to the pizza
def extraSauce():
    if (sauceAmt.get() == "Normal"):
        print("Extra")
        sauceAmt.set("Extra")
    elif(sauceAmt.get() == "Less"):
        print("Extra to normal")
        sauceAmt.set("Normal")
    else:
        print("Extra stays")
        
        
        
#This function tares the scale to zero when you press the button
def tare():
    ser.write(b'TK\n')
    
    


#This function subtracts ten percent from the sauce amount    
def lessSauce():
    if (sauceAmt.get() == "Normal"):
        print("Less")
        sauceAmt.set("Less")
    elif(sauceAmt.get() == "Extra"):
        print("Less to normal")
        sauceAmt.set("Normal")
    else:
        print("Less stays")
    

#This stops the whole machine
def stop():
    print("stop")
    global running
    running = False
        

#This cleans the machine
def cleanProgram():
    time.sleep(.5)
    tare()
    sauceWeightTotal = scaleWeight
    global running
        #update_firebase()
    running = True
    
    fourteenButton['state'] = 'disable'
    twelveButton['state'] = 'disable'
    tenButton['state'] = 'disable'
    sevenButton['state'] = 'disable'
    tareButton['state'] = 'disable'
    cleanButton['state'] = 'disable'
    
    for i in range(400000):
        if i%500 == 0:
            win.update()
        if  running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(9, GPIO.HIGH)
            #GPIO.output(13, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            #GPIO.output(13, GPIO.LOW)
            time.sleep(.00001)
        else:
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            #GPIO.output(13, GPIO.LOW)
    if running:
        f = open("/home/pi/Desktop/cleanCount.txt","a+")
        now = datetime.datetime.now()
        f.write("Pizzas: "+str(pizzasCompleted.get())+"\t Date: "+str(now)+"\n")
        pizzasCompleted.set(0)
        f.close()
        
    fourteenButton['state'] = 'normal'
    twelveButton['state'] = 'normal'
    tenButton['state'] = 'normal'
    sevenButton['state'] = 'normal'
    tareButton['state'] = 'normal'
    cleanButton['state'] = 'normal'
          
    
    
    
    #This cleans the machine
def primeProgram():
    time.sleep(.5)
    tare()
    sauceWeightTotal = scaleWeight
    global running
        #update_firebase()
    running = True
    
    fourteenButton['state'] = 'disable'
    twelveButton['state'] = 'disable'
    tenButton['state'] = 'disable'
    sevenButton['state'] = 'disable'
    tareButton['state'] = 'disable'
    cleanButton['state'] = 'disable'
    
    for i in range(40000):
        if i%500 == 0:
            win.update()
        if  running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(9, GPIO.HIGH)
            #GPIO.output(13, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            #GPIO.output(13, GPIO.LOW)
            time.sleep(.00001)
        else:
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            #GPIO.output(13, GPIO.LOW)

    fourteenButton['state'] = 'normal'
    twelveButton['state'] = 'normal'
    tenButton['state'] = 'normal'
    sevenButton['state'] = 'normal'
    tareButton['state'] = 'normal'
    cleanButton['state'] = 'normal'
          
    
    


#This is the suce function for the fourteen inch pizza
def fourteenProgram():
    time.sleep(.5)
    #normal sauce
    if sauceAmt.get() == "Normal":
        print("Normal 14")
        fourteenFunction(29000, 9)
        #extra sauce
    elif sauceAmt.get() == "Extra":
        print("Extra 14")
        fourteenFunction(43500,13)
        sauceAmt.set("Normal")
    else:
        #less sauce
        print("Less 14")
        fourteenFunction(16500,5)
        sauceAmt.set("Normal")
def fourteenFunction(runs, mods):
    print("Saucing 14 Inch")
    tare()
    sauceWeightTotal = scaleWeight
    global running
    
    fourteenButton['state'] = 'disable'
    twelveButton['state'] = 'disable'
    tenButton['state'] = 'disable'
    sevenButton['state'] = 'disable'
    tareButton['state'] = 'disable'
    cleanButton['state'] = 'disable'
    
    running = True
    for i in range(runs):
        if i%500 == 0:
            win.update()
        if i%mods == 0 and running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(9, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            time.sleep(.00001)
            
            GPIO.output(9, GPIO.HIGH)
            time.sleep(.00001)
            GPIO.output(9, GPIO.LOW)
            time.sleep(.00001)
            
            GPIO.output(9, GPIO.HIGH)
            time.sleep(.00001)
            GPIO.output(9, GPIO.LOW)
            time.sleep(.00001)
            
            GPIO.output(9, GPIO.HIGH)
            time.sleep(.00001)
            GPIO.output(9, GPIO.LOW)
            time.sleep(.00001)
               
#             GPIO.output(17, GPIO.HIGH)
#             time.sleep(.00001)
#             GPIO.output(17, GPIO.LOW)
#             time.sleep(.00001)
#              
#             GPIO.output(22, GPIO.HIGH)
#             time.sleep(.00001)
#             GPIO.output(22, GPIO.LOW)
#             time.sleep(.00001)
#             
#                         
#             GPIO.output(9, GPIO.HIGH)
#             time.sleep(.00001)
#             GPIO.output(9, GPIO.LOW)
#             time.sleep(.00001)
#             
#                         
#             GPIO.output(9, GPIO.HIGH)
#             time.sleep(.00001)
#             GPIO.output(9, GPIO.LOW)
#             time.sleep(.00001)
#             
#                         
#             GPIO.output(9, GPIO.HIGH)
#             time.sleep(.00001)
#             GPIO.output(9, GPIO.LOW)
#             time.sleep(.00001)
#             
#             
           

            
        elif running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(9, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            time.sleep(.00001)
        else:
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
    if running:
        pizzasCompleted.set(pizzasCompleted.get()+1)
    fourteenButton['state'] = 'normal'
    twelveButton['state'] = 'normal'
    tenButton['state'] = 'normal'
    sevenButton['state'] = 'normal'
    tareButton['state'] = 'normal'
    cleanButton['state'] = 'normal'
    
    
    
    
#This is the function to sauce the twelve inch pizza
def twelveProgram():
    time.sleep(.5)
    if sauceAmt.get() == "Normal":
        print("Normal 12")
        twelveFunction(29000, 9)
    elif sauceAmt.get() == "Extra":
        print("Extra 12")
        twelveFunction(42500,13)
        sauceAmt.set("Normal")
    else:
        print("Less 12")
        twelveFunction(15000,5)
        sauceAmt.set("Normal")
def twelveFunction(runs, mods):
    print("Saucing 12 Inch")
    tare()
    global running
    #update_firebase()
    running = True
    
    fourteenButton['state'] = 'disable'
    twelveButton['state'] = 'disable'
    tenButton['state'] = 'disable'
    sevenButton['state'] = 'disable'
    tareButton['state'] = 'disable'
    cleanButton['state'] = 'disable'
    
    
    for i in range(runs):
        if i%500 == 0:
            win.update()
        if i%mods == 0 and running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            time.sleep(.00001)
        elif running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            time.sleep(.00001)
        else:
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
    if running:
        pizzasCompleted.set(pizzasCompleted.get()+1)
    fourteenButton['state'] = 'normal'
    twelveButton['state'] = 'normal'
    tenButton['state'] = 'normal'
    sevenButton['state'] = 'normal'
    tareButton['state'] = 'normal'
    cleanButton['state'] = 'normal'



#This is the function to sauce the ten inch pizza
def tenProgram():
    time.sleep(.5)
    if sauceAmt.get() == "Normal":
        print("Normal 10")
        tenFunction(30000, 9)
    elif sauceAmt.get() == "Extra":
        print("Extra 10")
        tenFunction(44000,13)
        sauceAmt.set("Normal")
    else:
        print("Less 10")
        tenFunction(16000,5)
        sauceAmt.set("Normal")
def tenFunction(runs, mods):
    print("Saucing 10 Inch")
    tare()
    global running
    #update_firebase()
    running = True
    
    fourteenButton['state'] = 'disable'
    twelveButton['state'] = 'disable'
    tenButton['state'] = 'disable'
    sevenButton['state'] = 'disable'
    tareButton['state'] = 'disable'
    cleanButton['state'] = 'disable'
    
    for i in range(runs):
        if i%500 == 0:
            win.update()
        if i%mods == 0 and running: 
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(.00001)
    
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            time.sleep(.00001)
        elif running:    
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            time.sleep(.00001)
            
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            time.sleep(.00001)
        else:
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
    if running:
        pizzasCompleted.set(pizzasCompleted.get()+1)
    fourteenButton['state'] = 'normal'
    twelveButton['state'] = 'normal'
    tenButton['state'] = 'normal'
    sevenButton['state'] = 'normal'
    tareButton['state'] = 'normal'
    cleanButton['state'] = 'normal'
    



#This is the function to sauce the seven inch pizza
def sevenProgram():
    time.sleep(.5)
    if sauceAmt.get() == "Normal":
        print("Normal 7")
        sevenFunction(32000, 10)
    elif sauceAmt.get() == "Extra":
        print("Extra 7")
        sevenFunction(44000,13)
        sauceAmt.set("Normal")
    else:
        print("Less 7")
        sevenFunction(16000,5)
        sauceAmt.set("Normal")
def sevenFunction(runs, mods):
    print("Saucing 7 Inch")
    tare()
    global running
    #update_firebase()
    running = True
    fourteenButton['state'] = 'disable'
    twelveButton['state'] = 'disable'
    tenButton['state'] = 'disable'
    sevenButton['state'] = 'disable'
    tareButton['state'] = 'disable'
    cleanButton['state'] = 'disable'
    for i in range(runs):
        if i%500 == 0:
            win.update()
        if i%mods == 0 and running:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(.00001)
            GPIO.output(3, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            time.sleep(.00001)
        elif running:
            GPIO.output(3,GPIO.HIGH)
            time.sleep(.00001)
            GPIO.output(3, GPIO.LOW)
            time.sleep(.00001)
        else:
            GPIO.output(3, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(9, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)        
    if running:
        pizzasCompleted.set(pizzasCompleted.get()+1)
        
    fourteenButton['state'] = 'normal'
    twelveButton['state'] = 'normal'
    tenButton['state'] = 'normal'
    sevenButton['state'] = 'normal'
    tareButton['state'] = 'normal'
    cleanButton['state'] = 'normal'

win.title("Saucer Saucer Saucer")
win.geometry('800x480')

fourteenButton  = Button(win, text = "14 Inch", font = myFont, bg = "lightgreen", command = fourteenProgram, height =2 , width = 6) 
fourteenButton.place(x=610, y=0)

twelveButton  = Button(win, text = "12 Inch", font = myFont, bg = "lightgreen", command = twelveProgram, height =2 , width = 6) 
twelveButton.place(x=405, y=0)

tenButton  = Button(win, text = "10 Inch", font = myFont, bg = "lightgreen", command = tenProgram, height =2 , width = 6) 
tenButton.place(x=205, y=0)

sevenButton  = Button(win, text = "7 Inch", font = myFont, bg = "lightgreen", command = sevenProgram, height =2 , width = 6) 
sevenButton.place(x=0, y=0)

stopButton  = Button(win, text = "STOP", font = myFont, bg = "red", command = stop, height =1 , width = 15) 
stopButton.place(x=180, y=150)


cleanButton  = Button(win, text = "Clean", font = myFontSmall, command = cleanProgram, height =5, width = 18) 
cleanButton.place(relx=0.2, rely=0.85, anchor = "center")


tareButton  = Button(win, text = "Tare", font = myFontSmall, command = tare, height =5, width = 18) 
tareButton.place(relx=0.8, rely=0.85, anchor = "center")

primeButton  = Button(win, text = "Prime", font = myFontSmall, command = primeProgram, height =5, width = 18) 
primeButton.place(relx=0.5, rely=0.85, anchor = "center")

#extraSauceButton  = Button(win, text = "Extra", font = myFontMed, bg = "lightgreen", command = extraSauce, height =1 , width = 4) 
#extraSauceButton.place(relx=0.7, rely=0.9, anchor = "center")

#lessSauceButton  = Button(win, text = "Less", font = myFontMed, bg = "tomato", command = lessSauce, height =1 , width = 4) 
#lessSauceButton.place(relx=0.3, rely=0.9, anchor = "center")

#sauceAmtBox = LabelFrame(win)
#sauceAmtBox.place(relx=0.5, rely=0.9, anchor = "center", relheight = 0.1, relwidth = 0.15)

#sauceAmtText = Label(sauceAmtBox, textvariable = sauceAmt, font = myFontMed)
#sauceAmtText.place(anchor = "center", relx = 0.5, rely = 0.5)




scaleWeightBox = LabelFrame(win)
scaleWeightBox.place(relx=0.2, rely=0.6, anchor = "center", relheight = 0.1, relwidth = 0.25)

scaleWeightText = Label(scaleWeightBox, textvariable = scaleWeight, font = myFontMed)
scaleWeightText.place(anchor = "center", relx = 0.5, rely = 0.6)




pizzasSaucedBox = LabelFrame(win)
pizzasSaucedBox.place(relx=0.8, rely=0.6, anchor = "center", relheight = 0.1, relwidth = 0.25)

pizzasSaucedText = Label(pizzasSaucedBox, textvariable = pizzasCompleted, font = myFontMed)
pizzasSaucedText.place(anchor = "center", relx = 0.5, rely = 0.6)




readWeight()
mainloop()
