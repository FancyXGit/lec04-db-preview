# 数据库第一课预习仓库

这个仓库放三样东西：

- `preview/`：预习时照着敲的 SQL；
- `homework/`：课前作业题目和模板；
- `submissions/`：你提交作业的地方。

完整预习文档见 [docs/00-预习.md](docs/00-预习.md)。

## 快速开始

1. 安装 MySQL 8.0（Navicat 可选，不装也能完成全部作业，见预习文档附录）。
2. 打开 MySQL 命令行：`mysql -u root -p`。如果提示找不到，用开始菜单里的 MySQL 8.0 Command Line Client。
3. 新建数据库 `preview`，在 `mysql>` 里执行 `preview/init.sql` 里的语句。
4. 按 [预习文档](docs/00-预习.md) 在命令行里跑一遍增、改、删和查询。
5. 把作业写到 `submissions/<你的 GitHub 用户名>/`。
6. 向本仓库 `main` 分支提交 Pull Request。

## 提交约定

- 分支名：`<你的 GitHub 用户名>`
- 目录：`submissions/<你的 GitHub 用户名>/`
- PR 标题：`hw: <你的 GitHub 用户名>`
- 只修改自己目录下的文件。

PR 提交后会自动运行 `autograde`。绿色表示通过；红色点 `Details` 看原因。

> 不要写学号或真实姓名，只写 GitHub 用户名。

## 目录

```text
.
├── docs/00-预习.md          # 预习文档
├── preview/                 # 演示 SQL
├── homework/                # 作业题目与模板
├── submissions/             # 学生提交
├── grader/                  # 自动评测
└── .github/                 # Actions 与 PR 模板
```
