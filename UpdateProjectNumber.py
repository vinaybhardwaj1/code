import Connection as con

def updateProjNum(projNumNullGins,file):
    c = con.conn.cursor()
    for gins in projNumNullGins:
        selectString = 'SELECT COUNT(*) FROM PHX_JOB_ORDER WHERE GIN IN (\''+gins+'\');'
        updateString = 'UPDATE PHX_JOB_ORDER SET PROJECT_NUMBER='+gins+' WHERE GIN IN (\''+gins+'\');'

        countString = selectString.replace(';',' ')
        result = c.execute(countString)
        for row in result:
            count=row
            
        file.write('\n--Updating PHX_JOB_ORDER for gin number '+gins+'\n\n')
        file.write('\n--Count of rows to be updated = '+str(count[0])+'\n')
        file.write(selectString+'\n')
        file.write(updateString)
        file.write('\n\n')
    return file
