PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('user1', 'Derek Peter', 'joeclothes@umich.edu', 'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('user2','Joe Mauer','jclothes@umich.edu','505083b8b56c97429a728b68f31b0b2a089e5113.jpg','sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('user3','Ichiro Suzuki','admin@umich.edu','5ecde7677b83304132cb2871516ea50032ff7a4f.jpg','sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('user4','A Eddy','jmoney@umich.edu','73ab33bd357c3fd42292487b825880958c595655.jpg','sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');


INSERT INTO clothing(filename, owner, article, confidence)
VALUES ('122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'user1', 'blue_shirt', 100),
       ('ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'user1', 'red_pants', 100 ),
       ('9887e06812ef434d291e4936417d125cd594b38a.jpg', 'user1', 'purple_pants', 30),
       ('2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'user1', 'grey_shirt', 4),
       ('5ecde7677b83304132cb2871516ea50032ff7a4f.jpg', 'user1', 'grey_shirt', 4),
       ('73ab33bd357c3fd42292487b825880958c595655.jpg', 'user1', 'blue_shirt', 4),
       ('505083b8b56c97429a728b68f31b0b2a089e5113.jpg', 'user1', 'blue_shirt', 4),
       ('e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'user1', 'grey_shirt', 4);