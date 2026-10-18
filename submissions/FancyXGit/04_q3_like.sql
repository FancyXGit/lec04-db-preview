-- 04_q3_like.sql
-- 目标：查询姓“张”的同学（name 以“张”开头）。
-- 输出列（按这个顺序）：name
-- 排序：name ASC
-- 限制：只能写一条 SELECT；必须写 ORDER BY；不要用 SELECT *。
-- 提示：用 LIKE，百分号 % 表示任意多个字符。
-- 参考：preview/05_select.sql
-- 注意：评测会换一份数据，不要把结果写死。

-- 在这里写你的 SELECT：
SELECT name FROM members
WHERE name LIKE '张%'
ORDER BY name ASC;
