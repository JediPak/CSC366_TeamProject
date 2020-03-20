--List the employee that the employee manages.
SELECT e2.id
FROM employee as e1 JOIN employee as e2
WHERE e1.id != e2.id 
AND e1.id = e2.manager_id 
AND e1.id = 1 /*<user_input>*/

--How many hours did the employee work in the span of date A until date B 
---(inclusive)? (*had to change date from time, since we don’t save times*)
SELECT SUM(en.hours) FROM
employee as e JOIN PayCheck p
ON e.id = p.emp_role_id
JOIN TimeCard t
ON p.id = t.paycheck_id
AND t.is_approved = 1
JOIN Entry as en
ON t.id = en.timecard_id
AND t.date <= Cast('07/01/2020' as datetime)/*<dateB_input>*/ 
AND t.date > Cast('07/02/2011' as datetime)/*<dateA_input> */
AND e.id = 1 /*<employee_id_input>*/;

