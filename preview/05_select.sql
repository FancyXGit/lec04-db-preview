-- 在 mysql> 下逐条执行；也可以整段复制。
-- 全部
SELECT id, name, score FROM members;

-- 比较
SELECT id, name, score FROM members WHERE score >= 85;

-- 字符串
SELECT id, name, major FROM members WHERE major = '计算机';

-- 模糊
SELECT id, name FROM members WHERE name LIKE '张%';

-- 范围
SELECT id, name, score FROM members WHERE score BETWEEN 80 AND 90;

-- 多选
SELECT id, name, major FROM members WHERE major IN ('计算机', '数学');

-- 组合
SELECT id, name, score FROM members
WHERE major = '计算机' AND score >= 85;

-- 排序 + 截断
SELECT id, name, score FROM members
ORDER BY score DESC, name ASC
LIMIT 3;

-- 计数
SELECT COUNT(*) AS cnt FROM members;

-- 分组
SELECT major, COUNT(*) AS cnt FROM members GROUP BY major;
