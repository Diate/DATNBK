# LIBRARY IMPORT
from opcua import Server,ua, uamethod
from random import randint
import pyodbc
import time
import ctypes

# MODULE USER DEFINE
import SQL.Sql_res_connect as sqlres
import SQL.Sql_req_connect as sqlreq
from Varialble.Var_res_define import Stt,TufID,Origin,DeclareMass,RealMass,Error,Destination,Typep,DateSent,Datehandle,Status,getIf
from Varialble.Var_req_define import Sttsr,TufIDsr,Originsr,DeclareMasssr,RealMasssr,Errorsr,Destinationsr,Typepsr,DateSentsr,Datehandlesr,Statussr,getIfsr
# from PreProcess.Getdata_from_PLC import U,I,Duty,N,Up,Down
# IMPORT LIBRARY PREPROCESS
from Rount.OPC_connect import param_getInfo
from Rount.OPC_connect import add_space
# IMPORT LIBRARY ANN
from keras import models
import pandas as pd
import numpy as np
import pickle
# END IMPORT LIBRARY


def Getdata(count,vargetIf,old_condi):
    if(vargetIf != old_condi):
        count = 0
        open('Data.txt', 'w').close()
    while (count<=10):
        files = open('Data.txt', 'a')
        U_get = U.get_value()
        I_get = I.get_value()
        Duty_get = Duty.get_value()
        N_get = N.get_value()
        Up_get = Up.get_value()
        Down_get = Down.get_value()
        N_set_get = N_set.get_value()
        # condition = (U_get!=U_old)or(Up_get!=Up_old)or(Down_get!=Down_old)or(N_get!=N_old)or(I_get!=I_old)or(Duty_get!=Duty_old)
        if(((Up_get!=0)or(Down_get!=0))and(int(N_get)!=0)and(int(N_set_get)!=0)and(int(N_get)>(int(N_set_get)-15))and(int(N_get)<(int(N_set_get)+15))):
            files.write(str(U_get)+","+str(I_get)+","+str(N_get)+","+str(Duty_get)+"\n")
            count = count + 1
        time.sleep(0.3)
        files.close()  
    if (count == 10):
        count = 11
    old_condi = vargetIf  
    return count
def ANN(count):
    if count == 11:
        df = pd.read_csv('Data.txt',sep=",")
        df.columns = ['U','I','N','Duty']
        df = df[['U','I','N','Duty']]
        df['Duty'] = df['Duty'].apply(lambda x: (5000-x)/5000)
        df['U'] = df['U']*df['Duty']
        # --------------------------------------------
        model_Part1 = models.load_model("Part1_12_06.h5")
        y_predict_test=model_Part1.predict(df, batch_size=1)
        fn_result = np.mean(y_predict_test)*1000
        fn_result = round(fn_result,2)
    return fn_result

# CALL VAR PREPROCESS 
U = param_getInfo.add_variable(add_space, "U", 0)
I = param_getInfo.add_variable(add_space, "I", 0)
Duty = param_getInfo.add_variable(add_space, "Duty", 0)
N = param_getInfo.add_variable(add_space, "N", 0)
Up = param_getInfo.add_variable(add_space, "Up", 0)
Down = param_getInfo.add_variable(add_space, "Down", 0)
N_set = param_getInfo.add_variable(add_space, "N_set", 0)
U.set_writable()
I.set_writable()
Duty.set_writable()
N.set_writable()
Up.set_writable()
Down.set_writable()
N_set.set_writable()
old_condi = ""
count = 0

# Var define Infinity
IDget = "UNKNOWN"
oldID = "None"
varSTT = 0
varID = "Unknown"
varOrigin = "Unknown"
varDeclareMass = 0
varRealMass = 0
varError = 0
varDestination = "Unknown"
varType = "Unknown"
varDateSent = "**/**/****"
varDatehandle = "**/**/****"
varStatus = "Unknown"
vargetIf = "BSOU3208"
old_vargetIf = "UNKNOWN"

IDgetsr = "UNKNOWNS"
oldIDsr = "None"
varSTTsr = 0
varIDsr = "Unknown"
varOriginsr = "Unknown"
varDeclareMasssr = 0
varRealMasssr = 0
varErrorsr = 0
varDestinationsr = "Unknown"
varTypesr = "Unknown"
varDateSentsr = "**/**/****"
varDatehandlesr = "**/**/****"
varStatussr = "Unknown"
vargetIfsr = "BSOU3208"
# IDget = ""
old_vargetIfsr = "UNKNOWNS"
while True:
    vargetIf = getIf.get_value()
    if (vargetIf == 0):
        vargetIf = "UNKNOWN"
    if vargetIf != old_vargetIf :
        print(vargetIf,old_vargetIf)   
            # Home condition 
        if vargetIf != 0 :
            IDget = str(vargetIf)
        temp = sqlres.sql(IDget)
        
        for x in range(len(temp)-1):
            temp[x] = str(temp[x])
        [varSTT,varID,varOrigin,varDeclareMass,varRealMass,varError,varDestination,varType,varDateSent,varDatehandle,varStatus]=temp        
        if(varID=="ERRORQRS"):
            varQR = 1
        else: 
            varQR = 0
        biendem = Getdata(count,vargetIf,old_condi)
        # biendem = 11
        massR = ANN(biendem)
        varRealMass = massR
        # Hometab send-get data
        # Stt.set_value(varSTT)
        Stt.set_value(varQR)
        TufID.set_value(varID)
        Origin.set_value(varOrigin)
        DeclareMass.set_value(varDeclareMass)
        RealMass.set_value(varRealMass)
        Error.set_value(varError)
        Destination.set_value(varDestination)
        Typep.set_value(varType)
        DateSent.set_value(varDateSent)
        Datehandle.set_value(varDatehandle)
        Status.set_value(varStatus)
        # vargetIf = getIf.get_value()
        old_vargetIf = vargetIf
        
    vargetIfsr = getIfsr.get_value()
    # print("------------------------")
    
    if (vargetIfsr == 0):
        vargetIfsr = "UNKNOWNS"
    # print(vargetIfsr,old_vargetIfsr)
    if (vargetIfsr != old_vargetIfsr):
        if vargetIfsr != 0 :
            IDgetsr= str(vargetIfsr) 
        tempsr = sqlreq.sqlsr(IDgetsr)
        for x in range(len(tempsr)-1):
            tempsr[x] = str(tempsr[x]) 
        [varSTTsr,varIDsr,varOriginsr,varDeclareMasssr,varRealMasssr,varErrorsr,varDestinationsr,varTypesr,varDateSentsr,varDatehandlesr,varStatussr]=tempsr   
        # Searchtab send-get data
        Sttsr.set_value(varSTTsr)
        TufIDsr.set_value(varIDsr)
        Originsr.set_value(varOriginsr)
        DeclareMasssr.set_value(varDeclareMasssr)
        RealMasssr.set_value(varRealMasssr)
        Errorsr.set_value(varErrorsr)
        Destinationsr.set_value(varDestinationsr)
        Typepsr.set_value(varTypesr)
        DateSentsr.set_value(varDateSentsr)
        Datehandlesr.set_value(varDatehandlesr)
        Statussr.set_value(varStatussr)
        old_vargetIfsr = vargetIfsr
        # vargetIfsr = getIfsr.get_value()
    # Search condition 
    # print(varSTT,varID,varOrigin,varDeclareMass,varRealMass,varError,varDestination,varType,varDateSent,varDatehandle,varStatus)
    time.sleep(0.5)