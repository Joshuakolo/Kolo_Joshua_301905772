# E-commerce Platform — SQL queries

## 1. Show related orders, customers, order_items, products records (up to 20).

```sql
SELECT t0."order_id" AS "orders_order_id",
       t0."order_date" AS "orders_order_date",
       t3."customer_id" AS "customers_customer_id",
       t3."email" AS "customers_email",
       t1."item_id" AS "order_items_item_id",
       t1."quantity" AS "order_items_quantity",
       t2."product_id" AS "products_product_id",
       t2."sku" AS "products_sku"
FROM portfolio."orders" t0
JOIN portfolio."order_items" t1 ON t1."order_id" = t0."order_id"
JOIN portfolio."products" t2 ON t1."product_id" = t2."product_id"
JOIN portfolio."customers" t3 ON t0."customer_id" = t3."customer_id"
ORDER BY t0."order_id", t3."customer_id", t1."item_id", t2."product_id"
LIMIT 20;
```

| orders_order_id | orders_order_date | customers_customer_id | customers_email | order_items_item_id | order_items_quantity | products_product_id | products_sku |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 201 | 2026-02-01T12:00:00+00:00 | 1 | ava@example.test | 301 | 2 | 101 | MUG-001 |
| 202 | 2026-02-02T15:30:00+00:00 | 2 | noah@example.test | 302 | 1 | 102 | NOTE-001 |

## 2. Find customers records where email matches "ava@example.test" (up to 20).

```sql
SELECT * FROM portfolio."customers"
WHERE "email" IS NOT DISTINCT FROM 'ava@example.test'
ORDER BY "customer_id"
LIMIT 20;
```

| customer_id | email | display_name | created_at |
| --- | --- | --- | --- |
| 1 | ava@example.test | Ava Chen | 2026-01-10T09:00:00+00:00 |

## 3. Count order_items records for each order_id (up to 20 groups).

```sql
SELECT "order_id", count(*) AS record_count
FROM portfolio."order_items"
GROUP BY "order_id"
ORDER BY record_count DESC, "order_id" NULLS LAST
LIMIT 20;
```

| order_id | record_count |
| --- | --- |
| 201 | 1 |
| 202 | 1 |


## Index comparison

| Phase | Median (ms) | Three runs (ms) | Plan nodes | Buffer hits |
| --- | --- | --- | --- | --- |
| Before index | 1.129 | 1.393, 1.129, 0.998 | Sort → Seq Scan | 112 |
| After index | 0.175 | 0.175, 0.174, 0.195 | Sort → Bitmap Heap Scan → Bitmap Index Scan | 25 |

The median execution time changed from 1.129 ms to 0.175 ms. The measured plan used p2_filter_idx. The results matched in both phases. An index adds storage and write-maintenance costs; timings depend on the selected lookup and environment.

## Execution plans

### Before index, run 1

```text
Sort (actual time=1.36..1.361 rows=20 loops=1)
  Seq Scan on orders (actual time=0.022..1.315 rows=20 loops=1)
Planning Time: 0.427 ms
Execution Time: 1.393 ms
```

### Before index, run 2

```text
Sort (actual time=1.067..1.095 rows=20 loops=1)
  Seq Scan on orders (actual time=0.014..1.058 rows=20 loops=1)
Planning Time: 0.298 ms
Execution Time: 1.129 ms
```

### Before index, run 3

```text
Sort (actual time=0.97..0.972 rows=20 loops=1)
  Seq Scan on orders (actual time=0.014..0.936 rows=20 loops=1)
Planning Time: 0.326 ms
Execution Time: 0.998 ms
```

### After index, run 1

```text
Sort (actual time=0.122..0.123 rows=20 loops=1)
  Bitmap Heap Scan on orders (actual time=0.028..0.087 rows=20 loops=1)
    Bitmap Index Scan using p2_filter_idx (actual time=0.016..0.016 rows=20 loops=1)
Planning Time: 0.693 ms
Execution Time: 0.175 ms
```

### After index, run 2

```text
Sort (actual time=0.12..0.121 rows=20 loops=1)
  Bitmap Heap Scan on orders (actual time=0.028..0.085 rows=20 loops=1)
    Bitmap Index Scan using p2_filter_idx (actual time=0.015..0.016 rows=20 loops=1)
Planning Time: 0.542 ms
Execution Time: 0.174 ms
```

### After index, run 3

```text
Sort (actual time=0.119..0.121 rows=20 loops=1)
  Bitmap Heap Scan on orders (actual time=0.028..0.086 rows=20 loops=1)
    Bitmap Index Scan using p2_filter_idx (actual time=0.015..0.015 rows=20 loops=1)
Planning Time: 0.494 ms
Execution Time: 0.195 ms
```

## Reproduce

Use a fresh database with the Portfolio 1 schema and sample data. Run Kolo_Joshua_301905772_P2_Queries.sql, then Kolo_Joshua_301905772_P2_Optimisation.sql. The optimisation script creates a separate performance table and runs EXPLAIN (ANALYZE, BUFFERS).

[Query screenshot](screenshots/Kolo_Joshua_301905772_P2_QueryResults.png) · [Index comparison](screenshots/Kolo_Joshua_301905772_P2_IndexComparison.png)

## References

- [PostgreSQL — EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html)

