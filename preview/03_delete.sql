-- 先查
SELECT id, name FROM members WHERE id = 4;

-- 再删
DELETE FROM members WHERE id = 4;

-- 确认
SELECT id, name FROM members WHERE id = 4;
