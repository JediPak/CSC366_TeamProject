SET @myManagerId = 1;
SET @dateOfInterest = '2020-03-10'

-- What employees were on shift during a specific time?
WITH my_branch as (
    SELECT 
        b ->> 'branch_id'
    FROM
        branch b
        JOIN employee e
            b ->> 'manager_id' = e ->> 'emp_id'
    WHERE
        e ->> 'emp_id' = @myEmpId
),
timeCards AS (

    -- https://www.codeproject.com/Articles/1046120/Friday-the-th-JSON-is-coming-to-SQL-Server
    -- skip to polygon example

    SELECT 
        (pay ->> 'emp_role_id') AS 'EmpId',
        dateWorked,
        SUM(hoursWorked) AS 'TotalWorked'
    FROM OPENJSON(pay, '$.time_cards') as cards
       CROSS APPLY OPENJSON(cards.value) as lines
              CROSS APPLY OPENJSON(lines.value)
                     WITH (dateWorked date '$[0]', workType text '$[1]', hoursWorked number '$[2]')
    GROUP BY (pay ->> 'emp_role_id'), dateWorked
)

SELECT 
    (e ->> 'emp_id') AS 'EmpId',
    (e -> 'name' ->> 'first') AS 'FName',
    (e -> 'name' ->> 'last') AS 'LName'
FROM
    employee e
    JOIN timeCards tc
        ON (e ->> 'emp_id') = tc.EmpId
WHERE
    (e -> 'roles' ->> 'branch_id') in (select * from my_branch)
    and tc.dateWorked = @dateOfInterest;
;


-- What employees belong at the site I manage?
WITH my_branch as (
    SELECT 
        b ->> branch_id
    FROM
        branch b
        JOIN employee e
            b ->> manager_id = e ->> emp_id
    WHERE
        e ->> emp_id = @myEmpId
)

SELECT 
    (e ->> first) as FName, 
    (e ->> last) as LName, 
    (e ->> emp_id) as EmpId
FROM
    employee e
WHERE
    e -> roles ->> branch_id  in (select * from my_branch);


-- How many hours are my employees working? 
WITH timeCards AS (

    -- https://www.codeproject.com/Articles/1046120/Friday-the-th-JSON-is-coming-to-SQL-Server
    -- skip to polygon example

    SELECT 
        (pay ->> emp_role_id) AS 'EmpId',
        dateWorked,
        SUM(hoursWorked) AS 'TotalWorked'
    FROM OPENJSON(pay, '$.time_cards') as cards
       CROSS APPLY OPENJSON(cards.value) as lines
              CROSS APPLY OPENJSON(lines.value)
                     WITH (dateWorked date '$[0]', workType text '$[1]', hoursWorked number '$[2]')
    GROUP BY (pay ->> emp_role_id), dateWorked
)

SELECT 
    (e2 ->> emp_id) AS 'EmpId',
    dateWorked,
    TotalWorked
FROM
    employee e1
    JOIN employee e2
        ON (e1 ->> emp_id) = (e2 ->> manager_emp_id)
    JOIN timeCards tc
        ON (e2 ->> emp_id) = tc.EmpId
WHERE
    (e2 ->> end_date) is null
    AND (e1 ->> end_date) is null
    AND (e1 ->> emp_id) = @myEmpId
GROUP BY 1, 2;
