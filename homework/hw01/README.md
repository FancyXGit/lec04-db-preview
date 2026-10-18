# HW01：增删改查练习

## 提交信息

- 分支：`hw01/<你的 GitHub 用户名>`
- 目录：`submissions/<你的 GitHub 用户名>/hw01/`
- PR 标题：`[HW01] <你的 GitHub 用户名>`
- 只写 GitHub 用户名，不要写学号或真实姓名。

## 文件

```text
submissions/<你的 GitHub 用户名>/hw01/
├── 01_dml.sql
├── 02_q1_score.sql
├── 03_q2_major.sql
├── 04_q3_like.sql
├── 05_q4_top3.sql
└── README.md
```

把 `templates/` 里的文件复制过去，再把标了 `TODO` 的地方改掉。

## 任务 1：`01_dml.sql`

在 `preview/init.sql` 的 5 行数据基础上，依次完成四条语句。

### 1. 新增一条

- `name`：你的 GitHub 用户名
- `class_name`：`2025-1`
- `major`：`计算机`
- `score`：`90`

### 2. 修改一条

把 `id = 1` 的 `score` 改成 `80`。

### 3. 删除一条

删除 `id = 4` 的记录。

### 4. 批量新增三条

| name | class_name | major | score |
| --- | --- | --- | ---: |
| 周九 | 2023-3 | 数学 | 70 |
| 吴十 | 2024-3 | 英语 | 60 |
| 郑十一 | 2022-2 | 计算机 | 95 |

最终表里应该有 8 行。

> 姓名只写 GitHub 用户名，不要写学号或真实姓名。

## 任务 2：四条查询

每个文件只能有一条 `SELECT`，必须写 `ORDER BY`，不要用 `SELECT *`。

### `02_q1_score.sql`

查询 `score >= 85` 的同学。

- 输出列：`name`, `score`
- 排序：`score DESC, name ASC`

### `03_q2_major.sql`

查询专业为 `计算机` 的同学。

- 输出列：`name`, `major`
- 排序：`id ASC`

### `04_q3_like.sql`

查询姓张开头的同学。

- 输出列：`name`
- 排序：`name ASC`

### `05_q4_top3.sql`

查询分数最高的 3 位同学。

- 输出列：`name`, `score`
- 排序：`score DESC, name ASC`
- 截断：`LIMIT 3`

## 任务 3：`README.md`

写上你的 GitHub 用户名，并回答三个问题：

1. `WHERE` 是干什么的？
2. 如果 `UPDATE` 不写 `WHERE` 会发生什么？
3. 四条查询里，哪一条你改得最久，为什么？

## 本地自测

### 测 DML

在 Navicat 里按顺序执行：

1. `preview/init.sql`
2. `submissions/<你的 GitHub 用户名>/hw01/01_dml.sql`
3. `SELECT COUNT(*) FROM members;`

结果应该是 `8`。

### 测查询

评测会用另一份数据跑查询。你可以这样本地模拟：

1. 重跑 `preview/init.sql`
2. 执行 `grader/fixtures/eval_seed.sql`
3. 依次执行你的四个查询文件

这份数据下，正确结果应该是：

```text
q1: 林二 95.00, 周七 90.00, 吴六 88.00, 张五 87.00, 郑八 86.00
q2: 陈一 计算机, 张五 计算机, 周七 计算机
q3: 张五
q4: 林二 95.00, 周七 90.00, 吴六 88.00
```

不要把这些结果写死到 SQL 里。评测看的是查询逻辑。

## 评分

| 项目 | 分值 |
| --- | ---: |
| `01_dml.sql` 四条语句 | 40 |
| 四条查询 | 40 |
| `README.md` | 10 |
| 提交规范 | 10 |

80 分通过。

## 提交

1. 从 `upstream/main` 建分支 `hw01/<你的 GitHub 用户名>`；
2. 只修改 `submissions/<你的 GitHub 用户名>/hw01/`；
3. 提交 PR，标题 `[HW01] <你的 GitHub 用户名>`；
4. 等 `autograde` 变绿。

详细步骤见 [预习文档](../../docs/00-预习.md#8-提交-pr)。
