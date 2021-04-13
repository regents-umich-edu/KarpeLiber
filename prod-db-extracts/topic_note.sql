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
  pn.RPNOTETYPECD = pntc.NOTETYPECD;
