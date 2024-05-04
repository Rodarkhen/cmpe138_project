# CMPE 138 PROJECT: Healthcare Transparency

## Queries

### 5) Max and min percentage of how much patient and provider covers
No Optimization:
```
SELECT
  MAX(IF(total_paid != 0.00, paid_by_patient / total_paid, NULL)) AS max_percentage_patient_covers,
  MIN(IF(total_paid != 0.00, paid_by_patient / total_paid, NULL)) AS min_percentage_patient_covers,
  MAX(IF(total_paid != 0.00, paid_by_payer / total_paid, NULL)) AS max_percentage_provider_covers,
  MIN(IF(total_paid != 0.00, paid_by_payer / total_paid, NULL)) AS min_percentage_provider_covers
FROM `bigquery-public-data.cms_synthetic_patient_data_omop.cost`
```

With Optimization:
```
SELECT
  MAX(percent_patient_covers) AS max_percentage_patient_covers,
  MIN(percent_patient_covers) AS min_percentage_patient_covers,
  MAX(percent_provider_covers) AS max_percentage_provider_covers,
  MIN(percent_provider_covers) AS min_percentage_provider_covers
 
FROM (
  SELECT
    paid_by_patient/total_paid AS percent_patient_covers,
    paid_by_payer/total_paid AS percent_provider_covers
  FROM
    `bigquery-public-data.cms_synthetic_patient_data_omop.cost`
  WHERE total_paid != 0.00
)
```
### 6) 2nd most popular chemotherapy drug exposure time and observation time
No Optimization:
```
WITH get_drug_id AS (
    SELECT concept_name AS drug, drug_concept_id as dd
    FROM `bigquery-public-data.cms_synthetic_patient_data_omop.drug_exposure` d
    JOIN `bigquery-public-data.cms_synthetic_patient_data_omop.concept` c
        ON c.concept_id = d.drug_concept_id
    WHERE c.concept_name LIKE '%Sodium Chloride Injectable Solution%'
    LIMIT 1
),
get_person_id AS (
    SELECT
      d.person_id,
      DATE_DIFF(d.drug_exposure_end_date, d.drug_exposure_start_date, day)AS drug_time,
    FROM `bigquery-public-data.cms_synthetic_patient_data_omop.drug_exposure`d
    JOIN get_drug_id g ON d.drug_concept_id = g.dd
),
calc_date_diff AS (
    SELECT
        DATE_DIFF(o.observation_period_end_date, o.observation_period_start_date, day)AS observation_time
    FROM get_person_id as g
    JOIN `bigquery-public-data.cms_synthetic_patient_data_omop.observation_period` o
        ON o.person_id = g.person_id
)
SELECT
    ROUND(AVG(drug_time),2) avg_drug_exposure_time_in_days,
    ROUND(AVG(observation_time),2) avg_observation_time_in_days
FROM get_person_id, calc_date_diff
```

With Optimization:
```
WITH get_drug_id AS (
    SELECT
        concept_name AS drug,
        drug_concept_id as dd
    FROM `bigquery-public-data.cms_synthetic_patient_data_omop.drug_exposure` d
    JOIN `bigquery-public-data.cms_synthetic_patient_data_omop.concept` c
        ON c.concept_id = d.drug_concept_id
    WHERE c.concept_name LIKE '%Sodium Chloride Injectable Solution%'
    LIMIT 1
),

calc_date_diff AS (
    SELECT
    DATE_DIFF(d.drug_exposure_end_date, d.drug_exposure_start_date, day)AS drug_time,
    DATE_DIFF(o.observation_period_end_date, o.observation_period_start_date, day)AS observation_time
    FROM `bigquery-public-data.cms_synthetic_patient_data_omop.drug_exposure`d
    JOIN get_drug_id g
        ON d.drug_concept_id = g.dd
    JOIN `bigquery-public-data.cms_synthetic_patient_data_omop.observation_period` o
        ON o.person_id = d.person_id
)

SELECT
    ROUND(AVG(drug_time),2) avg_drug_exposure_time_in_days,
    ROUND(AVG(observation_time),2) avg_observation_time_in_days
FROM calc_date_diff
```