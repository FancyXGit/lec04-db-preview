-- 在 mysql> 下逐条执行；也可以整段复制。
-- 执行前先 USE preview;
-- 预习练习表：每次重跑这个文件，数据会回到 5 行。
DROP TABLE IF EXISTS members;

CREATE TABLE members (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name       VARCHAR(64)     NOT NULL,
  class_name VARCHAR(32)     NOT NULL,
  major      VARCHAR(32)     NOT NULL,
  score      DECIMAL(5,2)    NOT NULL DEFAULT 0,
  joined_at  DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO members (id, name, class_name, major, score) VALUES
(1, '张三', '2023-1', '计算机', 78),
(2, '李四', '2023-2', '数学', 88),
(3, '王五', '2024-1', '计算机', 92),
(4, '赵六', '2024-2', '英语', 65),
(5, '钱七', '2022-1', '计算机', 85);
