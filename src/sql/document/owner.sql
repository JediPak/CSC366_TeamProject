-- Owner/Board I
WITH

expand_receipt as (
    SELECT
        receipt.receipt->>'branch_id' as branch,
        jsonb_array_elements_text(receipt.receipt->'line_items') as item
    FROM
        receipt
),

expand_menu as (
    SELECT
        jsonb_array_elements(menu_item->'menu_items')->>'name' as item,
        (jsonb_array_elements(menu_item->'menu_items')->>'price')::float as price
    FROM
        "menuItem"
)


SELECT
    branch,
    sum(price) as revenue
FROM
    expand_menu m
    JOIN expand_receipt r
        USING (item)
GROUP BY branch
ORDER BY sum(price) desc

-- Owner/Board II
WITH

expand_receipt as (
    SELECT
        (receipt.receipt->>'time')::timestamp as time,
        jsonb_array_elements_text(receipt.receipt->'line_items') as item
    FROM
        receipt
),

expand_menu as (
    SELECT
        jsonb_array_elements(menu_item->'menu_items')->>'name' as item,
        (jsonb_array_elements(menu_item->'menu_items')->>'price')::float as price
    FROM
        "menuItem"
)

SELECT
    to_char(r.time, 'day') as day,
    date_part('hour', r.time) as hour,
    sum(price) as revenue
FROM
    expand_menu m
    JOIN expand_receipt r
        USING (item)
GROUP BY extract(dow from r.time), 1, 2
ORDER BY extract(dow from r.time), 2 asc

WITH

-- Owner/Board III
expand_receipt as (
    SELECT
        jsonb_array_elements_text(receipt.receipt->'line_items') as item
    FROM
        receipt
),

expand_menu as (
    SELECT
        jsonb_array_elements(menu_item->'menu_items')->>'name' as item,
        jsonb_array_elements(menu_item->'menu_items')->>'item_type' as item_type
    FROM
        "menuItem"
)

SELECT
    item,
    count(*) as orders
FROM
    expand_menu m
    JOIN expand_receipt r
        USING (item)
GROUP BY item
ORDER BY count(*) desc

-- Owner/Board IV.
-- The issue I had designing a query for this problem was that the 
-- pay period is not well-defined. It is difficult to chase down
-- who worked when and at what pay rate. 
