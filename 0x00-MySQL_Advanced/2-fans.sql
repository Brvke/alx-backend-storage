-- a script to count the number of fans of each country
SELECT origin, SUM(fans) AS nb_fans 
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

