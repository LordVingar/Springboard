-- from the terminal run:
-- psql < outer_space.sql

DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

-- Galaxies Table
CREATE TABLE galaxies (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Stars Table
CREATE TABLE stars (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  galaxy_id INTEGER REFERENCES galaxies(id)
);

-- Planets Table
CREATE TABLE planets (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  star_id INTEGER REFERENCES stars(id)
);

-- Moons Table
CREATE TABLE moons (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  planet_id INTEGER REFERENCES planets(id)
);

-- Insert Data
-- Galaxies
INSERT INTO galaxies (name) VALUES
  ('Milky Way'),
  ('Andromeda'),  -- added another galaxy for variety
  ('Whirlpool Galaxy');  -- added another galaxy for variety

-- Stars
INSERT INTO stars (name, galaxy_id) VALUES
  ('The Sun', 1),  -- Milky Way
  ('Proxima Centauri', 1),  -- Milky Way
  ('Gliese 876', 1);  -- Milky Way

-- Planets
INSERT INTO planets (name, orbital_period_in_years, star_id) VALUES
  ('Earth', 1.00, 1),  -- The Sun
  ('Mars', 1.88, 1),  -- The Sun
  ('Venus', 0.62, 1),  -- The Sun
  ('Neptune', 164.8, 1),  -- The Sun
  ('Proxima Centauri b', 0.03, 2),  -- Proxima Centauri
  ('Gliese 876 b', 0.23, 3);  -- Gliese 876

-- Moons
INSERT INTO moons (name, planet_id) VALUES
  ('The Moon', 1),  -- Earth
  ('Phobos', 2),  -- Mars
  ('Deimos', 2),  -- Mars
  ('Naiad', 4),  -- Neptune
  ('Thalassa', 4),  -- Neptune
  ('Despina', 4),  -- Neptune
  ('Galatea', 4),  -- Neptune
  ('Larissa', 4),  -- Neptune
  ('S/2004 N 1', 4),  -- Neptune
  ('Proteus', 4),  -- Neptune
  ('Triton', 4),  -- Neptune
  ('Nereid', 4),  -- Neptune
  ('Halimede', 4),  -- Neptune
  ('Sao', 4),  -- Neptune
  ('Laomedeia', 4),  -- Neptune
  ('Psamathe', 4),  -- Neptune
  ('Neso', 4);  -- Neptune