/*Number of people who have at least one observation period that is longer than 365 days*/

SELECT COUNT(DISTINCT person_ID) AS NUM_personS 
FROM observation_period 
WHERE observation_period_END_DATE - observation_period_START_DATE >= 365;
