-- REGNTPRO.V_ITEM source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_ITEM" ("id", "name", "topic_id", "addedTime", "updatedTime") AS 
  SELECT
  i.RPITEMIDNUM AS "id",
  i.RPITEMTEXT AS "name",
  i.RPPHRASEIDNUM AS "topic_id",
  i.RPITEMDATEADDED AS "addedTime",
  i.RPITEMDATEUPDATED AS "updatedTime"
FROM
  REGNTPRO.ITEM i;


-- REGNTPRO.V_ITEM_NOTE source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_ITEM_NOTE" ("id", "type_id", "item_id", "text", "referencedTopic_id") AS 
  SELECT
  to_number(i_n.RPITEMIDNUM || lpad(i_n.NOTEID, 3, '0')) AS "id",
  intc.ID AS "type_id",
  i_n.RPITEMIDNUM AS "item_id",
  i_n.RPNOTETXT AS "text",
  i_n.RELRPPHRASEIDNUM AS "referencedTopic_id"
FROM
  REGNTPRO.ITEM_NOTES i_n,
  REGNTPRO.ITEM_NOTE_TYPE_CODES intc
WHERE
  i_n.RPNOTETYPECD = intc.NOTETYPECD;


-- REGNTPRO.V_ITEM_PAGE source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_ITEM_PAGE" ("id", "page", "date", "item_id", "volume_id", "month", "year") AS 
  SELECT
  to_number(ip.RPITEMIDNUM || lpad(ip.PAGEID, 2, '0')) AS "id",
  to_char(ip.RPPAGENUM) AS "page",
  ip.VOLDATE AS "date",
  ip.RPITEMIDNUM AS "item_id",
  ip.VOLUMEID AS "volume_id",
  EXTRACT(MONTH FROM to_date(ip.RPMONTHCD, 'Mon')) AS "month",
  EXTRACT(YEAR FROM to_date(substr(ip.RPCALYEAR, 0, 4), 'YYYY')) AS "year"
FROM
  REGNTPRO.ITEM_PAGE ip;


-- REGNTPRO.V_NOTE_TYPE source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_NOTE_TYPE" ("ID", "code", "name") AS 
  SELECT
  id,
  nt.NOTETYPECD AS "code",
  nt.NOTETYPETXT AS "name"
FROM
  REGNTPRO.ITEM_NOTE_TYPE_CODES nt
ORDER BY
  id;


-- REGNTPRO.V_PAGE_MAPPING source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_PAGE_MAPPING" ("id", "volume_id", "page", "imageNumber", "confidence", "pageType") AS 
  SELECT
  TO_NUMBER(substr(pv.IDNO, 9, 4) || trim(LEADING '0' FROM pv.SEQ)) AS "id",
  to_number(substr(pv.IDNO, 9, 4)) AS "volume_id",
  CASE
    pv.N WHEN '00000000' THEN '0'
    ELSE TRIM(LEADING 0 FROM pv.N)
  END AS "page",
  to_number(pv.SEQ) AS "imageNumber",
  to_number(pv.CNF) AS "confidence",
  upper(pv.FTR) AS "pageType"
FROM
  PAGEVIEW pv;


-- REGNTPRO.V_TOPIC source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_TOPIC" ("id", "name", "addedTime", "updatedTime") AS 
  SELECT
  p.RPPHRASEIDNUM "id",
  p.RPPHRASETXT "name",
  p.RPPHRASEDATEADDED "addedTime",
  p.RPPHRASEDATEUPDATED "updatedTime"
FROM
  REGNTPRO.PHRASE p;


-- REGNTPRO.V_TOPIC_NOTE source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_TOPIC_NOTE" ("id", "type_id", "topic_id", "text", "referencedTopic_id") AS 
  SELECT
  to_number(pn.RPPHRASEIDNUM || lpad(pn.NOTEID, 3, '0')) AS "id",
  pntc.ID AS "type_id",
  pn.RPPHRASEIDNUM AS "topic_id",
  pn.RPNOTETXT AS "text",
  pn.RELRPPHRASEIDNUM AS "referencedTopic_id"
FROM
  REGNTPRO.PHRASE_NOTES pn,
  REGNTPRO.PHRASE_NOTE_TYPE_CODES pntc
WHERE
  pn.RPNOTETYPECD = pntc.NOTETYPECD(+);


-- REGNTPRO.V_VOLUME source

CREATE OR REPLACE FORCE EDITIONABLE VIEW "REGNTPRO"."V_VOLUME" ("id", "title", "available", "dateBegin", "dateEnd", "pages", "libraryNum") AS 
  SELECT
  to_number(v."YEAR") AS "id",
  TO_CHAR(v.BEGINDATE, 'Mon YYYY')||'–'||TO_CHAR(v.ENDDATE, 'Mon YYYY') AS "title",
  v.ISONLINE AS "available",
  v.BEGINDATE AS "dateBegin",
  v.ENDDATE AS "dateEnd",
  v.NUMPAGES AS "pages",
  'acw7513.' || v."YEAR" || '.001' AS "libraryNum"
FROM
  REGNTPRO.VOLUME v;
