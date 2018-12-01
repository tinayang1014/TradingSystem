
use TradingSys;


-- create table symbol
-- 	(currency_id int NOT NULL,
--     symbol varchar(10),
--     primary key(currency_id)
-- );

-- insert into symbol
-- value (1, 'BTC-USD');

-- insert into symbol
-- value (2, 'LTC-USD');

-- insert into symbol
-- value (3, 'ETH-USD');


-- create table price
-- 	(price_id int NOT NULL AUTO_INCREMENT,
--     currency_id int,
--     time_stamp TIMESTAMP,
--     open float,
--     price float,
--     best_bid float,
--     best_ask float,
--     PRIMARY KEY(price_id)
-- );


-- create table user
-- 	(user_id int NOT NULL auto_increment,
--     login varchar(20) NOT NULL,
--     password varchar(20) NOT NULL,
--     primary key(user_id)
-- );

-- insert into user(login, password)
-- values ('guest', 'abc');

-- create table transaction
-- 	(transaction_id int NOT NULL auto_increment,
--     currency_id int,
--     user_id int,
--     type varchar(5) NOT NULL check(type IN ('Buy', 'Sell')),
--     quant int,
--     price float,
-- 	timestamp timestamp,
--     PRIMARY KEY(transaction_id)
-- );


-- create table protfolio
-- 	(portfolio_id int NOT NULL auto_increment,
--     user_id int,
--     currency_id int,
--     quant int,
--     primary key(portfolio_id)
-- );


# update real time currency price
-- select price
-- from price
-- where currency_id = 1 and time_stamp = (
-- select max(time_stamp)
-- from price
-- where currency_id = 1);

# check userName already in DB
select *
from transaction;

