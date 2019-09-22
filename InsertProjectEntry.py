import Connection as con


def insertProjectEntry(missingProjectGins_list,file):
    sql = 'SELECT JO.GIN PROJECT_NUMBER,JO.BRANCH_NAME,JO.BU_NAME,JC.CUSTOMER_CODE,JO.DESCRIPTION,JO.JOB_NUMBER,JO.PROJECT_MANAGER_NAME,JO.ORDER_STATUS,jo.Project_type TYPE from phx_job_order jo,phx_job_contract jc where jo.job_number=jc.job_order_number and jo.gin=:gin'
    c = con.conn.cursor()
    for gins in missingProjectGins_list:
        selectionString = '''SELECT COUNT(*) FROM PHX_PROJECT WHERE PROJECT_NUMBER = GINSET;'''
        insertionString = '''INSERT INTO PHX_PROJECT (PROJECT_NUMBER,BRANCH_NAME,BU_NAME,CUSTOMER_CODE,DESCRIPTION,JOB_NUMBER,PROJECT_MANAGER_NAME,ORDER_STATUS,TYPE) 
values (PROJECT_NUMBER_VAL,BRANCH_NAME_VAL,BU_NAME_VAL,CUSTOMER_CODE_VAL,DESCRIPTION_VAL,JOB_NUMBER_VAL,PROJECT_MANAGER_NAME_VAL,ORDER_STATUS_VAL,TYPE_VAL);'''
        result=c.execute(sql,gin=gins)
        for row in result:
            selectionString = selectionString.replace('GINSET','\''+row[0]+'\'')
            insertionString = insertionString.replace('PROJECT_NUMBER_VAL','\''+row[0]+'\'')
            insertionString = insertionString.replace('BRANCH_NAME_VAL','\''+row[1]+'\'')
            insertionString = insertionString.replace('BU_NAME_VAL','\''+row[2]+'\'')
            insertionString = insertionString.replace('CUSTOMER_CODE_VAL','\''+row[3]+'\'')
            insertionString = insertionString.replace('DESCRIPTION_VAL','\''+str(row[4])+'\'')
            insertionString = insertionString.replace('JOB_NUMBER_VAL','\''+row[5]+'\'')
            insertionString = insertionString.replace('PROJECT_MANAGER_NAME_VAL','\''+row[6]+'\'')
            insertionString = insertionString.replace('ORDER_STATUS_VAL','\''+row[7]+'\'')
            insertionString = insertionString.replace('TYPE_VAL','\''+row[8]+'\'')

        file.write('\n--Inserting into PHX_PROJECT for gin number '+gins+'\n\n')
        file.write(selectionString+'\n')
        file.write(insertionString)
        file.write('\n\n')

    return file
