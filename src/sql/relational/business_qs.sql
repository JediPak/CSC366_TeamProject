-- Owner/Board III.
SELECT
    m.id,
    m.name,
    count(*) as total_orders
FROM
    lineItems i
    JOIN menuItem m
        ON i.menu_id = m.id
WHERE
    m.type in ('main_dish', 'premade_item')
GROUP BY m.id, m.name
ORDER BY count(*)
LIMIT 10

-- Owner/Board IV.
with 

revenue as (
    SELECT
        sum(m.price) revenue
    FROM
        receipt r
        JOIN lineItem i
            ON r.receipt_number = i.receipt_id
        JOIN menuItem m
            ON i.menu_id = m.id
    WHERE
        time between NOW() - INTERVAL 1 YEAR and NOW()
),

supplies as (
    SELECT
        1 as supply_outlays
)

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
        p.payperiod BETWEEN DATE_SUB(CUR_DATE(), INTERVAL 1 YEAR) and CUR_DATE
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
            te.timecard_id = t.id
    WHERE
        p.payperiod BETWEEN DATE_SUB(CUR_DATE(), INTERVAL 1 YEAR) and CUR_DATE
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
    supplies s
