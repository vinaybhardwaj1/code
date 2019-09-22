SET DEFINE OFF
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
------------------------------------------------------------


--Inserting into PHX_PROJECT for gin number G103913551

SELECT COUNT(*) FROM PHX_PROJECT WHERE PROJECT_NUMBER = 'G103913551';
INSERT INTO PHX_PROJECT (PROJECT_NUMBER,BRANCH_NAME,BU_NAME,CUSTOMER_CODE,DESCRIPTION,JOB_NUMBER,PROJECT_MANAGER_NAME,ORDER_STATUS,TYPE) 
values ('G103913551','UK16400','UK016','146902','Job closed as it was not possible to create a project as error messages kept appearing.  A replacement job will be issued.','UK16400-0004881','UK001423','CANCELED','TYPE_2');


--Inserting into PHX_PROJECT for gin number G103923708

SELECT COUNT(*) FROM PHX_PROJECT WHERE PROJECT_NUMBER = 'G103923708';
INSERT INTO PHX_PROJECT (PROJECT_NUMBER,BRANCH_NAME,BU_NAME,CUSTOMER_CODE,DESCRIPTION,JOB_NUMBER,PROJECT_MANAGER_NAME,ORDER_STATUS,TYPE) 
values ('G103923708','UK16200','UK016','147262','None','UK16200-0009969','UK003779','CANCELED','TYPE_2');


--Updating PHX_JOB_ORDER for gin number G103913551


--Count of rows to be updated = 1
SELECT COUNT(*) FROM PHX_JOB_ORDER WHERE GIN IN ('G103913551');
UPDATE PHX_JOB_ORDER SET PROJECT_NUMBER=G103913551 WHERE GIN IN ('G103913551');


--Updating PHX_JOB_ORDER for gin number G103923708


--Count of rows to be updated = 1
SELECT COUNT(*) FROM PHX_JOB_ORDER WHERE GIN IN ('G103923708');
UPDATE PHX_JOB_ORDER SET PROJECT_NUMBER=G103923708 WHERE GIN IN ('G103923708');


--Updating update_flag in PHX_JOB_TEST to SENT for gin number G103913551


--Count of rows to be updated = 2
select count(*) FROM PHX_JOB_TEST WHERE id in ('5869202','5869203') and JOB_SERVICE_LEVEL_id in (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER in (select job_number from phx_job_order where gin  in ('G103913551') and TYPE='PRODUCT'));
update PHX_JOB_TEST set update_flag='SENT' WHERE id in ('5869202','5869203') and JOB_SERVICE_LEVEL_id in  (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER in(select job_number from phx_job_order where gin  in ('G103913551') and TYPE='PRODUCT'));


--Updating update_flag in PHX_JOB_TEST to SENT for gin number G103923708


--Count of rows to be updated = 2
select count(*) FROM PHX_JOB_TEST WHERE id in ('5885138','5885137') and JOB_SERVICE_LEVEL_id in (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER in (select job_number from phx_job_order where gin  in ('G103923708') and TYPE='PRODUCT'));
update PHX_JOB_TEST set update_flag='SENT' WHERE id in ('5885138','5885137') and JOB_SERVICE_LEVEL_id in  (SELECT ID FROM PHX_JOB_SERVICE_LEVEL WHERE JOB_ORDER_NUMBER in(select job_number from phx_job_order where gin  in ('G103923708') and TYPE='PRODUCT'));


--Inserting into PHX_PROJECT_CONTRACT_FLAG for gin number G103913551

SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103913551'));
INSERT INTO PHX_PROJECT_CONTRACT_FLAG (JOB_NUMBER,ESB_DATE,ESB_FLAG) VALUES (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103913551'),sysdate,'NEW');


--Inserting into PHX_PROJECT_CONTRACT_FLAG for gin number G103923708

SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103923708'));
INSERT INTO PHX_PROJECT_CONTRACT_FLAG (JOB_NUMBER,ESB_DATE,ESB_FLAG) VALUES (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103923708'),sysdate,'NEW');


--Inserting into PHX_PROJECT_CONTRACT_FLAG for gin number G103955352

SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103955352'));
INSERT INTO PHX_PROJECT_CONTRACT_FLAG (JOB_NUMBER,ESB_DATE,ESB_FLAG) VALUES (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103955352'),sysdate,'NEW');


--Inserting into PHX_PROJECT_CONTRACT_FLAG for gin number G103956543

SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103956543'));
INSERT INTO PHX_PROJECT_CONTRACT_FLAG (JOB_NUMBER,ESB_DATE,ESB_FLAG) VALUES (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103956543'),sysdate,'NEW');


--Updating the ESB_FLAG to NEW in PHX_PROJECT_CONTRACT_FLAG for gin number G103632461


--Count of rows to be updated = 1
SELECT COUNT(*) FROM PHX_PROJECT_CONTRACT_FLAG WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103632461'));
UPDATE PHX_PROJECT_CONTRACT_FLAG SET ESB_FLAG='NEW' WHERE JOB_NUMBER IN (SELECT JOB_NUMBER FROM PHX_JOB_ORDER WHERE GIN in ('G103632461'));






------------------------------------------------------------
-- Verification Section
------------------------------------------------------------
-- Expected result: Please make sure above row count matches what I expect.
------------------------------------------------------------
-- If the number of rows update exceeed the number specified above, please rollback the transaction and
-- note the itrak as such.

