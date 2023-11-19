PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('user1', 'Derek Peter', 'joeclothes@umich.edu', 'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('user2','Joe Mauer','jclothes@umich.edu','505083b8b56c97429a728b68f31b0b2a089e5113.jpg','sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('user3','Ichiro Suzuki','admin@umich.edu','5ecde7677b83304132cb2871516ea50032ff7a4f.jpg','sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
       ('user4','A Eddy','jmoney@umich.edu','73ab33bd357c3fd42292487b825880958c595655.jpg','sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');


INSERT INTO clothing(filename, owner, article, confidence)
VALUES ('122a7d27ca1d7420a1072f695d9290fad4501a41.png', 'user1', 'blue_shirt', 100),
       ('ad7790405c539894d25ab8dcf0b79eed3341e109.png', 'user1', 'red_pants', 100 ),
       ('9887e06812ef434d291e4936417d125cd594b38a.png', 'user1', 'purple_pants', 79),
       ('2ec7cf8ae158b3b1f40065abfb33e81143707842.png', 'user1', 'grey_shirt', 89),
       ('5ecde7677b83304132cb2871516ea50032ff7a4f.png', 'user1', 'black_dress', 71),
       ('73ab33bd357c3fd42292487b825880958c595655.jpg', 'user1', 'black_shirt', 98),
       ('505083b8b56c97429a728b68f31b0b2a089e5113.jpg', 'user1', 'black_shorts', 98),
       ('e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'user1', 'black_suit', 86),
       ('6w71au3naveutt5qdfgyh4jmhsz3sarf76c5rmym.png', 'user1', 'black_pants', 97),
       ('wsnn7xupgntp5ojs4zihm3js19aajd45d675vhqk.jpg', 'user1', 'red_hoodie', 82),
       ('87u3xo4q6ayewr6gmidzghkivwmf9hy9lhbkwqr9.png', 'user1', 'black_shoes', 95),
       ('nn3lpgstrjrs6bzo1jutoxugf46zmjfrfqxe651k.jpg', 'user1', 'blue_dress', 82);