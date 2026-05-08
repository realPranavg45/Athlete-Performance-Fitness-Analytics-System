-- View Complete Dataset
SELECT * FROM athlete_data;

-- Total Number of Records
SELECT COUNT(*) FROM athlete_data;

-- Unique Workout Types
SELECT DISTINCT workout_type
FROM athlete_data;

-- Average Calories Burned
SELECT AVG(calories_burned)
FROM athlete_data;

-- Maximum Calories Burned
SELECT MAX(calories_burned)
FROM athlete_data;

-- Minimum Calories Burned
SELECT MIN(calories_burned)
FROM athlete_data;

-- Average BMI
SELECT ROUND(AVG(bmi),2)
FROM athlete_data;

-- Count Athletes by Gender
SELECT gender,
COUNT(*) AS total_athletes
FROM athlete_data
GROUP BY gender;

-- Average Calories Burned by Workout Type
SELECT workout_type,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data
GROUP BY workout_type
ORDER BY avg_calories DESC;

-- Workout Frequency Analysis
SELECT workout_frequency,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data
GROUP BY workout_frequency
ORDER BY workout_frequency;

-- Average BPM by Gender
SELECT gender,
ROUND(AVG(avg_bpm),2) AS avg_heart_rate
FROM athlete_data
GROUP BY gender;

-- Highest Calorie Burning Athletes
SELECT age,
gender,
workout_type,
calories_burned
FROM athlete_data
ORDER BY calories_burned DESC
LIMIT 10;

-- BMI Category Analysis
SELECT bmi_category,
COUNT(*) AS total_people
FROM athlete_data
GROUP BY bmi_category;

-- Average Session Duration by Workout Type
SELECT workout_type,
ROUND(AVG(session_duration_hours),2) AS avg_duration
FROM athlete_data
GROUP BY workout_type
ORDER BY avg_duration DESC;

-- Water Intake vs Calories Burned
SELECT ROUND(AVG(water_intake_liters),2) AS avg_water,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data;

-- Workout Type Distribution
SELECT workout_type,
COUNT(*) AS total_members
FROM athlete_data
GROUP BY workout_type
ORDER BY total_members DESC;

-- Experience Level Analysis
SELECT experience_level,
ROUND(AVG(calories_burned),2) AS avg_calories,
ROUND(AVG(avg_bpm),2) AS avg_bpm
FROM athlete_data
GROUP BY experience_level
ORDER BY experience_level;

-- Top Performing Workout Types
SELECT workout_type,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data
GROUP BY workout_type
HAVING AVG(calories_burned) > 800
ORDER BY avg_calories DESC;

-- Athlete Segmentation
SELECT
CASE
WHEN calories_burned < 500 THEN 'Low Performance'
WHEN calories_burned BETWEEN 500 AND 900 THEN 'Moderate Performance'
ELSE 'High Performance'
END AS performance_group,
COUNT(*) AS total_athletes
FROM athlete_data
GROUP BY performance_group;

-- Athlete Ranking Using Window Function
SELECT age,
gender,
workout_type,
calories_burned,
RANK() OVER(ORDER BY calories_burned DESC) AS athlete_rank
FROM athlete_data;

-- Workout Type with Highest Average BPM
SELECT workout_type,
ROUND(AVG(avg_bpm),2) AS avg_bpm
FROM athlete_data
GROUP BY workout_type
ORDER BY avg_bpm DESC;

-- High Intensity Athletes
SELECT *
FROM athlete_data
WHERE avg_bpm > 160
AND calories_burned > 900;

-- Advanced KPI Analysis
SELECT
workout_type,
COUNT(*) AS total_athletes,
ROUND(AVG(calories_burned),2) AS avg_calories,
ROUND(AVG(session_duration_hours),2) AS avg_duration,
ROUND(AVG(avg_bpm),2) AS avg_bpm
FROM athlete_data
GROUP BY workout_type
ORDER BY avg_calories DESC;

-- Athletes Burning Above Average Calories
SELECT *
FROM athlete_data
WHERE calories_burned >
(
SELECT AVG(calories_burned)
FROM athlete_data
);

-- CTE Workout Analysis
WITH calorie_stats AS
(
SELECT workout_type,
AVG(calories_burned) AS avg_calories
FROM athlete_data
GROUP BY workout_type
)

SELECT *
FROM calorie_stats
WHERE avg_calories > 700;

-- Experience Level vs Workout Frequency
SELECT
experience_level,
ROUND(AVG(workout_frequency),2) AS avg_frequency,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data
GROUP BY experience_level
ORDER BY experience_level;

-- Workout Efficiency Analysis
SELECT
workout_type,
ROUND(AVG(calories_burned/session_duration_hours),2) AS calories_per_hour
FROM athlete_data
GROUP BY workout_type
ORDER BY calories_per_hour DESC;

-- Top 5 Efficient Athletes
SELECT age,
gender,
workout_type,
calories_burned,
session_duration_hours,
ROUND(calories_burned/session_duration_hours,2) AS efficiency_score
FROM athlete_data
ORDER BY efficiency_score DESC
LIMIT 5;

-- Workout Trend Analysis
SELECT workout_frequency,
ROUND(AVG(session_duration_hours),2) AS avg_duration,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data
GROUP BY workout_frequency
ORDER BY workout_frequency;

-- Gender and Workout Type Analysis
SELECT
gender,
workout_type,
ROUND(AVG(calories_burned),2) AS avg_calories
FROM athlete_data
GROUP BY gender, workout_type
ORDER BY avg_calories DESC;
