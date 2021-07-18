DROP TABLE IF EXISTS products;

CREATE TABLE products
(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);

INSERT INTO products (name, price, description)
VALUES
    ('Assassins Creed Odyssey', 59.99, 'Choose your fate in Assassins Creed Odyssey. From outcast to living legend, embark on an odyssey to uncover the secrets of your past and change the fate of Ancient Greece.'),
    ('Dead by Daylight', 19.99, 'Dead by Daylight is a multiplayer (4vs1) horror game where one player takes on the role of the savage Killer, and the other four players play as Survivors, trying to escape the Killer and avoid being caught and killed.'),
    ('Doom Eternal', 59.99, 'Become the Slayer in an epic single-player campaign to conquer demons across dimensions and stop the final destruction of humanity.'),
    ('No Mans Sky', 54.99, 'No Mans Sky is a game about exploration and survival in an infinite procedurally generated universe.'),
    ('Sekiro: Shadows Die Twice', 59.99, 'Sekiro: Shadows Die Twice is an action-adventure video game set in late 1500s Sengoku Japan'),
    ('Fallout 4', 29.99, 'As the sole survivor of Vault 111, you enter a world destroyed by nuclear war. Every second is a fight for survival, and every choice is yours. Only you can rebuild and determine the fate of the Wasteland.'),
    ('Cyberpunk 2077', 47.99, 'Cyberpunk 2077 is an open-world, action-adventure story set in Night City, a megalopolis obsessed with power, glamour and body modification. You play as V, a mercenary outlaw going after a one-of-a-kind implant that is the key to immortality.'),
    ('7 Days To Die', 22.99, '7 Days to Die is an open-world game that is a unique combination of first person shooter, survival horror, tower defense, and RPG games.'),
    ('The Forest', 16.99, 'As the lone survivor of a passenger jet crash, you find yourself in a mysterious forest battling to stay alive against a society of cannibalistic mutants. Build, explore, survive in this terrifying first person survival horror simulator.'),
    ('Rust', 29.99, 'The only aim in Rust is to survive - Overcome struggles such as hunger, thirst and cold. Build a fire. Build a shelter. Kill animals. Protect yourself from other players.'),
    ('The Witcher 3', 29.99, 'The Witcher: Wild Hunt is a story-driven open world RPG set in a visually stunning fantasy universe full of meaningful choices and impactful consequences. '),
    ('Rainbow Six Siege', 19.99, 'Tom Clancys Rainbow Six Siege is an online tactical shooter video game developed by the renowned Ubisoft Montreal studio.');
    
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    username TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS details;
 
CREATE TABLE details
(
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    username TEXT PRIMARY KEY,
    address TEXT NOT NULL,
    address2 TEXT,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    postcode TEXT NOT NULL
);

DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

