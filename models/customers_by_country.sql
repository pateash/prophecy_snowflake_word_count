{{
  config({    
    "materialized": "table"
  })
}}

WITH CUSTOMER_DATA AS (

  SELECT * 
  
  FROM {{ source('ASHISH.PUBLIC', 'CUSTOMER_DATA') }}

),

SQLStatement_1 AS (

  SELECT 
    country,
    count(*) AS customers
  
  FROM CUSTOMER_DATA
  
  GROUP BY country

)

SELECT *

FROM SQLStatement_1
