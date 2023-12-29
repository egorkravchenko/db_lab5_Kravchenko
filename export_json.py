import json
from main import PostgresDB

database = PostgresDB()
database.connect()

table_names = ["show", "genre", "actor", "show_actor", "show_genre"]

output_path = "exported_data.json"

data = {}

for table_name in table_names:
    query = f"SELECT * FROM {table_name}"
    database.execute(query)
    rows = []
    fields = [x[0] for x in database.cursor.description]

    for row in database.cursor:
        rows.append(dict(zip(fields, row)))

    data[table_name] = rows

with open(output_path, 'w') as json_file:
    json.dump(data, json_file, default=str)

database.close_connection()
