-- Create Teams Table
CREATE TABLE Teams (
    team_id SERIAL PRIMARY KEY,
    team_name TEXT NOT NULL
);

-- Create Players Table
CREATE TABLE Players (
    player_id SERIAL PRIMARY KEY,
    player_name TEXT NOT NULL,
    team_id INTEGER REFERENCES Teams (team_id)
);

-- Create Referees Table
CREATE TABLE Referees (
    referee_id SERIAL PRIMARY KEY,
    referee_name TEXT NOT NULL
);

-- Create Seasons Table
CREATE TABLE Seasons (
    season_id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

-- Create Matches Table
CREATE TABLE Matches (
    match_id SERIAL PRIMARY KEY,
    home_team_id INTEGER REFERENCES Teams (team_id),
    away_team_id INTEGER REFERENCES Teams (team_id),
    match_date DATE NOT NULL,
    season_id INTEGER REFERENCES Seasons (season_id)
);

-- Create Goals Table
CREATE TABLE Goals (
    goal_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES Matches (match_id),
    player_id INTEGER REFERENCES Players (player_id),
    goal_time TIME NOT NULL
);

-- Create MatchReferees Table
CREATE TABLE MatchReferees (
    match_referee_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES Matches (match_id),
    referee_id INTEGER REFERENCES Referees (referee_id)
);

-- Create Standings View
CREATE VIEW Standings AS
SELECT 
    Teams.team_id, 
    Teams.team_name,
    COUNT(CASE WHEN Matches.home_team_id = Teams.team_id AND Matches.home_team_score > Matches.away_team_score THEN 1 END) +
    COUNT(CASE WHEN Matches.away_team_id = Teams.team_id AND Matches.away_team_score > Matches.home_team_score THEN 1 END) AS wins,
    COUNT(CASE WHEN Matches.home_team_id = Teams.team_id AND Matches.home_team_score = Matches.away_team_score THEN 1 END) +
    COUNT(CASE WHEN Matches.away_team_id = Teams.team_id AND Matches.away_team_score = Matches.home_team_score THEN 1 END) AS draws,
    COUNT(CASE WHEN Matches.home_team_id = Teams.team_id AND Matches.home_team_score < Matches.away_team_score THEN 1 END) +
    COUNT(CASE WHEN Matches.away_team_id = Teams.team_id AND Matches.away_team_score < Matches.home_team_score THEN 1 END) AS losses
FROM 
    Teams
LEFT JOIN Matches ON Matches.home_team_id = Teams.team_id OR Matches.away_team_id = Teams.team_id
GROUP BY 
    Teams.team_id, Teams.team_name
ORDER BY 
    wins DESC, draws DESC, losses ASC;