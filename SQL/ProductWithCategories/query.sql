select p.name as '�������', c.name as '���������' from product p
left join product_category pc on pc.product_id = p.id
left join category c on pc.category_id = c.id