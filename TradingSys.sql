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


-- TRUNCATE TABLE price;

# Get the currency quanty with specfic user
-- select quant from portfolio where user_id = 2 and currency_id = 1;

# Update user cash balance when make transaction
-- UPDATE user
-- SET cash_balance = 90000
-- WHERE user_id = 2;

# Get latest price in trading
-- select price 
-- from price 
-- where currency_id = 1 and time_stamp = 
-- (select max(time_stamp) from price where currency_id = 1 and time_stamp> '2018-12-03 16:36:54');

# Display on web
-- select s.symbol, t.type, t.quant, t.price, t.timestamp, t.trans_rpl from transaction as t join symbol as s on t.currency_id = s.currency_id where t.user_id = 2;

-- select s.symbol, p.quant, p.vwap, p.rpl from portfolio as p join symbol as s on p.currency_id = s.currency_id where p.user_id = 2;




