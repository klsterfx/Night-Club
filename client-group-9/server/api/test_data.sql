-- password = sha512('swen610')

INSERT INTO clubs(name,capacity,city) 
VALUES ('club-a',100,'Rochester');

INSERT INTO clubs(name,capacity,city) 
VALUES ('club-b',150,'Rochester');

INSERT INTO users(name,age,city, password) 
VALUES ('customer-a',20,'Rochester', '1ccb862acabbccce24a5bc6cb80a986d936425861d16af97455cb26679164f91846ae760fb82b7bf455289644f497b65a2fe966e9bc5742f97cf7fe6fc879692');

INSERT INTO users(name,age,city,password) 
VALUES ('customer-b',21,'Rochester', '1ccb862acabbccce24a5bc6cb80a986d936425861d16af97455cb26679164f91846ae760fb82b7bf455289644f497b65a2fe966e9bc5742f97cf7fe6fc879692');

INSERT INTO users(name,age,city, password) 
VALUES ('customer-c',22,'Rochester', '1ccb862acabbccce24a5bc6cb80a986d936425861d16af97455cb26679164f91846ae760fb82b7bf455289644f497b65a2fe966e9bc5742f97cf7fe6fc879692');