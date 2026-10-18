-- 在 mysql> 下逐条执行；也可以整段复制。
-- 先查，确认改的是谁
SELECT id, name, score FROM members WHERE id = 1;

-- 再改
UPDATE members SET score = 80 WHERE id = 1;

-- 再查，确认改对了
SELECT id, name, score FROM members WHERE id = 1;
