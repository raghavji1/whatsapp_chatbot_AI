import mysql.connector
from datetime import datetime, date
import time

# Convert current date to timestamp
date_str = str(date.today())
print(date_str)
date_obj = datetime.strptime(date_str, '%Y-%m-%d')
timestamp = int(time.mktime(date_obj.timetuple()))

# Establish the connection
conn = mysql.connector.connect(
    host="LocalHost",
    user="root",
    password="",
    database="rgv"
)

# Function to run the query
def run_query(conn):
    try:
        # Use a context manager to ensure cursor is closed
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT
                    CONCAT('https://www.balticshipping.com/job/', vacancies.id) AS job_url,
                    vacancies.id,
                    d_positions.name AS position_name,
                    vacancies.date_of_join,
                    vacancies.contract_duration,
                    vacancies.salary,
                    vacancies.engine_power,
                    vacancies.trading_area_id,
                    vacancies.cargoes,
                    vacancies_notes.note,
                    d_vessel_types.vessel_type,
                    d_countries.country
                FROM
                    vacancies
                INNER JOIN
                    vacancies_notes ON vacancies_notes.vacancie_id = vacancies.id
                INNER JOIN
                    d_vessel_types ON d_vessel_types.id = vacancies.vessel_type
                INNER JOIN
                    d_countries ON d_countries.id = vacancies.ship_flag
                INNER JOIN
                    d_positions ON vacancies.positions_id = d_positions.id
                WHERE
                    vacancies.date_of_join >= {timestamp}
                ORDER BY
                    vacancies.date_of_join;
            """)
            results = cursor.fetchall()
            file_name = "data.txt"

            # Open the file in write mode with utf-8 encoding
            with open(file_name, "w", encoding="utf-8") as file:
                # Write the content of the results to the file
                for row in results:
                    file.write(str(row) + "\n")
           
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

# Run the query
run_query(conn)
