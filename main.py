
# This code is for Probabilistic Load Forecasting by Modeling Conditional Residual.
## Includes
### Basics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import datetime

### Models
from sklearn.ensemble import GradientBoostingRegressor


def multiQuantile(File):

    ## Basics
    def Width(b,c,alpha):
        res=[]
        for i in range(0,len(b)):
            r=b[i]*(1+alpha)-c[i]*(1-alpha)
            res.append(r)
        print('Width:%f'%np.mean(res))
        return res
    
    def trainTestSplit(X,start=0,mid=0.8,fin=10):
        train=X[start:mid]
        forecast=X[mid:fin]
        final=X[fin:]
        return train,forecast,final
    
    def trainTestSplitSingle(X,mid=0):
        train=X[:mid]
        test=X[mid:]
        return train,test
        
    def XandYsplit(X):
        return X.iloc[:,1:],X.iloc[:,0]
    
    def MAPE(X,Y):
        count=len(X)
        Error=[]
        for i in range(0,count):
            try:
                Error.append(1-X[i]/Y[i])
            except:
                continue
        print('MAPE:%f'%np.mean(np.abs(Error)))
        return np.mean(np.abs(Error))
    
    def PICP(H,L,a):
        length=len(H)
        picp=0
        for i in range(0,length):
            if H[i]>=a[i] and L[i]<=a[i]:
                picp+=1
        picp=picp/length
        print('PIPC:%f'%picp)
        return picp
    
    ## IO
    OriginData=pd.read_table(File,sep=",",index_col=False)
    
    train,predict,test= trainTestSplit(OriginData,0,365*24*2,365*24*3)
    X_train,y_train=XandYsplit(train)
    X_predict,y_predict=XandYsplit(predict) 
    X_test,y_test=XandYsplit(test)  
    
    clf=GradientBoostingRegressor
    model=clf().fit(X_train,y_train)
    
    selfPredict=model.predict(X_predict)
    residList=y_predict-selfPredict
    
    X_predict.insert(0,'pointPredict',selfPredict)
    
    namesCol=['Real','PointPre']
    qclfList=[]
    for i in range(1,21,2):
        qclfList.append(clf(loss='quantile',alpha=i/20).fit(X_predict,residList))
        namesCol.append('Quant%.2f'%(i/20))
    
    pointPreResult=list(model.predict(X_test))
    
    X_testNew=copy.deepcopy(X_test)
    X_testNew.insert(0,'pointPredict',pointPreResult)
    
    qpreResult=[]
    qpreResult.append(list(y_test))
    qpreResult.append(pointPreResult)
    for i,item in enumerate(qclfList):
        _qResult=(list(item.predict(X_testNew)+pointPreResult))
        qpreResult.append(_qResult)
    
    qreDataFrame=pd.DataFrame(data=np.matrix(qpreResult).T,columns=namesCol)
    qreDataFrame.to_csv(r'quantileResult\\quantilePre%s'%File)
    
    # Index
    def Figure(a=[],b=[],c=[],d=[],startHour=0,endHour=0):
        print('--------------------------------')
        print('Plot start from',startHour,'to',endHour,'hours')
        plt.figure(figsize=(18,5))
        plt.xlabel('Hour/h')
        plt.ylabel('Power demand/MW')
        plt.plot(c[startHour:endHour],'green',label='Real Value')
        plt.plot(d[startHour:endHour], color='blue',label="Point Forecast")
        plt.plot(a[startHour:endHour],'gray',label='Upper Bound')
        plt.plot(b[startHour:endHour],'orange',label='Lower Bound')
        plt.legend(loc='best')
        plt.show()
        Width(a,b,0)
        PICP(a,b,c)
        MAPE(d,c)
        print('--------------------------------')
        print('--------------------------------')
    
    ## Single Regression
    singleTrain,singleTest=trainTestSplitSingle(OriginData,3*365*24)
    X_trainSingle,y_trainSingle=XandYsplit(singleTrain)
    X_testSingle,y_testSingle=XandYsplit(singleTest) 
    
    namesColSingle=['Real','PointPre']
    qclfListSingle=[]
    for i in range(1,21,2):
        qclfListSingle.append(clf(loss='quantile',alpha=i/20).fit(X_trainSingle,y_trainSingle))
        namesColSingle.append('Quant%.2f'%(i/20))
    
    modelSingle=clf().fit(X_trainSingle,y_trainSingle)
    pointPreResultSingle=list(modelSingle.predict(X_testSingle))
    
    qpreResultSingle=[]
    qpreResultSingle.append(list(y_testSingle))
    qpreResultSingle.append(pointPreResultSingle)
    for i,item in enumerate(qclfListSingle):
        _qResult=(list(item.predict(X_test)))
        qpreResultSingle.append(_qResult)
    
    qreDataFrameSingle=pd.DataFrame(data=np.matrix(qpreResultSingle).T,columns=namesColSingle)
    qreDataFrameSingle.to_csv(r'quantileResult\\quantilePreSingle%s'%File)
    
    print('Two Level Regression, File:%s'%File)
    Figure(list(qreDataFrame.iloc[:,11]),list(qreDataFrame.iloc[:,2]),
           list(qreDataFrame.iloc[:,0]),list(qreDataFrame.iloc[:,1])
           ,0*30*24,1*30*24)
    
    print('Single Regression, File:%s'%File)
    Figure(list(qreDataFrameSingle.iloc[:,11]),list(qreDataFrameSingle.iloc[:,2]),
           list(qreDataFrameSingle.iloc[:,0]),list(qreDataFrameSingle.iloc[:,1])
           ,0*30*24,1*30*24)
        
    
fileSet=['CT.csv','ME.csv','NEMASSBOST.csv','NH.csv','RI.csv','SEMASS.csv',
         'VT.csv','WCMASS.csv','ISONE CA.csv']    

for item in fileSet:
    starttime = datetime.datetime.now()
    multiQuantile(item)
    endtime = datetime.datetime.now()
    print('Time used:%d s'%((endtime-starttime).seconds))
    
    
            