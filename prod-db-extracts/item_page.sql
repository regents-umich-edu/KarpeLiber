SELECT
  to_number(ip.RPITEMIDNUM || lpad(ip.PAGEID, 2, '0')) AS "id",
  ip.RPPAGENUM AS "page",
  ip.VOLDATE AS "date",
  ip.RPITEMIDNUM AS "item_id",
  EXTRACT(MONTH FROM to_date(ip.RPMONTHCD, 'Mon')) AS "month",
  EXTRACT(YEAR FROM to_date(substr(ip.RPCALYEAR, 0, 4), 'YYYY')) AS "year"
FROM
  REGNTPRO.ITEM_PAGE ip,
  REGNTPRO.ITEM i
WHERE
  ip.RPITEMIDNUM = i.RPITEMIDNUM
