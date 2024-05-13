{{
  config({    
    "materialized": "table"
  })
}}

WITH CUSTOMER_DATA AS (

  SELECT * 
  
  FROM {{ source('QA_DATABASE.QA_SCHEMA', 'CUSTOMER_DATA') }}

),

groupByCountry AS (

  SELECT 
    any_value(COUNTRY) AS COUNTRY,
    count(ID) AS customers
  
  FROM CUSTOMER_DATA AS in0
  
  GROUP BY COUNTRY

),

OrderByCustomers AS (

  SELECT * 
  
  FROM groupByCountry AS in0
  
  ORDER BY CUSTOMERS DESC NULLS LAST

)

SELECT *

FROM OrderByCustomers
