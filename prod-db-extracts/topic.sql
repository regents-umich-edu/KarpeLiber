SELECT
  p.RPPHRASEIDNUM "id",
  p.RPPHRASETXT "name",
  p.RPPHRASEDATEADDED "addedTime",
  p.RPPHRASEDATEUPDATED "updatedTime"
FROM
  REGNTPRO.PHRASE p

  SELECT
  p.RPPHRASEIDNUM "id",
  p.RPPHRASETXT "name",
  p.RPPHRASEDATEADDED "addedTime",
  p.RPPHRASEDATEUPDATED "updatedTime"
FROM
  REGNTPRO.PHRASE p