
import Connection as con


def setFlagSentPhxTest(unsentPhxTest,file):
    c = con.conn.cursor()
    for gin,ids in unsentPhxTest.items():
        selectString = 'select count(*) FROM PHX_JOB_TEST WHERE id in ('

        whereIds = '\''+str(ids[0])+'\''
        
        del ids[0]
        for id in ids:
            whereIds+= ',\''+ str(id) + '\''

        selectString+=whereIds
        selectString+=') and JOB_SERVICE_LEVEL_id in (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER in (select job_number from phx_job_order where gin  in (\''+gin+'\') and TYPE=\'PRODUCT\'));'

        updateString = 'update PHX_JOB_TEST set update_flag=\'SENT\' WHERE id in ('
        updateString+=whereIds
        updateString+=') and JOB_SERVICE_LEVEL_id in  (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER in(select job_number from phx_job_order where gin  in (\''+gin+'\') and TYPE=\'PRODUCT\'));'

        countString = selectString.replace(';',' ')
        result = c.execute(countString)
        for row in result:
            count=row
            
        file.write('\n--Updating update_flag in PHX_JOB_TEST to SENT for gin number '+gin+'\n\n')
        file.write('\n--Count of rows to be updated = '+str(count[0])+'\n')
        file.write(selectString+'\n')
        file.write(updateString)
        file.write('\n\n')
    return file
