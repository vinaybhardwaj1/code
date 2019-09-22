def createBasicScript(file):
    header = r'''SET DEFINE OFF
SELECT NAME DATABASE_NAME, USER FROM V$DATABASE;
------------------------------------------------------------
------------------------------------------------------------
-- Application: Phoenix
-- Database Name: PHXPRD
-- Database Type: Oracle
-- Estimated Run Time: <=1 minute
--++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
------------------------------------------------------------
-- Backup Section
------------------------------------------------------------
-- Backup is not required for this script
------------------------------------------------------------
-- Execution Section 
------------------------------------------------------------'''

    file.write(header)
    file.write('\n\n')
    return file
    
def createBasicScriptFooter(file):
    footer = r'''

------------------------------------------------------------
-- Verification Section
------------------------------------------------------------
-- Expected result: Please make sure above row count matches what I expect.
------------------------------------------------------------
-- If the number of rows update exceeed the number specified above, please rollback the transaction and
-- note the itrak as such.'''
    file.write('\n\n\n')
    file.write(footer)
    file.write('\n\n')
    return file
