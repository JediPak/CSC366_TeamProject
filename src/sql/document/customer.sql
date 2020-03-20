-- Customer I
SELECT
	menu -> 'menu_items' -> 'items' ->> 'price' as FLOAT
FROM
	receipt, menu
WHERE
	receipt ->> 'number' = 1
	menu -> 'menu_items' -> 'items' ->> 'name' =  receipt -> 'line_items' -> 'name'
	menu -> 'menu_items' -> 'items' ->> 'item_type' = 'addon'
