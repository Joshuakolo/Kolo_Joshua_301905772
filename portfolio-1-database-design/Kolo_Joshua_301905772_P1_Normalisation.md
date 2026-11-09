# E-commerce Platform — normalisation

The example uses the saved sample records. The full set of fields is in the design and schema.

## Starting grouped records

| customer_id | orders records (list) |
| --- | --- |
| 1 | [201] |
| 2 | [202] |


The record IDs are grouped in a list. In 1NF, each record has its own row and each cell holds one value.

## 1NF: one value per cell

| orders.order_id | orders.customer_id | orders.status | customers.customer_id | customers.email |
| --- | --- | --- | --- | --- |
| 201 | 1 | completed | 1 | ava@example.test |
| 202 | 2 | cart | 2 | noah@example.test |

Key: order_id.

## 2NF: depend on the whole key

The declared candidate keys do not introduce a partial dependency here, so the 1NF rows stay unchanged at this step.

## orders_example

| orders.order_id | orders.customer_id | orders.status | customers.customer_id | customers.email |
| --- | --- | --- | --- | --- |
| 201 | 1 | completed | 1 | ava@example.test |
| 202 | 2 | cart | 2 | noah@example.test |

## 3NF: store each entity’s details once

The entity keys determine their own descriptions. Related records keep foreign keys rather than repeating those descriptions.

## customers

| customer_id | email | display_name | created_at |
| --- | --- | --- | --- |
| 1 | ava@example.test | Ava Chen | 2026-01-10T09:00:00+00:00 |
| 2 | noah@example.test | Noah Kim | 2026-01-11T10:30:00+00:00 |

## products

| product_id | sku | product_name | category | current_price | active |
| --- | --- | --- | --- | --- | --- |
| 101 | MUG-001 | Ceramic Mug | Home | 12.5 | true |
| 102 | NOTE-001 | Notebook | Stationery | 8.25 | true |

## orders

| order_id | customer_id | order_date | status |
| --- | --- | --- | --- |
| 201 | 1 | 2026-02-01T12:00:00+00:00 | completed |
| 202 | 2 | 2026-02-02T15:30:00+00:00 | cart |

## order_items

| item_id | order_id | product_id | quantity | unit_price |
| --- | --- | --- | --- | --- |
| 301 | 201 | 101 | 2 | 12.5 |
| 302 | 202 | 102 | 1 | 8.25 |

## Dependencies

- customers: (customer_id) → email, display_name, created_at
- products: (product_id) → sku, product_name, category, current_price, active
- orders: (order_id) → customer_id, order_date, status
- order_items: (item_id) → order_id, product_id, quantity, unit_price

Joining the decomposed sample tables reproduces the original 2 example rows. The design assumes the declared keys describe the relevant business dependencies.
