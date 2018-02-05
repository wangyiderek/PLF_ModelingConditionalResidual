# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 11:01:49 2018

@author: thuzhang
"""

#Using
import xlrd
import numpy as np
import csv

def createListCSV(fileName="", dataList=[]):
    with open(fileName, "w",newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerows(dataList)
        
originData =xlrd.open_workbook('smd_hourly_ME_Output_13_16.xls')
names=originData.sheet_names()



for index in range(0,len(names)):
#    outputFiles=xlwt.Workbook()
#    outputSheets=outputFiles.add_sheet('DATA',cell_overwrite_ok=True)
    
    originDataTable =originData.sheets()[index]
    nrows=originDataTable.nrows
    ncols=originDataTable.ncols
    
    resultMatrix=[]
    nameColumn=[]
    for i in range(1,nrows):
        resultList=[]
        
        #DateInfo
        rowValues=originDataTable.row_values(i)
        hour=0
        hour=int(rowValues[1])
        x=xlrd.xldate_as_tuple(originDataTable.cell_value(i,0),0)
        y=xlrd.xldate.xldate_as_datetime(originDataTable.cell_value(i,0),0).weekday()
        year=x[0]
        month=x[1]
        day=x[2]
        weekday=y
        DEMAND=rowValues[3]
        
        dateInfoList=[DEMAND,month,day,weekday,hour]        
        resultList=dateInfoList
        

           
        loadInfo=[]
        tempInfo=[]

        LoadColumn=[]
        tempNameColumn=[]
        for formerDaysHours in [24,25,47,48,49,72,96]:
            loadInfo.append(originDataTable.cell_value(i-formerDaysHours,3))
        tempInfo.append(originDataTable.cell_value(i,12))
        tempInfo.append(originDataTable.cell_value(i,13))
            
        for formerDaysHours in [24,25,47,48,49,72,96]:
            while i==1:
                LoadColumn.append('Demand%d'%(formerDaysHours))
                break
        tempNameColumn.append('DB')
        tempNameColumn.append('DP')
#        for index in range(2,8):
#            loadInfo.append(originDataTable.cell_value(i-24*index,3))
#            tempdbInfo.append(originDataTable.cell_value(i-24*index,12))
#            tempdpInfo.append(originDataTable.cell_value(i-24*index,13))
        while i==1:
            dateColumn=['Demand','month','day','weekday','hour']
            dateColumn.extend(LoadColumn)
            dateColumn.extend(tempNameColumn)
            resultMatrix.append(dateColumn)
            break
        
        if i<=8*24+2:
            continue
        
        resultList.extend(loadInfo)
        resultList.extend(tempInfo)
        resultMatrix.append(resultList) 

        print(resultList[:8])
    createListCSV('%s.csv'%names[index],resultMatrix)
    print("Saved %s"%names[index])
    
            
            
            
            
    