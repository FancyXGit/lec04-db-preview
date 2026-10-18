#!/usr/bin/env python3
"""HW01 自动评测：DML 状态检查 + 查询结果比对。"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pymysql
from pymysql.constants import CLIENT

REPO_ROOT = Path(__file__).resolve().parent.parent
INIT_SQL = REPO_ROOT / "preview" / "init.sql"
EVAL_SEED_SQL = REPO_ROOT / "grader" / "fixtures" / "eval_seed.sql"

DB_NAME = os.getenv("MYSQL_DATABASE", "hw01")
if not re.fullmatch(r"[A-Za-z0-9_]+", DB_NAME):
    raise SystemExit("MYSQL_DATABASE 只能包含字母、数字和下划线")

PASS_SCORE = 80

REQUIRED_FILES = [
    "01_dml.sql",
    "02_q1_score.sql",
    "03_q2_major.sql",
    "04_q3_like.sql",
    "05_q4_top3.sql",
    "README.md",
]

QUERY_SPECS = [
    {
        "file": "02_q1_score.sql",
        "name": "Q1 分数筛选",
        "columns": ["name", "score"],
        "rows": [
            ("林二", "95.00"),
            ("周七", "90.00"),
            ("吴六", "88.00"),
            ("张五", "87.00"),
            ("郑八", "86.00"),
        ],
    },
    {
        "file": "03_q2_major.sql",
        "name": "Q2 专业筛选",
        "columns": ["name", "major"],
        "rows": [
            ("陈一", "计算机"),
            ("张五", "计算机"),
            ("周七", "计算机"),
        ],
    },
    {
        "file": "04_q3_like.sql",
        "name": "Q3 模糊查询",
        "columns": ["name"],
        "rows": [("张五",)],
    },
    {
        "file": "05_q4_top3.sql",
        "name": "Q4 排序截断",
        "columns": ["name", "score"],
        "rows": [
            ("林二", "95.00"),
            ("周七", "90.00"),
            ("吴六", "88.00"),
        ],
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def strip_comments(sql: str) -> str:
    """去掉 -- 行注释和 /* */ 块注释，保留字符串里的内容。"""
    out: list[str] = []
    i = 0
    in_single = in_double = in_backtick = False
    while i < len(sql):
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < len(sql) else ""
        if not (in_single or in_double or in_backtick):
            if ch == "-" and nxt == "-":
                j = sql.find("\n", i)
                if j == -1:
                    break
                out.append("\n")
                i = j + 1
                continue
            if ch == "/" and nxt == "*":
                j = sql.find("*/", i + 2)
                if j == -1:
                    break
                out.append(" ")
                i = j + 2
                continue
            if ch == "'":
                in_single = True
            elif ch == '"':
                in_double = True
            elif ch == "`":
                in_backtick = True
        else:
            if ch == "\\" and not in_backtick:
                out.append(ch)
                if i + 1 < len(sql):
                    out.append(sql[i + 1])
                    i += 2
                    continue
            elif ch == "'" and in_single:
                in_single = False
            elif ch == '"' and in_double:
                in_double = False
            elif ch == "`" and in_backtick:
                in_backtick = False
        out.append(ch)
        i += 1
    return "".join(out)


def split_statements(sql: str) -> list[str]:
    body = strip_comments(sql)
    parts: list[str] = []
    current: list[str] = []
    in_single = in_double = in_backtick = False
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "'" and not (in_double or in_backtick):
            in_single = not in_single
        elif ch == '"' and not (in_single or in_backtick):
            in_double = not in_double
        elif ch == "`" and not (in_single or in_double):
            in_backtick = not in_backtick
        if ch == ";" and not (in_single or in_double or in_backtick):
            statement = "".join(current).strip()
            if statement:
                parts.append(statement)
            current = []
        else:
            current.append(ch)
        i += 1
    statement = "".join(current).strip()
    if statement:
        parts.append(statement)
    return parts


def first_keyword(statement: str) -> str:
    match = re.match(r"\s*([A-Za-z_]+)", statement)
    return match.group(1).upper() if match else ""


def norm(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def connect(with_db: bool = True):
    kwargs = dict(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        charset="utf8mb4",
        autocommit=True,
        client_flag=CLIENT.MULTI_STATEMENTS,
    )
    if with_db:
        kwargs["database"] = DB_NAME
    return pymysql.connect(**kwargs)


def reset_database() -> None:
    conn = connect(with_db=False)
    try:
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS `{DB_NAME}`")
            cur.execute(
                f"CREATE DATABASE `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
            )
    finally:
        conn.close()


def execute_script(conn, script: str) -> None:
    with conn.cursor() as cur:
        cur.execute(script)
        while cur.nextset():
            pass


def run_query(conn, statement: str):
    with conn.cursor() as cur:
        cur.execute(statement)
        columns = [item[0] for item in cur.description] if cur.description else []
        rows = cur.fetchall() if cur.description else []
        if cur.nextset():
            raise ValueError("查询文件只能包含一条 SELECT")
        return columns, rows


def fetch(conn, sql: str, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def setup_database(with_eval_seed: bool = False):
    reset_database()
    conn = connect(with_db=True)
    execute_script(conn, read_text(INIT_SQL))
    if with_eval_seed:
        execute_script(conn, read_text(EVAL_SEED_SQL))
    return conn


def check_dml(conn, submission_dir: Path, username: str):
    path = submission_dir / "01_dml.sql"
    if not path.exists():
        return [
            ("DML 新增", False, "文件不存在"),
            ("DML 修改", False, "文件不存在"),
            ("DML 删除", False, "文件不存在"),
            ("DML 批量新增", False, "文件不存在"),
        ]

    try:
        execute_script(conn, read_text(path))
    except Exception as exc:  # noqa: BLE001 - 需要把数据库错误展示给学生
        reason = f"执行失败：{exc}"
        return [
            ("DML 新增", False, reason),
            ("DML 修改", False, "未执行"),
            ("DML 删除", False, "未执行"),
            ("DML 批量新增", False, "未执行"),
        ]

    checks = []

    inserted = fetch(
        conn,
        "SELECT class_name, major, score FROM members WHERE name = %s",
        (username,),
    )
    insert_ok = (
        len(inserted) == 1
        and inserted[0][0] == "2025-1"
        and inserted[0][1] == "计算机"
        and norm(inserted[0][2]) == "90.00"
    )
    checks.append(
        (
            "DML 新增",
            insert_ok,
            f"应存在一条 name={username}、班级 2025-1、专业 计算机、分数 90.00 的记录",
        )
    )

    updated = fetch(conn, "SELECT score FROM members WHERE id = 1")
    update_ok = len(updated) == 1 and norm(updated[0][0]) == "80.00"
    checks.append(("DML 修改", update_ok, "id=1 的 score 应为 80.00"))

    deleted = fetch(conn, "SELECT COUNT(*) FROM members WHERE id = 4")
    delete_ok = deleted[0][0] == 0
    checks.append(("DML 删除", delete_ok, "id=4 应不存在"))

    batch = fetch(
        conn,
        """
        SELECT class_name, major, score
        FROM members
        WHERE (class_name, major, score) IN (
          ('2023-3', '数学', 70),
          ('2024-3', '英语', 60),
          ('2022-2', '计算机', 95)
        )
        """,
    )
    total = fetch(conn, "SELECT COUNT(*) FROM members")[0][0]
    batch_ok = len(batch) == 3 and total == 8
    checks.append(
        (
            "DML 批量新增",
            batch_ok,
            f"应有 3 条指定记录，且总行数为 8；实际匹配 {len(batch)} 条、总行数 {total}",
        )
    )
    return checks


def check_query(conn, path: Path, spec: dict):
    if not path.exists():
        return False, "文件不存在"

    try:
        raw = read_text(path)
    except Exception as exc:  # noqa: BLE001
        return False, f"读取失败：{exc}"

    statements = split_statements(raw)
    if len(statements) != 1:
        return False, f"只能有一条 SELECT，当前有 {len(statements)} 条语句"

    statement = statements[0]
    if first_keyword(statement) not in ("SELECT", "WITH"):
        return False, "必须是一条 SELECT"

    body = strip_comments(statement).lower()
    if "order by" not in body:
        return False, "缺少 ORDER BY"

    try:
        columns, rows = run_query(conn, statement)
    except Exception as exc:  # noqa: BLE001
        return False, f"执行失败：{exc}"

    actual_columns = [column.lower() for column in columns]
    expected_columns = [column.lower() for column in spec["columns"]]
    if actual_columns != expected_columns:
        return False, f"列名应为 {spec['columns']}，实际为 {columns}"

    actual_rows = [tuple(norm(value) for value in row) for row in rows]
    if actual_rows != spec["rows"]:
        return False, f"结果不一致：期望 {spec['rows']}，实际 {actual_rows}"

    return True, f"{len(actual_rows)} 行，结果正确"


def check_readme(submission_dir: Path, username: str):
    path = submission_dir / "README.md"
    if not path.exists():
        return False, "文件不存在"

    try:
        text = read_text(path)
    except Exception as exc:  # noqa: BLE001
        return False, f"读取失败：{exc}"

    lower = text.lower()
    if "<your-github-username>" in lower:
        return False, "还有 <your-github-username> 占位符没有替换"
    if username.lower() not in lower:
        return False, f"README 里要写 GitHub 用户名 {username}"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if len(lines) < 6:
        return False, "至少写 3 行回答，每行不要只写问题"

    answers = [line for line in lines if line.startswith("答：")]
    if len(answers) < 3 or any(len(line) <= 2 for line in answers):
        return False, "请在三个“答：”后面分别写回答"

    return True, "已填写"


def check_hygiene(submission_dir: Path, username: str):
    missing = [name for name in REQUIRED_FILES if not (submission_dir / name).exists()]
    if missing:
        return False, "缺少文件：" + ", ".join(missing)
    if submission_dir.parent.name.lower() != username.lower():
        return False, f"目录名应为 submissions/{username}/hw01/"

    return True, "6 个文件齐全"


def emit_report(items, score: int, passed: bool, username: str) -> None:
    lines = [
        "## 自动评测结果",
        "",
        f"GitHub 用户：`{username}`",
        "",
        "| 项目 | 结果 | 说明 | 得分 |",
        "| --- | --- | --- | ---: |",
    ]
    for name, ok, message, points in items:
        lines.append(f"| {name} | {'✅' if ok else '❌'} | {message} | {points} |")

    lines.extend(
        [
            "",
            f"**总分：{score} / 100**",
            "",
            "通过。" if passed else "未通过。按上面的说明修改后，在同一个分支继续 push。",
        ]
    )
    report = "\n".join(lines)
    print(report)

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write(report + "\n")

    for name, ok, message, _ in items:
        if not ok:
            print(f"::error::{name}: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="HW01 自动评测")
    parser.add_argument("--submission", default=os.getenv("SUBMISSION_DIR"))
    parser.add_argument("--github-user", default=os.getenv("GITHUB_USER"))
    args = parser.parse_args()

    if not args.submission or not args.github_user:
        print("缺少 --submission 或 --github-user", file=sys.stderr)
        return 2

    submission_dir = Path(args.submission)
    if not submission_dir.is_absolute():
        submission_dir = REPO_ROOT / submission_dir
    submission_dir = submission_dir.resolve()

    submissions_root = (REPO_ROOT / "submissions").resolve()
    if submissions_root not in submission_dir.parents:
        print("提交目录必须在 submissions/ 下", file=sys.stderr)
        return 2

    username = args.github_user.strip()
    items = []

    hygiene_ok, hygiene_message = check_hygiene(submission_dir, username)
    items.append(("提交规范", hygiene_ok, hygiene_message, 10 if hygiene_ok else 0))

    readme_ok, readme_message = check_readme(submission_dir, username)
    items.append(("README", readme_ok, readme_message, 10 if readme_ok else 0))

    try:
        conn = setup_database()
    except Exception as exc:  # noqa: BLE001
        print(f"无法初始化数据库：{exc}", file=sys.stderr)
        return 2

    try:
        for name, ok, message in check_dml(conn, submission_dir, username):
            items.append((name, ok, message, 10 if ok else 0))
    finally:
        conn.close()

    try:
        conn = setup_database(with_eval_seed=True)
    except Exception as exc:  # noqa: BLE001
        print(f"无法加载评测数据：{exc}", file=sys.stderr)
        return 2

    try:
        for spec in QUERY_SPECS:
            ok, message = check_query(conn, submission_dir / spec["file"], spec)
            items.append((spec["name"], ok, message, 10 if ok else 0))
    finally:
        conn.close()

    score = sum(points for _, _, _, points in items)
    passed = score >= PASS_SCORE
    emit_report(items, score, passed, username)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
