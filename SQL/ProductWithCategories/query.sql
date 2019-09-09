select p.name as 'Продукт', c.name as 'Категория' from product p
left join product_category pc on pc.product_id = p.id
left join category c on pc.category_id = c.id