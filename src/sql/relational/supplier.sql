-- Supplier I
SELECT invoice.branch_id, item.item_id, MIN(order_date)
FROM invoice
JOIN branch
    ON invoice.branch_id = branch.id
JOIN invoice_item
    ON invoice.invoice_id = invoice_item.invoice_id
JOIN item
    ON invoice_item.item_id = item.id
GROUP BY invoice.branch_id, item.id
ORDER BY invoice.branch_id, item.id

-- Supplier II
SELECT i1.branch_id, AVG(i2.order_date-i1.order_date)
FROM invoice i1
JOIN invoice i2
    ON i2.invoice_id = (
        SELECT id
        FROM invoice i3
        WHERE i3.order_date > i2.order_date
            AND i3.branch_id = i2.branch_id
        ORDER BY i2.order_date
        LIMIT 1
    )
        AND i1.branch_id = i2.branch_id

-- Supplier III
SELECT invoice_id
FROM invoice
WHERE DATEDIFF(deliver_date, order_date) > 7
