import pandas as pd
import cx_Oracle as co
import os
import xlsxwriter
import CreateBasicScript as basic
import InsertProjectEntry as projectEntry
import UpdateProjectNumber as updateProj
import UpdatePhxJobTest as phxJobTest
import ProjectContract as projContr
import Connection as con

def readExcel():
    con.os.chdir(con.currentDir)
    xls = pd.ExcelFile('InputPSFTFile.xlsx')
    df1 = pd.read_excel(xls, 'Activity_Count')
    df2 = pd.read_excel(xls, 'Activity_Mapping')
    df2 = df2.dropna(how='all');
    psftLineItems = df2.groupby('GIN')['Activity ID'].apply(lambda x: x.values.tolist()).to_dict()
    
    return psftLineItems


def compareData(psftItems,phxItems):
    compareDict = {}
    # in dic.items():
    for k, v in phxItems.items():
        dummyList = []
        for val in v:
            dummyList.append(val[1])
        compareDict[k] = dummyList    

    diffDict = {}
    for k,v in psftItems.items():
        for nk,nv in compareDict.items():
            if(k == nk):
                l = [x for x in v if x not in nv]
                diffDict[k] = l

    finalDict = {}
    for k in diffDict:
        if diffDict[k]:
            finalDict[k] = diffDict[k]

    return finalDict

def checkPhxTestSent(psftItems,phxItems):
    compareDict = {}
    for (fk,fv),(pk,pv) in zip(psftItems.items(),phxItems.items()):
        if(fk == pk):
            dummyList=[]
            for fval,pval in zip(fv,pv):
                if((float(fval) == float(pval[1])) &(pval[3] != 'SENT')):
                    dummyList.append(pval[0])
            if(dummyList):
                compareDict[fk]=dummyList

    return compareDict

def checkProject(psftItems):
    try:
        c = con.conn.cursor()
        noprojectExistence =[]
        sql = 'select * from PHX_PROJECT where PROJECT_NUMBER=:gin'
        dummyList = []
        for ginIt in psftItems:
            result=c.execute(sql,gin=ginIt)
            for row in result:
                if(row):
                    dummyList.append(ginIt)
            if ginIt not in dummyList:
                noprojectExistence.append(ginIt)
                
    except Exception as e:
        print(e)
##    finally:
##        con.conn.close()

    return noprojectExistence

def getPhoenixLineItems(psftLineItems_dict):
    try:
        c = con.conn.cursor()
        sql = 'select id,line_number, master_id, update_flag FROM PHX_JOB_TEST WHERE JOB_SERVICE_LEVEL_ID IN  (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER IN(SELECT JOB_NUMBER FROM phx_job_order where gin = :gin and TYPE=:type)) order by line_number'
        phxLineItems_dict = {}
        
        for ginIt in psftLineItems_dict:
            list_data=[]
            result=c.execute(sql,gin=ginIt,type='PRODUCT')
            for row in result:
                list_data.append(row)
            phxLineItems_dict[ginIt]= list_data

        phxLineItems_dict1 = phxLineItems_dict
        newDict = {}
        for (k,v),(k1,v1) in zip(phxLineItems_dict.items(),phxLineItems_dict1.items()):
            currId = 0
            denomId = 0
            newValList = []
            for val in v:
                newVal = [val[0],float(val[1]),val[2],val[3]]
                for val1 in v1:
                    if (val[2] == val1[0]):
                        newVal[1] = val1[1] + val[1]*(0.1)
                newValList.append(newVal)
            newDict[k] = newValList
          
    except Exception as e:
        print(e)
##    finally:
##        con.conn.close()
    return newDict

def deletePsftExport(psftExtra_dict):
    workbook = xlsxwriter.Workbook(r'''C:\Users\vinay.b.bhardwaj\Downloads\Python Practice\deleteItemPSFT.xlsx''') 
    worksheet = workbook.add_worksheet()
    row = 1
    columnk = 0
    columnv = 1
    worksheet.write(0, 0, 'GIN')
    worksheet.write(0, 1, 'Line Item to be deleted')
    for k,v in psftExtra_dict.items():
        worksheet.write(row, columnk, k)
        colNew = columnv
        for vval in v:
            worksheet.write(row, colNew, vval)
            colNew+=1
        row+=1
    workbook.close()
    print('deleteItemPSFT.xlsx exported successfully')

def checkProjNumNull(psftItems):
    try:
        c = con.conn.cursor()
        noprojectNumExistence =[]
        sql = 'SELECT project_number FROM PHX_JOB_ORDER WHERE GIN IN (:gin)'
        for ginIt in psftItems:
            result=c.execute(sql,gin=ginIt)
            for row in result:
                if row[0] is None:
                    noprojectNumExistence.append(ginIt)
                
    except Exception as e:
        print(e)
##    finally:
##        con.conn.close()

    return noprojectNumExistence

def checkProjectContractFlag(psftItems,file):
    try:
        c = con.conn.cursor()
        flagNoSent =[]
        dummyList=[]
        sql = 'SELECT JOB_NUMBER,ESB_DATE,ESB_FLAG FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in (:gin))'
        for ginIt in psftItems:
            result=c.execute(sql,gin=ginIt)

            if(result):
                for row in result:
                    dummyList.append(ginIt)
                    if (row[2] != 'SENT'):
                        flagNoSent.append(ginIt)
                        
        for ginIt in psftItems:
            if ginIt not in dummyList:
                file = projContr.insertIntoProjContrFlag(ginIt,file)
            
                
    except Exception as e:
        print(e)
##    finally:
##        con.conn.close()

    return flagNoSent,file

def main():
    try:
        psftLineItems_dict=readExcel()
        phxLineItems_dict = getPhoenixLineItems(psftLineItems_dict)

        psftExtra_dict = compareData(psftLineItems_dict,phxLineItems_dict)

        if psftExtra_dict:
            for x,y in psftExtra_dict.items():
                    for k,v in psftLineItems_dict.items():
                        if x==k:
                            for val in y:
                                v.remove(val) #for removing items not present in PHX
                                
            deletePsftExport(psftExtra_dict)

        fileName = 'SQL.sql'
        file = open(fileName,'w+')
        file = basic.createBasicScript(file)
        
        missingProjectGins_list = checkProject(psftLineItems_dict) #(1)
        file = projectEntry.insertProjectEntry(missingProjectGins_list,file)
        
        projNumNullGins_list = checkProjNumNull(psftLineItems_dict) #(2)
        file = updateProj.updateProjNum(projNumNullGins_list,file)
        
        unsentPhxTest_dict = checkPhxTestSent(psftLineItems_dict,phxLineItems_dict) #(3)
        file = phxJobTest.setFlagSentPhxTest(unsentPhxTest_dict,file)

        flagNoSent,file = checkProjectContractFlag(phxLineItems_dict,file) #(4)
        if(flagNoSent):
            file = projContr.setFlagNew(flagNoSent,file)

        file = basic.createBasicScriptFooter(file)
        
        file.close()
        con.conn.close()
        
    except Exception as e:
        print(e)
    
    
if __name__ == "__main__":
    main()
