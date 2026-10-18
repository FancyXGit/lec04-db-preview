-- 1. 新增：把 <your-github-username> 换成你的 GitHub 用户名
INSERT INTO members (name, class_name, major, score)
VALUES ('<your-github-username>', '2025-1', '计算机', 90);

-- 2. 修改：把 id=1 的 score 改成 80
UPDATE members SET score = 80 WHERE id = 1;

-- 3. 删除：删除 id=4
DELETE FROM members WHERE id = 4;

-- 4. 批量新增：三条记录
INSERT INTO members (name, class_name, major, score) VALUES
('周九', '2023-3', '数学', 70),
('吴十', '2024-3', '英语', 60),
('郑十一', '2022-2', '计算机', 95);
