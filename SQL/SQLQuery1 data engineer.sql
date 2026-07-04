

USE RetailDw;
GO

CREATE TABLE dim_Customer
(
	Customer_key      INT IDENTITY(1,1) PRIMARY KEY ,
	Customer_ID       VARCHAR(50),
	Customer_city     VARCHAR(50),
	Customer_State    VARCHAR(50)
);

CREATE TABLE dim_product
(
	product_key       INT IDENTITY (1,1) PRIMARY KEY,
	product_id        VARCHAR (100),
	product_category  VARCHAR (100)
	);

	CREATE TABLE dim_date
	(
		date_key      INT PRIMARY KEY,
		full_date     DATE,
		year          INT,
		month         INT,
		day           INT,
		quater        INT
	);

	CREATE TABLE fact_sales
	(
		sales_key         INT IDENTITY (1,1) PRIMARY KEY,
		order_id          VARCHAR (50),
		customer_key      INT,
		product_key       INT,
		date_key          INT,
		payment_value       DECIMAL (10,2),
		quantity           INT

	);
	go


	SELECT COUNT(*) AS Totalcustomers
	FROM dbo.dim_customer

	SELECT COUNT(*) AS Totalcustomers
	FROM dbo.dim_product


	SELECT COUNT(*)
	FROM dbo.dim_date
;

	SELECT COUNT (*) AS TotalSales
	FROM dbo.fact_sales;

	SELECT 
		SUM(payment_value) AS TotalSalesValue
		FROM dbo.fact_sales;

		SELECT 
			COUNT(*) AS TotalOrders
		FROM dbo.fact_sales;

		SELECT
		
			d.year,
			SUM(f.payment_value) AS Revenue
			FROM dbo.fact_sales f
			JOIN dbo.dim_date d ON f.date_key = d.date_key
			GROUP BY d.year
			order BY d.year;

 SELECT TOP 10
    p.product_category,
    SUM(f.payment_value) AS Revenue
FROM dbo.fact_sales f
JOIN dbo.dim_product p
ON f.product_key = p.product_key
GROUP BY p.product_category
ORDER BY Revenue DESC;

SELECT TOP 10
    c.customer_city,
    SUM(f.payment_value) AS Revenue
FROM dbo.fact_sales f
JOIN dbo.dim_customer c
ON f.customer_key = c.customer_key
GROUP BY c.customer_city
ORDER BY Revenue DESC

____view one

CREATE VIEW vw_revenue_by_year AS

SELECT
    d.year,
    SUM(f.payment_value) AS Revenue
FROM dbo.fact_sales f
JOIN dbo.dim_date d
ON f.date_key = d.date_key
GROUP BY d.year;



CREATE VIEW vw_revenue_by_category AS

SELECT
    p.product_category,
    SUM(f.payment_value) AS Revenue
FROM dbo.fact_sales f
JOIN dbo.dim_product p
ON f.product_key = p.product_key
GROUP BY p.product_category;



CREATE VIEW vw_revenue_by_city AS

SELECT
    c.customer_city,
    SUM(f.payment_value) AS Revenue
FROM dbo.fact_sales f
JOIN dbo.dim_customer c
ON f.customer_key = c.customer_key
GROUP BY c.customer_city;

SELECT COUNT(*) AS FactRows
FROM dbo.fact_sales;

SELECT COUNT(DISTINCT order_id) AS DistinctOrders
FROM dbo.fact_sales;


SELECT TOP 10 *
FROM dbo.fact_sales;


SELECT Customer_ID,
       COUNT(*) AS cnt
FROM dbo.dim_Customer
GROUP BY Customer_ID
HAVING COUNT(*) > 1;

SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT Customer_ID) AS DistinctCustomers
FROM dbo.dim_Customer;



 SELECT
    COUNT(*) AS NullCustomerKeys
FROM dbo.fact_sales
WHERE customer_key IS NULL;

 SELECT
    COUNT(*) AS NullProductKeys
FROM dbo.fact_sales
WHERE product_key IS NULL;

 SELECT
    COUNT(*) AS NullDateKeys
FROM dbo.fact_sales
WHERE date_key IS NULL;
