/** Number of people continuously observed throughout a year **/

SELECT COUNT(
DISTINCT person_ID) AS NUM_persons 
FROM observation_period 
WHERE observation_period_start_date <= '01-jan-2011' AND observation_period_end_date >= '31-dec-2011';
