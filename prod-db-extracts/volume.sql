SELECT
  to_number(v."YEAR") AS "id",
  v.DESCRIPTION AS "title",
  v.ISONLINE AS "available",
  v.BEGINDATE AS "dateBegin",
  v.ENDDATE AS "dateEnd",
  v.NUMPAGES AS "pages"
FROM
  REGNTPRO.VOLUME v
