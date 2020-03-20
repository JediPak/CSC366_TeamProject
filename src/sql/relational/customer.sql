-- Customer I
SELECT a.price
FROM LineItem as l, AddOn as a
WHERE l.receipt_id = 1 
AND l.menu_id = a.id

-- Customer II
SELECT e.name
FROM Receipt as r, Branch as b, Employee as e
WHERE r.receipt_number = 1 
AND b.id = r.branch_id 
AND b.manager_id = e.manager.id

-- Customer III
th main_count as (
	  SELECT m.name, count(m.name) as num
	  FROM LineItem as l, MainDish as m
	  WHERE l.receipt_id = 1 and l.menu_id = m.id
	  GROUP BY m.name
),
add_count as (
	  SELECT a.name, count(a.name) as num
	  FROM LineItem as l, AddOn as a
	  WHERE l.receipt_id = 1 and l.menu_id = a.id
	  GROUP BY a.name
),
premade_count as (
	  SELECT p.name, count(p.name) as num
	  FROM LineItem as l, PremadeItem as p
	  WHERE l.receipt_id = 1 and l.menu_id = p.id
	  GROUP BY p.name
)
SELECT name, MAX(num) as amount
FROM main_count
GROUP BY name
UNION
SELECT name, MAX(num) as amount
FROM add_count
GROUP BY name
UNION
SELECT name, MAX(num) as amount
FROM premade_count
GROUP BY name
ORDER BY amount
