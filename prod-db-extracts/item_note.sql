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
  i_n.RPNOTETYPECD = intc.NOTETYPECD
