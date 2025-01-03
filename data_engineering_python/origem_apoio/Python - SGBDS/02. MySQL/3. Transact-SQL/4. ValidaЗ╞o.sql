use python

SET SQL_SAFE_UPDATES = 0;

delete FROM python.order_items;
delete FROM python.orders;
delete FROM python.customers;
delete FROM python.products;
delete FROM python.categories;
delete FROM python.stores;


SELECT count(*) as categorias FROM python.categories;
SELECT count(*) as Clientes FROM python.customers;
SELECT count(*) as ord_items FROM python.order_items;
SELECT count(*) as orders FROM python.orders
SELECT count(*) as products FROM python.products
SELECT count(*) as stores FROM python.stores


SELECT  * FROM python.categories;
SELECT  * FROM python.customers;
SELECT  * FROM python.order_items;
SELECT  * FROM python.orders;
SELECT  * FROM python.products;
SELECT  * FROM python.stores;