import Connection as con

def insertIntoProjContrFlag(gin,file):
    
    selectionString = 'SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in (\''+gin+'\'));'
    insertionString = 'INSERT INTO PHX_PROJECT_CONTRACT_FLAG (JOB_NUMBER,ESB_DATE,ESB_FLAG) VALUES (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in (\''+gin+'\'),sysdate,\'NEW\');'
    
    file.write('\n--Inserting into PHX_PROJECT_CONTRACT_FLAG for gin number '+gin+'\n\n')
    file.write(selectionString+'\n')
    file.write(insertionString)
    file.write('\n\n')

    return file

def setFlagNew(flagNoSent,file):
    c = con.conn.cursor()
    for gin in flagNoSent:
        selectionString = 'SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in (\''+gin+'\'));'
        updationString = 'UPDATE PHX_PROJECT_CONTRACT_FLAG SET ESB_FLAG=\'NEW\' WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in (\''+gin+'\'));'

        result = c.execute('SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in (\''+gin+'\'))')
        for row in result:
            count=row
        
        file.write('\n--Updating the ESB_FLAG to NEW in PHX_PROJECT_CONTRACT_FLAG for gin number '+gin+'\n\n')
        file.write('\n--Count of rows to be updated = '+str(count[0])+'\n')
        file.write(selectionString+'\n')
        file.write(updationString)
        file.write('\n\n')

    return file
        
