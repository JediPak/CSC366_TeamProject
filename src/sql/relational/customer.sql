-- Customer I
SELECT 
	m.price
FROM 
	lineItem l,
	menuItem m
WHERE 
	l.receipt_id = 1 
	AND l.menu_id = m.id
	AND m.type = 'add_on';

-- Customer II
SELECT 
	ei.name
FROM 
	receipt r, 
	branch b, 
	employee e,
	employeeInfo ei
WHERE 
	r.receipt_number = 1
	AND e.emp_id = ei.emp_id
	AND b.id = r.branch_id 
	AND b.manager_id = e.id;

-- Customer III
WITH

ranks as (
	SELECT 
		i.name, 
		m.type,
		count(*) amount,
		rank() over (partition by m.type order by count(*) desc) rk
	FROM 
		lineItem l, 
		menuItem m,
		item i
	WHERE 
		l.receipt_id = 1 
		AND l.menu_id = m.id
		AND m.id = i.id
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
