import sqlite3
import pandas as pd

if __name__ == "__main__":

    select_sql = "SELECT * FROM '091120'"
    select_sql_a = "SELECT * FROM a091120"
    
    con = sqlite3.connect("c:/db/kosdap.db")
    
    df = pd.read_sql(select_sql, con)
    
    df.to_csv('091120.csv')
    #df.to_csv('091120')