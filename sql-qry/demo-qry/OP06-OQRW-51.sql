/* Count average number of observation days. */

SELECT avg( observation_period_end_date - observation_period_start_date ) AS num_days 
FROM observation_period;
