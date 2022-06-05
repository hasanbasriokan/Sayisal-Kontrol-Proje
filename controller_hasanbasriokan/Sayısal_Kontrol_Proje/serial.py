import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from GUI import *
import time
import serial

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

#Veritabani islemleri
import sqlite3
baglanti = sqlite3.connect("urunler.db")
islem = baglanti.cursor()
baglanti.commit()
table = islem.execute("create table if not exists urun (kp double, ki double, kd double) ")

start = 0
CW = 0

gonder = serial.Serial("COM1", 9600)

def Kp():
    
    if ui.lne_Kp.text() == '':
        ui.statusbar.showMessage("Kp GİRİLMEDİ ")
    else:
        Kp = int(ui.lne_Kp.text())
        ui.statusbar.showMessage("Kp değeri: " + ui.lne_Kp.text())
        Kp_mesaj = QMessageBox.question(pencere,"Kp Değeri", "Kp değeri: " + ui.lne_Kp.text(), QMessageBox.Ok)
        ui.statusbar.showMessage("Kp değeri: " + ui.lne_Kp.text())
        gonder.write("P" + ui.lne_Kp.text())
    
def Ki():
    if ui.lne_Kp.text() == '':
        ui.statusbar.showMessage("Ki GİRİLMEDİ ")
    else:
        Ki = int(ui.lne_Ki.text())
        ui.statusbar.showMessage("Ki değeri: " + ui.lne_Ki.text())
        Kp_mesaj = QMessageBox.question(pencere,"Ki Değeri", "Ki değeri: " + ui.lne_Ki.text(), QMessageBox.Ok)
        ui.statusbar.showMessage("Ki değeri: " + ui.lne_Ki.text())
        gonder.write("I" + ui.lne_Ki.text())

def Kd():
    if ui.lne_Kp.text() == '':
        ui.statusbar.showMessage("Kd GİRİLMEDİ ")
    else:
        Kd = int(ui.lne_Kd.text())
        ui.statusbar.showMessage("Kd değeri: " + ui.lne_Kd.text())
        Kp_mesaj = QMessageBox.question(pencere,"Kd Değeri", "Kd değeri: " + ui.lne_Kd.text(), QMessageBox.Ok)
        ui.statusbar.showMessage("Kd değeri: " + ui.lne_Kd.text())
        gonder.write("D" + ui.lne_Kd.text())

def MotorHizi():
    if ui.lne_Kp.text() == '':
        ui.statusbar.showMessage("HIZ GİRİLMEDİ ")
    else:
        MotorHizi = int(ui.lne_MotorHizi.text())
        ui.statusbar.showMessage("Motor Hiz değeri: " + ui.lne_MotorHizi.text())
        Kp_mesaj = QMessageBox.question(pencere,"Motor Hiz Değeri", "Motor Hiz değeri: " + ui.lne_MotorHizi.text(), QMessageBox.Ok)
        ui.statusbar.showMessage("Motor Hiz değeri: " + ui.lne_MotorHizi.text())
        gonder.write("H" + ui.lne_MotorHizi.text())

def StartStop():
    global start
    if start == 0:
        Kp_mesaj = QMessageBox.question(pencere,"Motor Calisma Durumu", "Motoru çalıştırmak ister misiniz?", QMessageBox.Yes | QMessageBox.No)
        if Kp_mesaj == QMessageBox.Yes:
            ui.statusbar.showMessage("Motor çalışıyor")
            start = 1
        else:
            ui.statusbar.showMessage("Motor çalışmıyor")
          
    else:
        Kp_mesaj = QMessageBox.question(pencere,"Motor Calisma Durumu", "Motoru durdurmak ister misiniz? ", QMessageBox.Yes | QMessageBox.No)
        if Kp_mesaj == QMessageBox.Yes:
            ui.statusbar.showMessage("Motor çalışmıyor")
            start = 0
        else:
            ui.statusbar.showMessage("Motor çalışıyor")

def CW():
    global CW
    if CW == 0:
        CW = 1
        ui.statusbar.showMessage("Motor saat yönünde dönüyor ")
    else:
        CW = 0
        ui.statusbar.showMessage("Motor saat yönünün tersine dönüyor ")
 
		
#Butonlar
ui.btn_SetKp.clicked.connect(Kp)
ui.btn_SetKi.clicked.connect(Ki)
ui.btn_SetKd.clicked.connect(Kd)
ui.btn_MotorHizi.clicked.connect(MotorHizi)
ui.btn_StartStop.clicked.connect(StartStop)
ui.btn_CW.clicked.connect(CW)


# Pencere kapatma butonuna basilmadigi surece acik kalmasi icin yazdik
sys.exit(uygulama.exec_())
