SET @myManagerId = 1;
SET @dateOfInterest = '2020-03-10'

-- What employees were on shift during a specific time?
SELECT e.name FROM
Employee e
JOIN Role r
ON e.role = r.id
AND e.end_date = None
JOIN PayCheck p
ON r.id = p.emp_role
JOIN TimeCard t
ON p.id = t.paycheck_id
JOIN Entry en
ON t.id = en.timecard_id
AND en.date = dateOfInterest
;

-- What employees belong at the site I manage?
SELECT ei.name FROM
Employee e 
JOIN Branch b 
ON e.manager_id = b.manager_id
AND e.works_at_id = b.id
AND e.manager = myManagerId
JOIN EmployeeInfo ei
ON ei.emp_id = e.id
;

-- How many hours are my employees working? 
SELECT SUM(en.hours) FROM
Employee e
JOIN Role r
ON e.role = r.id
AND e.end_date = None
AND e.manager = myManagerId
JOIN PayCheck p
ON r.id = p.emp_role
JOIN TimeCard t
ON p.id = t.paycheck_id
AND t.is_approved = 1
AND t.week_of = NOW() - INTERVAL 1 WEEK
JOIN Entry en
ON t.id = en.timecard_id
;
