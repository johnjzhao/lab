-- VT_ENR1 Create

CREATE MULTISET VOLATILE TABLE VT_ENR1 AS
        (
        SELECT 
    Max(CVRG_END_DT) Over (PARTITION BY SRC_MBR_KEY, HLTHPLN_IK ORDER BY CVRG_START_DT, CVRG_END_DT ROWS BETWEEN Unbounded Preceding AND CURRENT ROW) CVRG_END_DT_NEW,
    Row_Number () Over (PARTITION BY SRC_MBR_KEY, HLTHPLN_IK ORDER BY CVRG_START_DT,CVRG_END_DT) NR,
    VT_ENR1_1.*
FROM
(
        select
                MBR_KEY,HLTHPLN_KEY,HLTHPLN_SRC_PLAN_SK,HLTHPLN_MRKT_RELTN_SK,EMPLR_GRP_SK,SRC_MBR_KEY,HLTHPLN_IK,SYS_CVRG_GRP_ID,ENRLMT_START_DT,CVRG_START_DT,CVRG_TY_CD,SRC_DATA_KEY,ENRLMT_START_DT_KEY,ENRLMT_END_DT,ENRLMT_END_DT_KEY,ENRLMT_CONTS_FRST_DT,CVRG_START_DT_KEY,CVRG_END_DT,CVRG_END_DT_KEY,TENANT_CD,PRODT_TY_CD,PRODT_CONTS_FRST_DT,PAYOR_NM,PAYOR_CONTS_FRST_DT,ENRLMT_SIG_DT,ENRLMT_SIG_DT_KEY           
        from
        (
        SELECT
        DISTINCT
                Nvl(MD.MBR_KEY, -1) AS MBR_KEY ,
                Nvl(HD.HLTHPLN_KEY, -1) AS HLTHPLN_KEY,
                -1 AS HLTHPLN_SRC_PLAN_SK,
                Nvl(HMR.HLTHPLN_MRKT_RELTN_SK, -1) AS HLTHPLN_MRKT_RELTN_SK ,
                -1 AS EMPLR_GRP_SK,
                '59' || '_'|| Trim(PD.POL_ADMIN_ID_VAL) AS SRC_MBR_KEY,
                Coalesce(HD.HLTHPLN_IK,'U') AS HLTHPLN_IK,
                'U' AS SYS_CVRG_GRP_ID,
                PCF.CVRG_EFF_DT AS ENRLMT_START_DT,
                PCF.CVRG_EFF_DT AS CVRG_START_DT,
                'CMS' AS CVRG_TY_CD,
                59 AS SRC_DATA_KEY,
                Cast(Cast(Cast(ENRLMT_START_DT AS DATE Format 'yyyymmdd') AS VARCHAR(8)) AS INTEGER) AS ENRLMT_START_DT_KEY,
                Coalesce(PCF.CVRG_TERM_DT,DATE '9999-12-31') AS ENRLMT_END_DT,
                Cast(Cast(Cast(ENRLMT_END_DT AS DATE Format 'yyyymmdd') AS VARCHAR(8)) AS INTEGER) AS ENRLMT_END_DT_KEY,
                NULL AS ENRLMT_CONTS_FRST_DT,
                Cast(Cast(Cast(CVRG_START_DT AS DATE Format 'yyyymmdd') AS VARCHAR(8)) AS INTEGER) AS CVRG_START_DT_KEY,
                Coalesce(PCF.CVRG_TERM_DT,DATE '9999-12-31') AS CVRG_END_DT,
                Cast(Cast(Cast(CVRG_END_DT AS DATE Format 'yyyymmdd') AS VARCHAR(8)) AS INTEGER) AS CVRG_END_DT_KEY,
                'UNKNOWN' AS TENANT_CD,
                'Medicare' AS PRODT_TY_CD,
                NULL AS PRODT_CONTS_FRST_DT,
                'Cigna Supplemental Benefits' AS PAYOR_NM,
                NULL AS PAYOR_CONTS_FRST_DT,
                NULL AS ENRLMT_SIG_DT,
                NULL AS ENRLMT_SIG_DT_KEY
        FROM
                TRXHUB_CORE_V.CSB_POL_DIM AS PD
        INNER JOIN
                TRXHUB_CORE_V.CSB_POLICY_CVAG_FCT PCF
        ON PD.POL_ID=PCF.POL_ID
        INNER JOIN
                TRXHUB_CORE_V.CSB_CUST_DIM CDIM
        ON PCF.CUST_ID=CDIM.CUST_ID
        INNER JOIN
                DATAMART_MEMBER_V.MBR_DIM AS MD
        ON Trim(MD.MBR_ID) = Trim(PD.POL_ADMIN_ID_VAL)
                AND MD.SRC_DATA_KEY = PD.SRC_DATA_KEY
                AND MD.IS_CURR_IND='Y'
        INNER JOIN
                TRXHUB_CORE_V.CSB_PRODT P
        ON P.PRODT_ID = PCF.PRODT_ID
                AND P.REC_STAT_CD = 'C'
        INNER JOIN
                DATAMART_REFDATA_V.HLTHPLN_DIM AS HD
        ON Trim(HD.HLTHPLN_NM) = Trim(P.PRODT_NM)
                AND HD.SRC_DATA_KEY=59
                AND HD.IS_CURR_IND='Y'
        LEFT OUTER JOIN
                DATAMART_REFDATA_V.HLTHPLN_MRKT_RELTN_DIM AS HMR
        ON Trim(HD.HLTHPLN_IK) = Trim(HMR.HLTHPLN_IK)
                AND HMR.ETL_IS_CURR_IND='Y'
        WHERE
                PD.POL_ADMIN_ID_TY = 'CSB'
        AND (PD.POL_ADMIN_ID_VAL IS NOT NULL AND TRIM(PD.POL_ADMIN_ID_VAL) <> '')
                QUALIFY Row_Number() Over (PARTITION BY SRC_MBR_KEY, SYS_CVRG_GRP_ID ORDER BY PCF.REC_UPDT_DT DESC  ) = 1
        ) core_v
        QUALIFY Row_Number() Over (PARTITION BY SRC_MBR_KEY, HLTHPLN_IK, CVRG_START_DT, CVRG_END_DT ORDER BY SYS_CVRG_GRP_ID) = 1
) VT_ENR1_1
)WITH DATA
PRIMARY INDEX(MBR_KEY,HLTHPLN_KEY, SRC_DATA_KEY, CVRG_START_DT, CVRG_END_DT)
ON COMMIT PRESERVE ROWS;
COLLECT STATS ON VT_ENR1
COLUMN (MBR_KEY,HLTHPLN_KEY, SRC_DATA_KEY, CVRG_START_DT, CVRG_END_DT)
; 

-- VT_ENR3 Create 

CREATE MULTISET VOLATILE TABLE VT_ENR3 AS
(
SELECT 
   Min(CVRG_START_DT) Over (PARTITION BY SRC_MBR_KEY,HLTHPLN_IK, SUMM) ENRLMT_CONTS_FRST_DT_NEW,
   SRC_MBR_KEY, HLTHPLN_IK, CVRG_START_DT, CVRG_END_DT 
FROM 
(
	SELECT 
	   Sum(DIFF) Over (PARTITION BY SRC_MBR_KEY, HLTHPLN_IK ORDER BY CVRG_START_DT, CVRG_END_DT, DIFF DESC ROWS Unbounded Preceding ) SUMM,
	   X.* 
	FROM 
	(
		SELECT 
			SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, HLTHPLN_IK, CVRG_END_DT,ENRLMT_CONTS_FRST_DT, CVRG_TY_CD, 
			CVRG_END_DT_NEW, LAGG
			,Coalesce ((CVRG_START_DT - LAGG),0) AS DIFF1
			,CASE WHEN DIFF1 <= 1 THEN 0 ELSE DIFF1 END DIFF
		from
		(
			SELECT  
			   A.SRC_MBR_KEY, A.PRODT_TY_CD, A.HLTHPLN_IK, A.CVRG_START_DT, A.CVRG_END_DT, A.ENRLMT_CONTS_FRST_DT, A.CVRG_TY_CD, A.CVRG_END_DT_NEW, 
			   B.CVRG_END_DT_NEW AS LAGG  -- , A.NR 
			FROM 
				VT_ENR1 A
			LEFT JOIN 
				VT_ENR1 B
			ON A.SRC_MBR_KEY = B.SRC_MBR_KEY 
			AND A.HLTHPLN_IK = B.HLTHPLN_IK AND A.NR-1 = B.NR
		)VT_ENR2
	)X
)Y
)WITH DATA
PRIMARY INDEX(SRC_MBR_KEY, HLTHPLN_IK, CVRG_START_DT, CVRG_END_DT)
ON COMMIT PRESERVE ROWS;
COLLECT STATS ON VT_ENR3
COLUMN (SRC_MBR_KEY, HLTHPLN_IK, CVRG_START_DT, CVRG_END_DT)
;

-- CSB_MBR_ENRLMT_CVRG_BASE_GET Create

CREATE MULTISET VOLATILE TABLE CSB_MBR_ENRLMT_CVRG_BASE_GET AS
(
select * from VT_ENR1
)WITH DATA
PRIMARY INDEX(MBR_KEY,HLTHPLN_KEY, SRC_DATA_KEY, CVRG_START_DT, CVRG_END_DT)
ON COMMIT PRESERVE ROWS;

COLLECT STATS ON CSB_MBR_ENRLMT_CVRG_BASE_GET
COLUMN (MBR_KEY,HLTHPLN_KEY, SRC_DATA_KEY, CVRG_START_DT, CVRG_END_DT)
;

-- VT_PRD1 Create

CREATE MULTISET VOLATILE TABLE VT_PRD1 AS
(
SELECT  
    Max(CVRG_END_DT) Over (PARTITION BY SRC_MBR_KEY, PRODT_TY_CD ORDER BY CVRG_START_DT, CVRG_END_DT ROWS BETWEEN Unbounded Preceding AND CURRENT ROW) CVRG_END_DT_LATEST,
    Row_Number () Over (PARTITION BY SRC_MBR_KEY, PRODT_TY_CD ORDER BY CVRG_START_DT,CVRG_END_DT) NR_1,
    VT_PRD1_1.* 
FROM 
    (
    SELECT 
        * 
    FROM 
        CSB_MBR_ENRLMT_CVRG_BASE_GET
    QUALIFY Row_Number() Over (PARTITION BY SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT ORDER BY SYS_CVRG_GRP_ID) = 1
    ) VT_PRD1_1
)WITH DATA
PRIMARY INDEX(SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT)
ON COMMIT PRESERVE ROWS;
COLLECT STATS ON VT_PRD1
COLUMN (SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT)
;

--  VT_PRD3 create

CREATE MULTISET VOLATILE TABLE VT_PRD3 AS
(
SELECT 
   Min(CVRG_START_DT) Over (PARTITION BY SRC_MBR_KEY,PRODT_TY_CD, summ) PRODT_CONTS_FRST_DT_New,
   SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT
FROM 
(
    SELECT 
       Sum(DIFF) Over (PARTITION BY SRC_MBR_KEY, PRODT_TY_CD ORDER BY CVRG_START_DT, CVRG_END_DT, DIFF DESC ROWS Unbounded Preceding ) SUMM,
       x.* 
    FROM 
    (
       SELECT 
          SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT, PRODT_CONTS_FRST_DT, CVRG_TY_CD, 
          CVRG_END_DT_New, LAGG
          ,Coalesce ((CVRG_START_DT - LAGG),0) AS DIFF1
          ,CASE WHEN DIFF1 <= 1 THEN 0 ELSE DIFF1 END DIFF
		FROM 
		(
			SELECT  
				A.SRC_MBR_KEY, A.PRODT_TY_CD, A.CVRG_START_DT, A.CVRG_END_DT, A.PRODT_CONTS_FRST_DT, A.CVRG_TY_CD, A.CVRG_END_DT_NEW, 
				B.CVRG_END_DT_NEW AS LAGG
			FROM 
				VT_PRD1 A
			LEFT JOIN 
				VT_PRD1 B
			ON A.SRC_MBR_KEY = B.SRC_MBR_KEY 
			AND A.PRODT_TY_CD = B.PRODT_TY_CD AND A.NR-1 = B.NR
		)VT_PRD2
    ) x
)VT_PRD3_1
)WITH DATA
PRIMARY INDEX(SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT)
ON COMMIT PRESERVE ROWS;
COLLECT STATS ON VT_PRD3
COLUMN (SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, CVRG_END_DT)
;

-- VT_PAY1 Create

CREATE MULTISET VOLATILE TABLE VT_PAY1 AS
(
SELECT  
      Max(CVRG_END_DT) Over (PARTITION BY SRC_MBR_KEY, PAYOR_NM ORDER BY CVRG_START_DT, CVRG_END_DT ROWS BETWEEN Unbounded Preceding AND CURRENT ROW) CVRG_END_DT_NEW_1,
      Row_Number () Over (PARTITION BY SRC_MBR_KEY, PAYOR_NM ORDER BY CVRG_START_DT,CVRG_END_DT) NR_1,
      a.* 
FROM
(
	SELECT 
		* 
	FROM 
		CSB_MBR_ENRLMT_CVRG_BASE_GET
    QUALIFY Row_Number() Over (PARTITION BY SRC_MBR_KEY, PAYOR_NM, CVRG_START_DT, CVRG_END_DT ORDER BY SYS_CVRG_GRP_ID) = 1  
) a
)WITH DATA
PRIMARY INDEX(SRC_MBR_KEY, PAYOR_NM)
ON COMMIT PRESERVE ROWS;
COLLECT STATS ON VT_PAY1
COLUMN (SRC_MBR_KEY, PAYOR_NM)
;

-- VT_PAY3 Create

CREATE MULTISET VOLATILE TABLE VT_PAY3 AS
(
SELECT 
   Min(CVRG_START_DT) Over (PARTITION BY SRC_MBR_KEY,PAYOR_NM, summ) PAYOR_CONTS_FRST_DT_New,
   SRC_MBR_KEY, PAYOR_NM, CVRG_START_DT, CVRG_END_DT --,y.* 
FROM 
(
    SELECT 
          Sum(diff) Over (PARTITION BY SRC_MBR_KEY, PAYOR_NM ORDER BY CVRG_START_DT, CVRG_END_DT, diff DESC ROWS Unbounded Preceding ) summ,
          x.* 
    FROM 
    (
		SELECT 
          SRC_MBR_KEY, PRODT_TY_CD, CVRG_START_DT, PAYOR_NM, CVRG_END_DT,PAYOR_CONTS_FRST_DT,CVRG_TY_CD, 
          CVRG_END_DT_NEW, LAGG
          ,Coalesce ((CVRG_START_DT - LAGG),0) AS DIFF1
          ,CASE WHEN DIFF1 <= 1 THEN 0 ELSE DIFF1 END DIFF
		FROM 
		(
			SELECT  
			A.SRC_MBR_KEY, A.PRODT_TY_CD, A.PAYOR_NM, A.CVRG_START_DT, A.CVRG_END_DT, A.PAYOR_CONTS_FRST_DT, A.CVRG_TY_CD, A.CVRG_END_DT_NEW, 
			B.CVRG_END_DT_NEW AS LAGG  -- , A.NR 
		 FROM VT_PAY1 A
		 LEFT JOIN VT_PAY1 B
		 ON A.SRC_MBR_KEY = B.SRC_MBR_KEY 
		 AND A.PAYOR_NM = B.PAYOR_NM AND A.NR-1 = B.NR
		)VT_PAY2
    ) x
) y
)WITH DATA
PRIMARY INDEX( SRC_MBR_KEY, CVRG_START_DT, PAYOR_NM, CVRG_END_DT)
ON COMMIT PRESERVE ROWS;
COLLECT STATS ON VT_PAY3
COLUMN ( SRC_MBR_KEY,CVRG_START_DT, PAYOR_NM, CVRG_END_DT)
;
