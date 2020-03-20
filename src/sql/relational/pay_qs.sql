SET @myEmpId = 1;
SET @otherEmpId = 2;

--List the employee that the employee manages.
SELECT 
    e2.emp_id
FROM 
    employee e1,
    employee e2
WHERE 
    e1.id = e2.manager_id 
    and e2.end_date is null
    and e1.end_date is null
    and e1.emp_id = @myEmpId;

--How many hours did the employee work in the span of date A until date B 
---(inclusive)? (*had to change date from time, since we don’t save times*)
SELECT 
    SUM(en.hours) 
FROM
    employee e 
    JOIN paycheck p
        ON e.id = p.emp_role_id
    JOIN timeCard t
        ON p.id = t.paycheck_id
        AND t.is_approved
    JOIN timeCardEntry en
        ON t.id = en.timecard_id
        AND en.date <= Cast('2020-03-19' as datetime)/*<dateB_input>*/ 
        AND en.date > Cast('2020-03-20' as datetime)/*<dateA_input> */
        AND e.emp_id = @otherEmpId; /*<employee_id_input>*/

