/*Number of people who have a gap in observation (two or more observations)*/

SELECT count( person_id ) AS num_persons 
FROM -- more than one observatio period 
( SELECT person_id FROM observation_period GROUP BY person_id HAVING COUNT( person_id ) > 1 );
