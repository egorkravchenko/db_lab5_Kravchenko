import csv
from main import PostgresDB

database = PostgresDB()
database.connect()

table_names = ["show", "genre", "actor", "show_genre", "show_actor"]

for table_name in table_names:
    file_path = f"csv_files/export/{table_name}.csv"
    database.execute(f"SELECT * FROM {table_name}")
    rows = database.fetch_all()

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow([desc[0] for desc in database.cursor.description])
        # Write data
        writer.writerows(rows)

database.close_connection()
