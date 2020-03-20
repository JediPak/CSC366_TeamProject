--List the employee that the employee manages.
SELECT e2 ->> id
FROM employee as e1 JOIN employee as e2
WHERE e1 ->> id != e2 ->> id 
AND e1 ->> id = e2 ->> manager_id 
AND e1 ->> id = 1 /*<user_input>*/

--How many hours did the employee work in the span of date A until date B 
---(inclusive)? (*had to change date from time, since we don’t save times*)
-- https://www.codeproject.com/Articles/1046120/Friday-the-th-JSON-is-coming-to-SQL-Server
-- skip to polygon example
-- https://www.codeproject.com/Articles/1046120/Friday-the-th-JSON-is-coming-to-SQL-Server
    -- skip to polygon example
SELECT pay ->> emp_role_id) AS 'EmpId',
    SUM(hoursWorked) AS 'TotalWorked'
    FROM(
        SELECT 
            (pay ->> emp_role_id) AS 'EmpId',
            dateWorked,
            SUM(hoursWorked) AS 'TotalWorked'
        FROM (
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
        WHERE dateWorked >= <dateA_input> AND dateWorked <= <dateB_input>
    )
