APIUSER_DDL = ''' CREATE TABLE IF NOT EXISTS apiuser (
       id serial,
       name varchar(100) NOT NULL,
       login varchar(20) UNIQUE NOT NULL,
       password varchar(20) NOT NULL,
       email varchar(30) NOT NULL,
       PRIMARY KEY (id)
     ) ;'''
