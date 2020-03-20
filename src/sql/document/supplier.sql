-- Supplier I
SELECT invoice ->> branch_id, item ->> item_id, MIN(invoice - >>order_date)
FROM invoice
JOIN branch
    ON invoice ->> branch_id = branch ->> id
JOIN invoice_item
    ON invoice ->> invoice_id = invoice_item ->> invoice_id
JOIN item
    ON invoice_item ->> item_id = item ->> id
GROUP BY invoice ->> branch_id, item ->> id
ORDER BY invoice ->> branch_id, item ->> id

-- Supplier II: Average time between orders for each branch
SELECT invoice ->> branch_id,
    AVG(TO_DATE(invoice ->> order_date, 'YYYY-MM-DD') - TO_DATE(LAG(invoice ->> order_date, 1), 'YYYY-MM-DD'))
        over (order by invoice ->> order_date)
FROM invoice
GROUP BY invoice ->> branch_id
ORDER BY  invoice ->> branch_id, invoice ->> order_date

-- Supplier III: Orders not delivered within 7 days
SELECT invoice ->> invoice_id as id
FROM invoice
WHERE CAST(invoice->>deliver_date AS INTEGER) - CAST(invoice->>order_date AS INTEGER) > 7
