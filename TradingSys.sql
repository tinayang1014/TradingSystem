-- create database TradingSys;
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
--     price float,
--     PRIMARY KEY(price_id)
-- );


-- create table user
-- 	(user_id int NOT NULL auto_increment,
--     login varchar(20) NOT NULL,
--     password varchar(20) NOT NULL,
--     cash_balance float,
--     primary key(user_id)
-- );

-- insert into user(login, password, cash_balance)
-- values ('guest', 'abc', 100000);


-- create table transaction
-- 	(transaction_id int NOT NULL auto_increment,
--     currency_id int,
--     user_id int,
--     type varchar(5) NOT NULL check(type IN ('Buy', 'Sell')),
--     quant int,
--     price float,
-- 	timestamp timestamp,
--     trans_rpl float,
--     PRIMARY KEY(transaction_id)
-- );


-- create table portfolio
-- 	(portfolio_id int NOT NULL auto_increment,
--     user_id int,
--     currency_id int,
--     quant int,
--     vwap float,
--     rpl float,
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
-- select *
-- from transaction;

-- TRUNCATE TABLE price;


-- select price 
-- from price 
-- where currency_id = 1 and time_stamp = 
-- (select max(time_stamp) from price where currency_id = 1 and time_stamp< '2018-12-03 12:00:00');

-- select * from price where currency_id=3;

-- select quant from portfolio where user_id = 2 and currency_id = 1;
-- insert into portfolio (user_id, currency_id, quant) values (2, 1, 100);

-- UPDATE user
-- SET cash_balance = 90000
-- WHERE user_id = 2;

-- select * from portfolio where user_id = 2;

-- select price 
-- from price 
-- where currency_id = 1 and time_stamp = 
-- (select max(time_stamp) from price where currency_id = 1 and time_stamp> '2018-12-03 16:36:54');

select * from transaction;
-- select * from portfolio;
-- select * from user;