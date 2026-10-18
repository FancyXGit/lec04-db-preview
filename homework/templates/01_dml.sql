-- 01_dml.sql
-- 目标：在 preview/init.sql 的 5 行数据基础上，按顺序完成下面 4 条语句。
-- 完成后 members 表应该有 8 行。
-- 参考：preview/01_insert.sql、02_update.sql、03_delete.sql、04_batch_insert.sql
-- 注意：文件里只写 SQL，不要写 mysql>、-> 这些提示符；每条语句以 ; 结尾。
--
-- 1. 新增一条
--    name       = 你的 GitHub 用户名（不要写学号或真实姓名）
--    class_name = 2025-1
--    major      = 计算机
--    score      = 90
--    提示：INSERT INTO 表名 (列1, 列2, ...) VALUES (值1, 值2, ...);



-- 2. 修改一条
--    把 id = 1 的 score 改成 80。
--    提示：先 SELECT 确认要改哪一行，再 UPDATE 表名 SET 列 = 值 WHERE 条件;
--    注意：UPDATE 必须带 WHERE。



-- 3. 删除一条
--    删除 id = 4 的记录。
--    提示：先 SELECT 确认，再 DELETE FROM 表名 WHERE 条件;
--    注意：DELETE 必须带 WHERE。



-- 4. 批量新增三条
--    周九   / 2023-3 / 数学   / 70
--    吴十   / 2024-3 / 英语   / 60
--    郑十一 / 2022-2 / 计算机 / 95
--    提示：一条 INSERT 后面跟多个 VALUES (...), (...), (...);



-- 自查：执行 SELECT COUNT(*) FROM members; 结果应该是 8。
