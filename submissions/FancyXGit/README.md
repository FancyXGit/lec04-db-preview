# HW01

GitHub 用户名：FancyXGit

1. `WHERE` 是干什么的？
   答：`WHERE` 用来筛选行，只保留满足条件的记录，后面的查询、更新和删除都只作用于这些行。

2. 如果 `UPDATE` 不写 `WHERE` 会发生什么？
   答：MySQL 会把表里所有行的该列都改掉，而不只是目标那一行，容易造成数据被误改。

3. 四条查询里，哪一条你写得最久，为什么？
   答：第 4 条（分数最高的 3 位），因为要同时写对 `ORDER BY score DESC, name ASC` 和 `LIMIT 3`。
