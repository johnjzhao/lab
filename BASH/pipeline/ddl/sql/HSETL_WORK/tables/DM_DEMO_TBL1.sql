--liquibase formatted sql

--changeset david.mahler:svt_autochg_tdv_dev.tables.dm_demo_tbl1_1 runOnChange:true labels:tmp,demo,dmahler context:dev
--comment: Create table HSETL_WORK_DEV2.DM_DEMO_TBL1
SELECT 1 
FROM DBC.TABLES 
WHERE DatabaseName = 'HSETL_WORK_DEV2'
  AND TableName = 'DM_DEMO_TBL1'
  AND TableKind IN ('T','O','V');

.IF ACTIVITYCOUNT = 0 THEN GOTO create_table;

.LABEL drop_table;
DROP TABLE HSETL_WORK_DEV2.DM_DEMO_TBL1;

.LABEL create_table;
CREATE TABLE HSETL_WORK_DEV2.DM_DEMO_TBL1 (
DEMO_TBL_KEY CHAR(32) NOT NULL,
CRET_TS TIMESTAMP NOT NULL,
UPDT_TS TIMESTAMP NOT NULL,
CHK_SUM_TXT CHAR(32) NOT NULL,
CMMNT_TXT VARCHAR(1000) NOT NULL,
CRET_BY VARCHAR(1000),
ACT_IND CHAR(1) NOT NULL
);