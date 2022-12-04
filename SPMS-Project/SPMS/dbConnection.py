import mysql.connector

def settingsDB():
    database = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'spms',  
        'USER': 'root',  
        'PASSWORD': 'inja',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
          
    }  
    }
    return database


def queriesDB():
    mydb=mysql.connector.connect(
        host= '127.0.0.1',
        user= 'root',  
        password= 'inja',  
        database= 'spms'  
    )
    return mydb