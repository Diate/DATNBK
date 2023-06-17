from keras import models
import pandas as pd
import numpy as np
import pickle
# X_test = pd.read_csv("X_train2.csv",sep=";")
# --------------------------------------------
df = pd.read_csv('Data.txt',sep=",")
df.columns = ['U','I','N','Duty']
df = df[['U','I','N','Duty']]
df['Duty'] = df['Duty'].apply(lambda x: (5000-x)/5000)
df['U'] = df['U']*df['Duty']
# --------------------------------------------
model_Part1 = models.load_model("Part1_12_06.h5")
y_predict_test=model_Part1.predict(df, batch_size=1)
print(y_predict_test)
# y_predict_test = np.concatenate(y_predict_test)
# X_test['Predict'] = y_predict_test
# model_Part2 = pickle.load(open('Part2.sav', 'rb'))
# Y_result = model_Part2.predict(X_test)
A = np.mean(y_predict_test)*1000
print(A)

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
        # if(((Up_get!=0)or(Down_get!=0))and(N_get!=0)):
        if(1):
            files.write(str(U_get)+","+str(I_get)+","+str(N_get)+","+str(Duty_get)+","+str(Up_get)+","+str(Down_get)+","+"\n")
            count = count + 1
        time.sleep(0.2)
        files.close()
    if (count == 10):
        count = 11
    old_condi = vargetIf  
    return count
def ANN(count):
    if count == 11:
        X_test = pd.read_csv("X_train2.csv",sep=";")
        model_Part1 = models.load_model("Part1.h5")
        y_predict_test=model_Part1.predict(X_test, batch_size=1)
        y_predict_test = np.concatenate(y_predict_test)
        print(y_predict_test)
        X_test['Predict'] = y_predict_test
        model_Part2 = pickle.load(open('Part2.sav', 'rb'))
        Y_result = model_Part2.predict(X_test)
        fn_result = np.mean(Y_result)
        fn_result = round(fn_result,2)
    return fn_result