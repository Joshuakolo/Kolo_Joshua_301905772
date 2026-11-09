-- Run these deliberately invalid statements one at a time, outside a transaction.
-- Each should fail at the named constraint; the sample rows should remain unchanged.

-- 1. customers pk. Expected: pk_customers, SQLSTATE 23505.
INSERT INTO portfolio."customers" ("customer_id", "email", "display_name", "created_at")
VALUES (1, 'pk-test@example.test', 'PK Test', '2026-03-01T09:00:00Z');

-- 2. customers unique. Expected: uq_customers_0, SQLSTATE 23505.
INSERT INTO portfolio."customers" ("customer_id", "email", "display_name", "created_at")
VALUES (9002, 'ava@example.test', 'Unique Test', '2026-03-01T09:00:00Z');

-- 3. customers not null. Expected: display_name, SQLSTATE 23502.
INSERT INTO portfolio."customers" ("customer_id", "email", "display_name", "created_at")
VALUES (9003, 'nn-test@example.test', NULL, '2026-03-01T09:00:00Z');

-- 4. products pk. Expected: pk_products, SQLSTATE 23505.
INSERT INTO portfolio."products" ("product_id", "sku", "product_name", "category", "current_price", "active")
VALUES (101, 'PK-TEST', 'PK Test Product', 'Test', 1, TRUE);

-- 5. products unique. Expected: uq_products_0, SQLSTATE 23505.
INSERT INTO portfolio."products" ("product_id", "sku", "product_name", "category", "current_price", "active")
VALUES (9102, 'MUG-001', 'Unique Test Product', 'Test', 1, TRUE);

-- 6. orders pk. Expected: pk_orders, SQLSTATE 23505.
INSERT INTO portfolio."orders" ("order_id", "customer_id", "order_date", "status")
VALUES (201, 1, '2026-03-01T09:00:00Z', 'completed');

-- 7. orders fk. Expected: fk_orders_0, SQLSTATE 23503.
INSERT INTO portfolio."orders" ("order_id", "customer_id", "order_date", "status")
VALUES (9202, 999999, '2026-03-01T09:00:00Z', 'completed');

-- 8. order items pk. Expected: pk_order_items, SQLSTATE 23505.
INSERT INTO portfolio."order_items" ("item_id", "order_id", "product_id", "quantity", "unit_price")
VALUES (301, 201, 101, 1, 1);

-- 9. order items order fk. Expected: fk_order_items_0, SQLSTATE 23503.
INSERT INTO portfolio."order_items" ("item_id", "order_id", "product_id", "quantity", "unit_price")
VALUES (9302, 999999, 101, 1, 1);

-- 10. order items product fk. Expected: fk_order_items_1, SQLSTATE 23503.
INSERT INTO portfolio."order_items" ("item_id", "order_id", "product_id", "quantity", "unit_price")
VALUES (9303, 201, 999999, 1, 1);

-- 11. order items check. Expected: positive_item_quantity, SQLSTATE 23514.
INSERT INTO portfolio."order_items" ("item_id", "order_id", "product_id", "quantity", "unit_price")
VALUES (9304, 201, 101, 0, 1);

-- 12. orders partial unique. Expected: one_cart_per_customer, SQLSTATE 23505.
INSERT INTO portfolio."orders" ("order_id", "customer_id", "order_date", "status")
VALUES (9203, 2, '2026-03-01T09:00:00Z', 'cart');
