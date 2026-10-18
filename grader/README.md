# 自动评测说明（老师/助教用）

## 依赖

- Python 3.10+
- MySQL 8.0
- Python 包：`pymysql`、`cryptography`

```bash
pip install pymysql cryptography
```

## 环境变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `MYSQL_HOST` | `127.0.0.1` | MySQL 地址 |
| `MYSQL_PORT` | `3306` | 端口 |
| `MYSQL_USER` | `root` | 用户 |
| `MYSQL_PASSWORD` | 空 | 密码 |
| `MYSQL_DATABASE` | `hw01` | 评测数据库名，脚本会重建它 |
| `SUBMISSION_DIR` | 无 | 例如 `submissions/alice/hw01` |
| `GITHUB_USER` | 无 | PR 作者的 GitHub 用户名 |

## 本地运行

```bash
MYSQL_USER=root MYSQL_PASSWORD=你的密码 \
python grader/grade.py \
  --submission submissions/alice/hw01 \
  --github-user alice
```

Windows PowerShell：

```powershell
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="你的密码"
python grader/grade.py --submission submissions/alice/hw01 --github-user alice
```

## 判分逻辑

| 项目 | 分值 | 检查方式 |
| --- | ---: | --- |
| 提交规范 | 10 | 6 个文件齐全，目录名等于 GitHub 用户名 |
| DML 新增 | 10 | `name` 等于 GitHub 用户名，班级/专业/分数正确 |
| DML 修改 | 10 | `id=1` 的 `score=80.00` |
| DML 删除 | 10 | `id=4` 不存在 |
| DML 批量新增 | 10 | 3 条指定记录，总行数 8 |
| Q1 分数筛选 | 10 | 列名、行数、顺序完全匹配 |
| Q2 专业筛选 | 10 | 同上 |
| Q3 模糊查询 | 10 | 同上 |
| Q4 排序截断 | 10 | 同上 |
| README | 10 | 填了 GitHub 用户名，至少 3 行回答 |

80 分通过。

## 数据

- DML 使用 `preview/init.sql` 的 5 行数据；
- 查询使用 `preview/init.sql` + `grader/fixtures/eval_seed.sql` 的 7 行数据。

每次评测都会：

1. `DROP DATABASE` / `CREATE DATABASE`；
2. 重新执行 `preview/init.sql`；
3. 跑学生 SQL；
4. 比对结果。

## 注意

- 脚本会重建 `MYSQL_DATABASE` 指定的数据库，不要指向有真实数据的库。
- fork PR 的 `GITHUB_TOKEN` 是只读的，所以不自动发 PR 评论；结果写到 Actions 的 Summary。
- 学生只能改 `submissions/<username>/hw01/`，越界由 workflow 的 Guard 拦截。
