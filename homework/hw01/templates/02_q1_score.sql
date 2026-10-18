-- TODO: 把 0 改成 85
SELECT name, score
FROM members
WHERE score >= 0
ORDER BY score DESC, name ASC;
