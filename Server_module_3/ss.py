import pyodbc
IDgetsr = "4545"
conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-E2PGTAG\SQLEXPRESS2019; Database=SQLDB; UID=dh; PWD=31052001')
IDss = str(IDgetsr)
IDss = "'" + IDss + "'"
cursor = conx.cursor()
select = "select * from dboData where ID = " + IDss

cus = cursor.execute(select)
row = cursor.fetchone()
# print(row)
if(str(type(row))=="<class 'pyodbc.Row'>"):
    for row in cus:
        # print(str(row))
        pass
else:
    select = "select * from dboData where ID = 'ERRORQRS'"
    cus = cursor.execute(select)
    for row in cus:
        # print(str(row))
        pass
print(row)
conx.close()

