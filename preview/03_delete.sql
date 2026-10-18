-- 在 mysql> 下逐条执行；也可以整段复制。
-- 先查
SELECT id, name FROM members WHERE id = 4;

-- 再删
DELETE FROM members WHERE id = 4;

-- 确认
SELECT id, name FROM members WHERE id = 4;
