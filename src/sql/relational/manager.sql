SET @myEmpId = 1;
SET @dateOfInterest = "2020-03-10";

-- What employees were on shift during a specific time?
WITH

my_branch as (
    SELECT
        b.id
    FROM
        branch b
        JOIN employee e
            ON b.manager_id = e.id
    WHERE
        e.emp_id = @myEmpId
)

SELECT 
    ei.name 
FROM
    employee e
    JOIN employeeInfo ei
        ON e.emp_id = ei.emp_id
WHERE
    e.works_at_id in (select * from my_branch);

-- What employees belong at the site I manage?
WITH

my_branch as (
    SELECT
        b.id
    FROM
        branch b
        JOIN employee e
            ON b.manager_id = e.id
    WHERE
        e.emp_id = @myEmpId
)

SELECT 
    ei.name 
FROM
    employee e
    JOIN employeeInfo ei
        ON e.emp_id = ei.emp_id
WHERE
    e.works_at_id in (select * from my_branch);

-- How many hours are my employees working? 
SELECT 
    e2.emp_id,
    t.week_of,
    SUM(en.hours) 
FROM
    employee e1
    JOIN employee e2
        ON e1.id = e2.manager_id
    JOIN paycheck p
        ON e2.id = p.emp_role_id
    JOIN timeCard t
        ON p.id = t.paycheck_id
    JOIN timeCardEntry en
        ON t.id = en.timecard_id
WHERE
    e2.end_date is null
    and e1.end_date is null
    and e1.emp_id = @myEmpId
    AND t.is_approved
GROUP BY 1, 2;
