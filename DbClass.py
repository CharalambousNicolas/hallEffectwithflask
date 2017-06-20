import mysql.connector as connector


class DbClass:
    def __init__(self):
        self.__dsn = {
            "host": "localhost",
            "user": "kmteller",
            "passwd": "123",
            "db": "dbproject"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getUsersFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM users"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getTotalDistanceFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT distance FROM data ORDER BY ID DESC limit 1"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getSpeedFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT speed  FROM data ORDER BY ID DESC"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def saveSensorValuesToDatabase(self, distance, speed, dateday):
        # Query met parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO data (distance,speed,dateday) VALUES ('{param1}','{param2}','{param3}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=distance, param2=speed, param3=dateday)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def getData(self):
        query = "SELECT ID, distance, speed FROM data"

        # query uitvoeren
        self.__cursor.execute(query)

        # resultaat opvragen
        result = self.__cursor.fetchall()

        # cursor sluiten
        self.__cursor.close()

        return result

    def saveContactToDatabase(self, userID, subject, message):
        # Query met parameters
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        sqlQuery = "INSERT INTO contact (userID,subject,message) VALUES ('{param1}','{param2}','{param3}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=userID, param2=subject, param3=message)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()
