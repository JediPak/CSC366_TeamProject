-- Supplier I
SELECT 
    invoice.branch_id, 
    item.name, 
    max(order_date) most_recent
FROM 
    invoice
    JOIN branch
        ON invoice.branch_id = branch.id
    JOIN invoiceItem
        ON invoice.invoice_id = invoiceItem.invoice_id
    JOIN item
        ON invoiceItem.item_id = item.id
GROUP BY invoice.branch_id, item.id
ORDER BY invoice.branch_id, item.id;

-- Supplier II
WITH

time_between as (
SELECT 
    branch_id,
    (order_date - lag(order_date) over (partition by branch_id order by order_date asc)) time_between_ship
FROM 
    invoice i
)

SELECT
    branch_id,
    avg(time_between_ship) as avg_time_between_ship
FROM
    time_between
GROUP BY branch_id;

-- Supplier II ALT
SELECT invoice_id,
    AVG(LAG(order_date,1))
        over (
            partition by branch_id
            order by order_date
        )
FROM invoice
ORDER BY branch_id, order_date

-- Supplier III
SELECT 
    invoice_id
FROM 
    invoice
WHERE 
    DATEDIFF(deliver_date, order_date) > 7;
