# import pyodbc
# def sqlsr(IDgetsr):
#     conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-E2PGTAG\SQLEXPRESS2019; Database=SQLDB; UID=dh; PWD=31052001')
#     IDss = str(IDgetsr)
#     IDss = "'" + IDss + "'"
#     cursor = conx.cursor()
#     select = "select * from dboData where ID = " + IDss + " AND Status = 'Done'"
#     cus = cursor.execute(select)
#     for row in cus:
#         print(str(row)) 
#     conx.close()
#     return row
import pyodbc
def sqlsr(IDgetsr):
    conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-E2PGTAG\SQLEXPRESS2019; Database=SQLDB; UID=dh; PWD=31052001')
    IDss = str(IDgetsr)
    IDss = "'" + IDss + "'"
    cursor = conx.cursor()
    select = "select * from dboData where ID = " + IDss + " AND Status = 'Done'"
    cus = cursor.execute(select)
    row = cursor.fetchone()
    if(str(type(row))=="<class 'pyodbc.Row'>"):
        for row in cus:
            pass
    else:
        select = "select * from dboData where ID = 'UNKNOWNS' AND Status = 'Done'"
        cus = cursor.execute(select)
        for row in cus:
            pass
    print(row)
    conx.close()
    return row