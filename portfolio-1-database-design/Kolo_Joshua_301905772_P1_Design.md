# E-commerce Platform — database design

My case study records customers, products, orders, order_items.

## Users

- Customers placing and reviewing orders
- Store staff reviewing order activity

## Main operations

- Create an order and add product line items
- Find a customer's recent orders
- Summarize units and sales by product

## Entities

| Entity | Information stored |
| --- | --- |
| customers | Stores synthetic customer identity and account creation details. |
| products | Stores the catalog attributes used to describe products on sale. |
| orders | Stores order-level ownership, date, and lifecycle status. |
| order_items | Stores product-specific quantities and price snapshots for each order. |

## customers

| Field | Type | Key | Required |
| --- | --- | --- | --- |
| customer_id | BIGINT | PK | Yes |
| email | TEXT | Unique | Yes |
| display_name | TEXT |  | Yes |
| created_at | TIMESTAMPTZ |  | Yes |
- Unique key: (email).

## products

| Field | Type | Key | Required |
| --- | --- | --- | --- |
| product_id | BIGINT | PK | Yes |
| sku | TEXT | Unique | Yes |
| product_name | TEXT |  | Yes |
| category | TEXT |  | Yes |
| current_price | NUMERIC(18,2) |  | Yes |
| active | BOOLEAN |  | Yes |
- Unique key: (sku).

## orders

| Field | Type | Key | Required |
| --- | --- | --- | --- |
| order_id | BIGINT | PK | Yes |
| customer_id | BIGINT | FK | Yes |
| order_date | TIMESTAMPTZ |  | Yes |
| status | TEXT |  | Yes |
- customer_id → customers.customer_id

## order_items

| Field | Type | Key | Required |
| --- | --- | --- | --- |
| item_id | BIGINT | PK | Yes |
| order_id | BIGINT | FK | Yes |
| product_id | BIGINT | FK | Yes |
| quantity | INTEGER |  | Yes |
| unit_price | NUMERIC(18,2) |  | Yes |
- order_id → orders.order_id
- product_id → products.product_id

## Relationships and business rules

- Each customer email identifies at most one customer.
- Every order must reference an existing customer.
- Every order item must have a quantity greater than zero.
- A customer may have at most one order whose status is cart; enforce a partial unique constraint on customer_id for rows with status cart.

## Assumptions

- Each order belongs to exactly one customer; each line item refers to exactly one order and one product.
- A product's unit price is recorded on the line item so later product price changes do not alter historical order data.
- An order with status cart is an open cart; at most one such cart may exist per customer.
- The exercise uses no real customer, payment, or student data.

