import string
import uuid
from operator import itemgetter

import psycopg2
from pydantic import BaseModel, ConfigDict


class UserLog(BaseModel):
    user_login: str
    user_password: str


class UserReg(UserLog):
    user_first_name: str
    user_last_name: str
    user_third_name: str | None = None
    user_sex: str | None = None
    user_birthday: str
    user_hobby: str | None = None
    user_city: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserSearch(BaseModel):
    user_first_name: str
    user_last_name: str


class UsersCreds:
    @classmethod
    def user_login(cls, data: UserLog) -> str:
        global connector, engine
        result = None
        user_dict = data.model_dump()
        try:
            connector = psycopg2.connect(dbname='social', user='postgres', password='sinicin123')
            engine = connector.cursor()
            username, password = user_dict['user_login'], user_dict['user_password']
            engine.callproc('check_login', [username, password])
            result = engine.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgresSQL", error)
        finally:
            # closing database connection.
            if connector:
                engine.close()
                connector.close()
                print("PostgresSQL connection is closed")
        result = list(map(itemgetter(0), result))[0]
        return result

    @classmethod
    def user_registration(cls, data: UserReg) -> str:
        global connector, engine
        result, result_reg = None, []
        user_dict = data.model_dump()
        try:
            connector = psycopg2.connect(dbname='social', user='postgres', password='sinicin123')
            engine = connector.cursor()
            first_name, last_name, third_name, sex, datebirth, hobbies, city = user_dict["user_first_name"], user_dict[
                'user_last_name'], user_dict['user_third_name'], user_dict['user_sex'], user_dict['user_birthday'], \
            user_dict['user_hobby'], user_dict['user_city']
            engine.callproc('add_user', [first_name, last_name, third_name, sex, datebirth, hobbies, city])
            result = engine.fetchall()
            result = list(map(itemgetter(0), result))[0]
            result_reg = engine.callproc('add_login', [result, user_dict["user_login"], user_dict["user_password"]])
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgresSQL", error)
        finally:
            # closing database connection.
            if connector:
                engine.close()
                connector.close()
                print("PostgresSQL connection is closed")
        return result_reg[0]

    @classmethod
    def search_user(cls, data: UserSearch) -> list | None:
        global connector, engine
        result = []
        user_dict = data.model_dump()
        try:
            connector = psycopg2.connect(dbname='social', user='postgres', password='sinicin123')
            engine = connector.cursor()
            find_query = """select u.user_id, u.first_name, u.second_name, u.third_name, u.sex, date_birth, c.city_name, hobby from users u join cities c on u.city_id = c.city_id where u.first_name = %s and u.second_name = %s"""
            engine.execute(find_query, [user_dict["user_first_name"], user_dict["user_last_name"]])
            result = engine.fetchall()
            #print(result)
            #result = list(map(itemgetter(0), result))
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgresSQL", error)
        finally:
            # closing database connection.
            if connector:
                engine.close()
                connector.close()
                print("PostgresSQL connection is closed")
        return result
