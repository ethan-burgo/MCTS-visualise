import psycopg2
from psycopg2 import sql
import time
from helpers import format_update_statement, format_id

# Replace these variables with your PostgreSQL connection details
class Postgres:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="MCTS_visualise", user="postgres", password="bindi2012", host="localhost", port="5432"
        )
        self.cursor = self.connection.cursor()
        self.table_def = {  
            "Execution": "exe_id, title, starttime, endtime, resultdes",
            "State_tb": "current_state, node_id_s",
            "Node": "node_id, parent_id, execution_id, chosen, move_, childern, value_, visits"
        }

    def insert_into_table(self, table, values):
        for k,v in self.table_def.items():
            if table == k:
                insert_query = sql.SQL(f"""
                    INSERT INTO "MCTS_visualise"."{table}" ({v}) 
                    VALUES {values}""")
                self.cursor.execute(insert_query)
                self.connection.commit()
                return f"{values} inserted successfully into {table}"
    
    def close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            pass
    
    def check_if_record_exists(self, table, id_name, id):
        try:
            self.cursor.execute(f'SELECT count(*) FROM "MCTS_visualise"."{table}" WHERE {id_name}={format_id(id)}')
            rows = self.cursor.fetchall()
            for row in rows:
                if int(row[0]) > 0:
                    return True
            return False

        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)
    

    def update_record(self, table, record_id, values, id_name):
        update_string = format_update_statement(values)
        update_query = sql.SQL(f"""
            UPDATE "MCTS_visualise"."{table}"
            SET {update_string}
            WHERE {id_name} = {format_id(record_id)}
        """)
        try:
            self.cursor.execute(update_query, [*values.values(), format_id(record_id)])
            self.connection.commit()
            return f"Record with ID {record_id} updated successfully in {table}"
        except Exception as e:
            return f"Error updating record: {e}"

    def initalise_exe(self):
        pass