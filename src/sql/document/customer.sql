-- Customer I
SELECT
	menu -> 'menu_items' -> 'items' ->> 'price' as FLOAT
FROM
	receipt, menu
WHERE
	receipt ->> 'number' = 1
	menu -> 'menu_items' -> 'items' ->> 'menu_id' =  receipt -> 'line_items' -> 'items' ->> 'menu_id'
	menu -> 'menu_items' -> 'items' ->> 'item_type' = 'addon';

-- Customer II
SELECT
	employee -> 'name' ->> 'first' as VARCHAR
FROM
	receipt, branch, employee 
WHERE
	receipt ->> 'number' = 1
	AND receipt ->> 'branch_id' = branch ->> 'branch_id'
	AND branch ->> 'manager_id' = employee ->> 'emp_id';

-- Customer III
WITH

rank as (
	SELECT
		menu -> 'menu_items' -> 'items' ->> 'name' as VARCHAR
		menu -> 'menu_items' -> 'items' ->> 'item_type' as VARCHAR
		COUNT(*) as amount,
		rank() over (partition by menu -> 'menu_items' -> 'items' -> 'item_type' order by count(*) desc) as rk
	FROM
		receipt,
		menu
	WHERE
		receipt ->> 'number' = 1
		menu -> 'menu_items' -> 'items' ->> 'menu_id' =  receipt -> 'line_items' -> 'items' ->> 'menu_id'
	GROUP BY 1
)

SELECT
	name,
	type,
	amount
FROM
	ranks
WHERE
	rk = 1;
