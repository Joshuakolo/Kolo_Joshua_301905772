-- Fictional sample records for E-commerce Platform.
BEGIN;
SET LOCAL standard_conforming_strings = on;
INSERT INTO portfolio."customers" ("customer_id", "email", "display_name", "created_at") VALUES (1, 'ava@example.test', 'Ava Chen', '2026-01-10T09:00:00Z');
INSERT INTO portfolio."customers" ("customer_id", "email", "display_name", "created_at") VALUES (2, 'noah@example.test', 'Noah Kim', '2026-01-11T10:30:00Z');
INSERT INTO portfolio."products" ("product_id", "sku", "product_name", "category", "current_price", "active") VALUES (101, 'MUG-001', 'Ceramic Mug', 'Home', 12.5, TRUE);
INSERT INTO portfolio."products" ("product_id", "sku", "product_name", "category", "current_price", "active") VALUES (102, 'NOTE-001', 'Notebook', 'Stationery', 8.25, TRUE);
INSERT INTO portfolio."orders" ("order_id", "customer_id", "order_date", "status") VALUES (201, 1, '2026-02-01T12:00:00Z', 'completed');
INSERT INTO portfolio."orders" ("order_id", "customer_id", "order_date", "status") VALUES (202, 2, '2026-02-02T15:30:00Z', 'cart');
INSERT INTO portfolio."order_items" ("item_id", "order_id", "product_id", "quantity", "unit_price") VALUES (301, 201, 101, 2, 12.5);
INSERT INTO portfolio."order_items" ("item_id", "order_id", "product_id", "quantity", "unit_price") VALUES (302, 202, 102, 1, 8.25);
COMMIT;
