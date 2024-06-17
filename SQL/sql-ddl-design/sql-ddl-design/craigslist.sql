-- Create Regions Table
CREATE TABLE Regions (
    region_id SERIAL PRIMARY KEY,
    region_name TEXT NOT NULL
);

-- Create Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    preferred_region_id INTEGER REFERENCES Regions (region_id)
);

-- Create Posts Table
CREATE TABLE Posts (
    post_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    user_id INTEGER REFERENCES Users (user_id),
    location TEXT NOT NULL,
    region_id INTEGER REFERENCES Regions (region_id)
);

-- Create Categories Table
CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL
);

-- Create PostCategories Table
CREATE TABLE PostCategories (
    post_category_id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES Posts (post_id),
    category_id INTEGER REFERENCES Categories (category_id)
);
