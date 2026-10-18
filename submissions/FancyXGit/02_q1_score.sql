-- 02_q1_score.sql
-- 目标：查询 score >= 85 的同学。
-- 输出列（按这个顺序）：name, score
-- 排序：score DESC, name ASC
-- 限制：只能写一条 SELECT；必须写 ORDER BY；不要用 SELECT *。
-- 参考：preview/05_select.sql
-- 注意：评测会换一份数据，不要把姓名或分数写死在条件里。

-- 在这里写你的 SELECT：
SELECT name, score FROM members
WHERE score >= 85
ORDER BY score DESC, name ASC;
