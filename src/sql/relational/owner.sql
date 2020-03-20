-- Owner/Board I
SELECT
    r.branch_id branch, 
    sum(m.price) revenue
FROM
    receipt r
    JOIN lineItem i
        ON r.receipt_number = i.receipt_id
    JOIN menuItem m
        ON i.menu_id = m.id
WHERE
    r.time between NOW() - INTERVAL 1 YEAR and NOW()
GROUP BY r.branch_id
ORDER BY r.branch_id;

-- Owner/Board II.
SELECT
    DAYNAME(r.time) day, 
    HOUR(r.time) hour,
    sum(m.price) revenue
FROM
    receipt r
    JOIN lineItem i
        ON r.receipt_number = i.receipt_id
    JOIN menuItem m
        ON i.menu_id = m.id
WHERE
    r.time between NOW() - INTERVAL 1 YEAR and NOW()
GROUP BY DAYOFWEEK(r.time), DAYNAME(r.time), HOUR(r.time)
ORDER BY DAYOFWEEK(r.time), HOUR(r.time);

-- Owner/Board III.
SELECT
    m.id,
    i.name,
    count(*) as total_orders
FROM
    lineItem li
    JOIN menuItem m
        ON li.menu_id = m.id
    JOIN item i
        ON m.id = i.id
WHERE
    m.type in ('main_dish', 'premade_item')
GROUP BY m.id, i.name
ORDER BY count(*)
LIMIT 10;

-- Owner/Board IV.
WITH 

revenue as (
    SELECT
        sum(m.price) as revenue
    FROM
        receipt r
        JOIN lineItem i
            ON r.receipt_number = i.receipt_id
        JOIN menuItem m
            ON i.menu_id = m.id
    WHERE
        r.time between NOW() - INTERVAL 1 YEAR and NOW()
),

supplies as (
    SELECT
        sum(ii.price) as supply_outlays
    FROM
        invoice i
        JOIN invoiceItem ii
            ON i.invoice_id = ii.invoice_id
    WHERE
        i.order_date between NOW() - INTERVAL 1 YEAR and NOW()
),

payroll_salary as (
    SELECT
        sum(r.rate) as salary_pay
    FROM
        paycheck p
        JOIN employee e
            ON e.id = p.emp_role_id
        JOIN `role` r
            ON r.id = e.role_id
    WHERE
        p.payperiod BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) and CURDATE()
        and r.exempt
),

payroll_hourly as (
    SELECT
        sum(if(te.hour_type = 'OVERTIME', te.hours * r.rate * 1.5, te.hours * r.rate)) as hourly_pay
    FROM
        paycheck p
        JOIN employee e
            ON e.id = p.emp_role_id
        JOIN `role` r
            ON r.id = e.role_id
        JOIN timeCard t
            ON p.id = t.paycheck_id
        JOIN timeCardEntry te
            ON te.timecard_id = t.id
    WHERE
        p.payperiod BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) and CURDATE()
        and not r.exempt
)

SELECT
    r.revenue,
    ps.salary_pay,
    ph.hourly_pay,
    s.supply_outlays
FROM
    revenue r,
    payroll_salary ps,
    payroll_hourly ph,
    supplies s;
