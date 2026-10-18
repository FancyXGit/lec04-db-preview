-- 03_q2_major.sql
-- 目标：查询专业为“计算机”的同学。
-- 输出列（按这个顺序）：name, major
-- 排序：id ASC（id 不用输出，但排序要用它）
-- 限制：只能写一条 SELECT；必须写 ORDER BY；不要用 SELECT *。
-- 参考：preview/05_select.sql
-- 注意：评测会换一份数据，不要把结果写死。

-- 在这里写你的 SELECT：
SELECT name, major FROM members
WHERE major = '计算机'
ORDER BY id ASC;
