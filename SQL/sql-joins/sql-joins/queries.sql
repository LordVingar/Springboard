-- write your queries here

-- Task 1: Join owners and vehicles tables, showing all columns and records regardless of owner_id
SELECT 
    owners.id AS owner_id, 
    owners.first_name, 
    owners.last_name, 
    vehicles.id AS vehicle_id, 
    vehicles.make, 
    vehicles.model, 
    vehicles.year, 
    vehicles.price, 
    vehicles.owner_id
FROM 
    owners
LEFT JOIN 
    vehicles
ON 
    owners.id = vehicles.owner_id;

-- Task 2: Count the number of vehicles for each owner, ordered by first_name in ascending order
SELECT 
    owners.first_name, 
    owners.last_name, 
    COUNT(vehicles.id) AS vehicle_count
FROM 
    owners
LEFT JOIN 
    vehicles
ON 
    owners.id = vehicles.owner_id
GROUP BY 
    owners.first_name, 
    owners.last_name
ORDER BY 
    owners.first_name ASC;

-- Task 3: Count vehicles and display average price for owners with more than one vehicle and an average price greater than 10000, ordered by first_name in descending order
SELECT 
    owners.first_name, 
    owners.last_name, 
    COUNT(vehicles.id) AS vehicle_count, 
    AVG(vehicles.price)::INTEGER AS average_price
FROM 
    owners
LEFT JOIN 
    vehicles
ON 
    owners.id = vehicles.owner_id
GROUP BY 
    owners.first_name, 
    owners.last_name
HAVING 
    COUNT(vehicles.id) > 1 
    AND AVG(vehicles.price) > 10000
ORDER BY 
    owners.first_name DESC;
