/** Average length of observation, in month **/

SELECT avg(
datediff(month, observation_period_start_date , observation_period_end_date ) ) AS num_months 
FROM observation_period;
