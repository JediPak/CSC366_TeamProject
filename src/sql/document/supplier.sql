-- Supplier I
SELECT invoice ->> branch_id, item ->> item_id, MIN(invoice - >>order_date)
FROM invoice
JOIN invoice_item
    ON invoice ->> invoice_id = invoice_item ->> invoice_id
JOIN item
    ON invoice_item ->> item_id = item ->> id
GROUP BY invoice ->> branch_id, item ->> id
ORDER BY invoice ->> branch_id, item ->> id


-- Supplier II: Average time between orders for each branch
WITH

time_between as (
SELECT
    invoice ->> branch_id,
    (TO_DATE(invoice ->> order_date, 'YYYY-MM-DD') - TO_DATE(LAG(invoice ->> order_date), 'YYYY-MM-DD') over
        (partition by invoice ->> branch_id order by invoice ->> order_date asc)) time_between_ship
FROM
    invoice i
)

SELECT
    invoice ->> branch_id,
    avg(time_between_ship) as avg_time_between_ship
FROM
    time_between
GROUP BY invoice ->> branch_id;


-- Supplier III: Orders not delivered within 7 days
SELECT invoice ->> invoice_id as id
FROM invoice
WHERE CAST(invoice->>deliver_date AS INTEGER) - CAST(invoice->>order_date AS INTEGER) > 7
