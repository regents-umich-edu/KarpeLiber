SELECT
  TO_NUMBER(substr(pv.IDNO, 9, 4) || trim(LEADING '0' FROM pv.SEQ)) AS "id",
  to_number(substr(pv.IDNO, 9, 4)) AS "volume_id",
  pv.IDNO AS "libraryNum",
  pv.N AS "page",
  to_number(pv.SEQ) AS "imageNumber",
  to_number(pv.CNF) AS "confidence",
  pv.FTR AS "pageType"
FROM
  PAGEVIEW pv
