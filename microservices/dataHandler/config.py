from os import environ


class Config:

    # Configuration variables for database ; Will include them as environment variables
    # sql_hostname = 'mysqldb'
    # sql_user = 'root'
    # sql_port = 3306
    # sql_password = 'password'
    # db_name = 'watchdog'

    # """Set configration vars"""
    # environ['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{sql_user}:{sql_password}@{sql_hostname}:{sql_port}/{db_name}'
    # environ['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
    
    # Variables for database setup
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')