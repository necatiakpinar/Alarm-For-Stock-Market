import os
import sys
import codecs
from bs4 import BeautifulSoup
#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#GUI
import tkinter as tk
from tkinter.ttk import *
from functools import partial


#Alarm
from pydub import AudioSegment
from pydub.playback import play


#Variables
startUpdating=False
refleshButton = None


#-------------------My Portfolio Variables-------------------#

#----Data Information----#
portfolioList = []
individualStockInfoList = [] 
portfolioStockInfoList = []
portfolioStockInfoDetailedList = []
portfolioStockInfoDetailedDict = {}

#Details
stockName = []
stockUnit = []
stockLivePrice = []
stockAmountTL = []
stockCost = []
stockProfitLoss = []
stockFunctions = []



#GUI Variables
nameLabelList = []
unitLabelList = []
livePriceLabelList = []
amountLabelList = []
costLabelList = []
profitLossLabelList = []



#--------------------Favorite Stock Variables--------------------#

#Details
favStockName = []
favStockNameList = []
favStockGroup = []
favStockGroupList = []
favStockLivePrice = []
favStockLivePriceList = []
favStockHigh = []
favStockHighList = []
favStockLow = []
favStockLowList = []
favStockChange = []
favStockChangeList = []
favStockFunctions = []
favStockFunctionsList = []

#GUI Variables
favNameLabelList = []
favGroupLabelList = []
favLivePriceLabelList = []
favHighLabelList = []
favLowLabelList = []
favChangeLabelList = []
favFunctionLabelList = []
alarmButtonList = []
#---Test Button---#



def clearPortfolio():
#-----My Portfolio Variables-----#

    #Data Information
    portfolioList.clear()
    individualStockInfoList.clear()
    portfolioStockInfoList.clear()
    portfolioStockInfoDetailedList.clear()
    portfolioStockInfoDetailedDict.clear()
    
    #Details
    stockName.clear()
    stockUnit.clear()
    stockLivePrice.clear()
    stockAmountTL.clear()
    stockCost.clear()
    stockProfitLoss.clear()
    stockFunctions.clear()
    
    #GUI
    nameLabelList.clear()
    unitLabelList.clear()
    livePriceLabelList.clear()
    amountLabelList.clear()
    costLabelList.clear()
    profitLossLabelList.clear()
    
    
    
#--------Favorite Stocks---------#
    #Details
    favStockName.clear()
    favStockNameList.clear()
    favStockGroup.clear()
    favStockGroupList.clear()
    favStockLivePrice.clear()
    favStockLivePriceList.clear()
    favStockHigh.clear()
    favStockHighList.clear()
    favStockLow.clear()
    favStockLowList.clear()
    favStockChange.clear()
    favStockChangeList.clear()
    favStockFunctions.clear()
    favStockFunctionsList.clear()
    
    
    #GUI Variables
    favNameLabelList.clear()
    favGroupLabelList.clear()
    favLivePriceLabelList.clear()
    favHighLabelList.clear()
    favLowLabelList.clear()
    favChangeLabelList.clear()
    favFunctionLabelList.clear()
    alarmButtonList.clear()
    

#------Alarm-----#
    #alarmStockLivePriceLabelList.clear()

def fetchPortfolioFromSite():
    global startUpdating
    global refleshButton
    refleshButton = driver.find_element_by_id("btn-WidgetPortfolioOverall-refresh")
    
    clearPortfolio()
    
    fetchFavoriteStocksFromSite() #Instantiate my Favorite Stock List    

    #Stock Portfolio
    portfolioList=driver.find_element_by_id("table-content-portfolio-equity").find_elements_by_class_name("ts-data") 
    
    #Dataset Range Variables
    startRange = 0
    endRange = 7
    
    stocks=0
    for stocks in range(len(portfolioList)): # Stocks inside of the list
        for info in range(len(portfolioList[stocks].find_elements_by_xpath('./td'))): #Individual stock properties
            individualStockInfoList.append(portfolioList[stocks].find_elements_by_xpath('./td')[info].text) #Converting into text from web element
        
        portfolioStockInfoList.append(individualStockInfoList[startRange:endRange])
        stockName.append(portfolioStockInfoList[stocks][0])
        stockUnit.append(portfolioStockInfoList[stocks][1])
        stockLivePrice.append(portfolioStockInfoList[stocks][2])
        stockAmountTL.append(portfolioStockInfoList[stocks][3])
        stockCost.append(portfolioStockInfoList[stocks][4])
        stockProfitLoss.append(portfolioStockInfoList[stocks][5])
        stockFunctions.append(portfolioStockInfoList[stocks][6])
        
        startRange = endRange
        endRange = endRange+endRange
    
    portfolioStockInfoDetailedList.append(stockName)
    portfolioStockInfoDetailedList.append(stockUnit)
    portfolioStockInfoDetailedList.append(stockLivePrice)
    portfolioStockInfoDetailedList.append(stockAmountTL)
    portfolioStockInfoDetailedList.append(stockCost)
    portfolioStockInfoDetailedList.append(stockProfitLoss)
    portfolioStockInfoDetailedList.append(stockFunctions)
    
    #Convert into dictionary for more detail.
    portfolioStockInfoDetailedDict.update({'Name' : portfolioStockInfoDetailedList[0]})
    portfolioStockInfoDetailedDict.update({'Unit' : portfolioStockInfoDetailedList[1]})
    portfolioStockInfoDetailedDict.update({'LivePrice' : portfolioStockInfoDetailedList[2]})
    portfolioStockInfoDetailedDict.update({'Amount' : portfolioStockInfoDetailedList[3]})
    portfolioStockInfoDetailedDict.update({'Cost' : portfolioStockInfoDetailedList[4]})
    portfolioStockInfoDetailedDict.update({'ProfitLoss' : portfolioStockInfoDetailedList[5]})
    
    
    updateGUIPortfolioLabels()
    
    #Alarm Label Function
    #updateGUIAlarmLabels()
    
    
    startUpdating=True



def fetchFavoriteStocksFromSite():
    #Favorite Stocks
    favStockName = driver.find_elements_by_id("equityBodyTitle")
    favStockGroup = driver.find_elements_by_id("equityTypeTitle")
    favStockLivePrice = driver.find_elements_by_id("equityBodyLastPrice") #Pzt günü güncelle(equityBodyLiveData)
    #favStockLivePrice = driver.find_elements_by_id("equityBodyLastPrice")    
    
    favStockHigh = driver.find_elements_by_id("equityBodyHighPrice")
    favStockLow = driver.find_elements_by_id("equityBodyLowPrice")
    favStockChange = driver.find_elements_by_id("equityBodyPercent")
    favStockFunctions = driver.find_elements_by_id("equityBodyOperation")

    index=0
    for index in range(len(favStockName)):
        favStockNameList.append(favStockName[index].text)
        favStockGroupList.append(favStockGroup[index].text)
        favStockLivePriceList.append(favStockLivePrice[index].text)
        favStockHighList.append(favStockHigh[index].text)
        favStockLowList.append(favStockLow[index].text)
        favStockChangeList.append(favStockChange[index].text)
        favStockFunctionsList.append(favStockFunctions[index].text)
        
        
    updateGUIFavoriteLabels()
    
    
    
def updateGUIPortfolioLabels():
    index=0
    for index in range(len(portfolioStockInfoDetailedDict['Name'])):
        nameLabelList.append(Label(alarmFrame,text=portfolioStockInfoDetailedDict['Name'][index]))
        nameLabelList[index].grid(row=index+1,column=0)
        
        unitLabelList.append(Label(alarmFrame,text=portfolioStockInfoDetailedDict['Unit'][index]))
        unitLabelList[index].grid(row=index+1,column=1)
        
        livePriceLabelList.append(Label(alarmFrame,text=portfolioStockInfoDetailedDict['LivePrice'][index]))
        livePriceLabelList[index].grid(row=index+1,column=2)
        
        amountLabelList.append(Label(alarmFrame,text=portfolioStockInfoDetailedDict['Amount'][index]))
        amountLabelList[index].grid(row=index+1,column=3)
        
        costLabelList.append(Label(alarmFrame,text=portfolioStockInfoDetailedDict['Cost'][index]))
        costLabelList[index].grid(row=index+1,column=4)
        
        
        profitLossLabelList.append(Label(alarmFrame,text=portfolioStockInfoDetailedDict['ProfitLoss'][index]))
        profitLossLabelList[index].grid(row=index+1,column=5)
        


def updateGUIFavoriteLabels():
    index=0
    for index in range(len(favStockNameList)):
        favNameLabelList.append(Label(favoriteStocksFrame,text= favStockNameList[index]))
        favNameLabelList[index].grid(row=index+1,column=0)
        favGroupLabelList.append(Label(favoriteStocksFrame,text = favStockGroupList[index]))
        favGroupLabelList[index].grid(row=index+1,column=1)
        favLivePriceLabelList.append(Label(favoriteStocksFrame,text = favStockLivePriceList[index]))
        favLivePriceLabelList[index].grid(row=index+1,column=2)
        favHighLabelList.append(Label(favoriteStocksFrame,text = favStockHighList[index]))
        favHighLabelList[index].grid(row=index+1,column = 3)
        favLowLabelList.append(Label(favoriteStocksFrame,text = favStockLowList[index]))
        favLowLabelList[index].grid(row=index+1,column = 4)
        favChangeLabelList.append(Label(favoriteStocksFrame,text = favStockChangeList[index]))
        favChangeLabelList[index].grid(row=index+1,column=5)
        setAlarmFuncWithParameter = partial(setAlarm,index)
        alarmButtonList.append(Button(favoriteStocksFrame,text="Alarm Kur",command=setAlarmFuncWithParameter))
        alarmButtonList[index].grid(row=index+1,column=6)
    
def updateGUIAlarmLabels():
    for stockIndex in range(len(alarmStockLivePriceList)):
        alarmStockLivePriceLabelList.append(Label(establishedAlarmFrame,text= favStockLivePriceList[stockIndex]))
        alarmStockLivePriceLabelList[stockIndex].grid(row=stockIndex+1,column=1)
    

        
        
def startConnectionToSite():
    #Connection
    global driver 
    driver = webdriver.Firefox()
    driver.get('https://esube1.ziraatyatirim.com.tr/sanalsube/')
    
    #Enter your TC and Password
    tcNo = "11111111111"
    password = "123456"
    
    tcBox = driver.find_element_by_id("InputCustomerNo")
    tcBox.send_keys(tcNo)
    passwordBox = driver.find_element_by_id("Passphrase")
    passwordBox.send_keys(password)
    driver.find_element_by_class_name("submit-button").click()
  
  
#------------------------------------------GUI------------------------------------------#
root = tk.Tk()
root.title("Hisse İzleme Programı")
root.geometry('1000x500')


#Create tab control object
tabControl = Notebook(root)

#Create individual tabs
connectionFrame = tk.Frame(tabControl,background="#123456")
connectionFrame.pack(side="bottom",fill="both",expand=True)
alarmFrame = tk.Frame(tabControl)
alarmFrame.pack(side="bottom",fill="both",expand=True)
favoriteStocksFrame = tk.Frame(tabControl)

#Add into tabControl
favoriteStocksFrame.pack(side="bottom",fill="both",expand=True)
tabControl.add(connectionFrame, text='Bağlantı Ekranı')
tabControl.add(alarmFrame, text='Benim Portfolyom')
tabControl.add(favoriteStocksFrame, text='Favori Hisseler')



#------------Connection Tab------------#
startConnectionLabel = tk.Label(connectionFrame,text="Bağlantıyı başlatmak için 'Bağlan' butonuna bas.")
startConnectionLabel.grid(row= 0 , column= 0,pady=1)

checkConnectionLabel = tk.Label(connectionFrame,text="Eğer bağlantı başarılı bir şekilde gerçekleştiyse 'Bağlandım' butonuna bas.")
checkConnectionLabel.grid(row= 2 , column= 0,pady=2)

startConnectionButton = tk.Button(connectionFrame,background="yellow",text ="Bağlan",command = startConnectionToSite)
startConnectionButton.grid(row=1,column=0,pady=1)

checkConnectionButton = tk.Button(connectionFrame,background="yellow",text ="Bağlandım", command = fetchPortfolioFromSite )
checkConnectionButton.grid(row=3,column=0,pady=1)




#------------------ALARM TAB------------------#

#Global Variables
isAlarmRinging = False
isAlarmActive= False
global stockLivePriceNumber
global stockTargetPriceNumber
global alarmStockName


alarmStockName= ""
alarmIndex = 0
stockLivePriceNumber=0
stockTargetPriceNumber=0

alarmDict = {}

#Established Alarm Variables #Note: Do not clear those variables with using clear function!!!!!!!!!! Delete this after alarm ringing!
alarmStockNameList = []
alarmStockLivePriceList = []
alarmStockConditionList = []
alarmStockTargetPriceList = []

#--GUI--#
alarmStockNameLabelList = []  #Sıfırlama
alarmStockLivePriceLabelList = [] #GÜNCELLE!
alarmStockConditionLabelList = [] #Sıfırlama
alarmStockTargetPriceLabelList = [] #Sıfırlama




#Alarm Button Function
def setAlarm(stockIndex):
    global stockLivePriceNumber
    global alarmStockName
    global alarmIndex
    #stockLivePriceNumber = float(favStockLivePriceList[stockIndex])
    stockLivePriceNumber  = float(favStockLivePriceList[stockIndex])
    alarmStockName = favStockNameList[stockIndex]
    alarmIndex = stockIndex
    #print(stockLivePriceNumber)
    print("Seçilen hisse adı"+alarmStockName)
    alarmDict.update({alarmStockName:stockLivePriceNumber})
    
    
  
def alarmUpdateFunc():
    global isAlarmActive
    for stockIndex in range(len(alarmStockNameList)):
        livePrice = float(favStockLivePriceList[stockIndex])
        targetPrice = float(alarmStockTargetPriceList[stockIndex])
        
        if livePrice == targetPrice:
            print("HEDEFE ULAŞILDI!")
            isAlarmActive=True
  


    
    
#------PORTFOLIO FRAME------#

stockLabel = tk.Label(alarmFrame,text="Hisse")
stockLabel.grid(row= 0 , column= 0,padx=5)

unitLabel = tk.Label(alarmFrame,text="Adet")
unitLabel.grid(row= 0 , column= 1,padx=5)

livePriceLabel = tk.Label(alarmFrame,text="Canlı Fiyat")
livePriceLabel.grid(row= 0 , column= 2,padx=5)

amountLabel = tk.Label(alarmFrame,text="Tutar")
amountLabel.grid(row= 0 , column= 3,padx=5)

costLabel = tk.Label(alarmFrame,text="Maliyet")
costLabel.grid(row= 0 , column= 4,padx=5)

profitlossLabel = tk.Label(alarmFrame,text="Kar/Zarar")
profitlossLabel.grid(row= 0 , column= 5,padx=5)


#-----FAVORITE STOCKS FRAME-----#

favStockNameLabel = tk.Label(favoriteStocksFrame, text="Hisse")
favStockNameLabel.grid(row=0,column=0,padx=5)
favStockGroupLabel = tk.Label(favoriteStocksFrame, text="Grup")
favStockGroupLabel.grid(row=0,column=1,padx=5)
favLivePricesLabel = tk.Label(favoriteStocksFrame, text="Canlı Fiyat")
favLivePricesLabel.grid(row=0,column=2,padx=5)
favStockHighLabel = tk.Label(favoriteStocksFrame, text="Yüksek")
favStockHighLabel.grid(row=0,column=3,padx=5)
favStockLowLabel = tk.Label(favoriteStocksFrame, text="Düşük")
favStockLowLabel.grid(row=0,column=4,padx=5)
favStockChangeLabel = tk.Label(favoriteStocksFrame, text="Değişim %")
favStockChangeLabel.grid(row=0,column=5,padx=5)

alarmLabel = tk.Label(favoriteStocksFrame,text="Alarm")
alarmLabel.grid(row=0,column=6,padx=5)


    
    
#Button Function
def getTargetPriceNumber():
    global stockTargetPriceNumber
    global stockLivePriceNumber
    stockTargetPriceNumber = float(targetPriceEntry.get())
    alarmStockNameList.append(alarmStockName)
    alarmStockLivePriceList.append(stockLivePriceNumber)
    alarmStockTargetPriceList.append(stockTargetPriceNumber)
    
    selectedCondition = conditionListBox.curselection()
    for condition in selectedCondition:
        conditionName= conditionListBox.get(condition)
        alarmStockConditionList.append(conditionName)
        
        
    ###
    stockIndexPosition=len(alarmStockNameList)-1
    stockIndex=alarmIndex
    
    
    #Labels
    alarmStockNameLabelList.append(Label(establishedAlarmFrame,text= alarmStockNameList[stockIndex]))
    alarmStockNameLabelList[stockIndex].grid(row=stockIndexPosition+1,column=0)
    alarmStockLivePriceLabelList.append(Label(establishedAlarmFrame,text= favStockLivePriceList[stockIndex])) #Fetch this data from live data!
    alarmStockLivePriceLabelList[stockIndex].grid(row=stockIndexPosition+1,column=1)
    alarmStockConditionLabelList.append(Label(establishedAlarmFrame,text=alarmStockConditionList[stockIndex]))
    alarmStockConditionLabelList[stockIndex].grid(row=stockIndexPosition+1,column=2)
    alarmStockTargetPriceLabelList.append(Label(establishedAlarmFrame,text=str(alarmStockTargetPriceList[stockIndex])))
    alarmStockTargetPriceLabelList[stockIndex].grid(row=stockIndexPosition+1,column=3)
    


#--------------Set Alarm Frame------------------#

setAlarmFrame = tk.Frame(tabControl)
setAlarmFrame.pack(side="bottom",fill="both",expand=True)

establishedAlarmFrame = tk.Frame(tabControl)
establishedAlarmFrame.pack(side="bottom",fill="both",expand=True)

tabControl.add(setAlarmFrame, text='Alarm Kur')
tabControl.add(establishedAlarmFrame, text='Kurulmuş Alarmlar')


targetPriceLabel = Label(setAlarmFrame,text="Fiyatı giriniz= ")
targetPriceLabel.grid(row=0,column=0,padx=5,pady=5)

targetPriceEntry = Entry(setAlarmFrame)
targetPriceEntry.grid(row=0,column=1,padx=5,pady=6)

conditionListBox = tk.Listbox(setAlarmFrame)
conditionListBox.insert(1,"Küçükse hatırlat")
conditionListBox.insert(2,"Küçük eşitse hatırlat")
conditionListBox.insert(3,"Eşitse hatırlat")
conditionListBox.insert(4,"Büyük eşitse hatırlat")
conditionListBox.insert(5,"Büyükse hatırlat")

targetPriceButton = Button(setAlarmFrame,text="Kur",command=getTargetPriceNumber)
targetPriceButton.grid(row=2,column=1)

#------------------------------------------------#


#*------Established Alarm Frame-------------#

alarmStockNameLabel = Label(establishedAlarmFrame,text="Hisse Adı").grid(row=0,column=0)
alarmStockLivePriceLabel = Label(establishedAlarmFrame,text = "Canlı Fiyat").grid(row=0,column=1)
alarmStockConditionLabel = Label(establishedAlarmFrame, text ="Alarm Türü").grid(row=0,column=2)    
alarmStockTargetPriceLabel = Label(establishedAlarmFrame,text="Kurulan Fiyat").grid(row=0,column=3)

#------------------------------------------#

#-----AUDIO-----#
song = AudioSegment.from_wav("shipAlarm.wav")

def ringTheAlarm():
    global isAlarmActive
    counter= 3
    while (counter>0):
        play(song)
        time.sleep(0.1)
        counter= counter -1
    alarmInfo = tk.messagebox.askquestion("Alarm Bilgisi",message="Alarmı kapatmak için 'Evet' tuşuna basınız.")
    if alarmInfo == 'yes':
        print("EVET DEDİİİ")
        isAlarmActive = False
    else:
        isAlarmActive = True
    
    
#-------------#


def fetchDataAutomatically(): #Every seconds it fetches data from the site
    alarmUpdateFunc()
    if isAlarmActive:
        ringTheAlarm()
        root.after(2000,fetchDataAutomatically)
        
    # for stockInfo in range(len(alarmStockNameList)):
    #     print("Alarm kurulan hisse"+alarmStockNameList[stockInfo]+" Canlı Fiyatı"+str(alarmStockLivePriceList[stockInfo]) + " Alarm Fiyatı" + str(alarmStockTargetPriceList[stockInfo]))
       
    if startUpdating:
        fetchPortfolioFromSite() #Fetch data in seconds
        refleshButton.click() #Reflesh the site for not disconnect
                                
    root.after(2000,fetchDataAutomatically)
    
root.after(2000,fetchDataAutomatically)

conditionListBox.grid(row=1,column=1,pady=5)
tabControl.pack(expand=1, fill='both')
root.mainloop()





        
