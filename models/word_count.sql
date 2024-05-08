{{
  config({    
    "materialized": "table"
  })
}}

WITH README AS (

  SELECT * 
  
  FROM {{ source('ASHISH.PUBLIC', 'README') }}

),

tokenize AS (

  SELECT 
    LINE AS LINE,
    CASE
      WHEN LINE IS NOT NULL
        THEN SPLIT(REGEXP_REPLACE(line, '\\s+', ' '), ' ')
      ELSE ARRAY_CONSTRUCT()
    END AS words
  
  FROM README AS in0

),

add_word_count AS (

  SELECT 
    LINE AS LINE,
    WORDS AS WORDS,
    ARRAY_SIZE(WORDS) AS words_count
  
  FROM tokenize AS in0

)

SELECT *

FROM add_word_count
