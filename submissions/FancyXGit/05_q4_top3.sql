-- 05_q4_top3.sql
-- 目标：查询分数最高的 3 位同学。
-- 输出列（按这个顺序）：name, score
-- 排序：score DESC, name ASC
-- 截断：LIMIT 3
-- 限制：只能写一条 SELECT；必须写 ORDER BY；不要用 SELECT *。
-- 参考：preview/05_select.sql
-- 注意：评测会换一份数据，不要把结果写死。

-- 在这里写你的 SELECT：
SELECT name, score FROM members
ORDER BY score DESC, name ASC
LIMIT 3;
