import psycopg2
from matplotlib import pyplot as plt

views = {
    "shows_rating": """
            CREATE VIEW shows_rating AS SELECT 
                title, 
                rating
            FROM show
            ORDER BY rating DESC
            LIMIT 5;
        """,

    "show_count_for_genres": """
            CREATE VIEW show_count_for_genres AS SELECT 
                genre_name, 
                COUNT(*) as count
            FROM genre g
            JOIN show_genre sg ON g.genre_id = sg.genre_id
            GROUP BY genre_name;
        """,

    "actor_count_for_show": """
            CREATE VIEW actor_count_for_show AS SELECT
                s.title, 
                COUNT(sa.actor_id) as actor_count
            FROM show s
                LEFT JOIN show_actor sa ON s.show_id = sa.show_id
            GROUP BY s.title;
        """
}


class PostgresDB:
    def __init__(self):
        self.dbname = "db_lab3_Kravchenko"  
        self.user = "postgres"  
        self.password = "13032002"  
        self.host = "localhost"
        self.port = 5432
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(f"Error executing query: {e}")

    def fetch_all(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()


class StatisticsRepository:
    def __init__(self):
        self.database = PostgresDB()

    def get_shows_rating(self):
        view_name = "shows_rating"
        return self.__execute_view(view_name)

    def get_show_count_for_genres(self):
        view_name = "show_count_for_genres"
        return self.__execute_view(view_name)

    def get_actor_count_for_show(self):
        view_name = "actor_count_for_show"
        return self.__execute_view(view_name)

    def __execute_view(self, view_name):
        self.database.connect()
        self.__create_view(view_name)
        result = self.__read_view(view_name)
        self.database.close_connection()

        return result

    def __create_view(self, view_name):
        create_view_sql = views[view_name]
        self.database.execute(create_view_sql)

    def __read_view(self, view_name):
        select_sql = 'SELECT * FROM ' + view_name
        self.database.execute(select_sql)

        return self.database.fetch_all()


class StatisticsVisualizer:
    def __init__(self):
        self.statistics_provider = StatisticsRepository()

    def showHistogram(self):
        shows_rating = self.statistics_provider.get_shows_rating()
        title, rating = zip(*shows_rating)

        plt.bar(title, rating, color='orange')
        plt.xlabel('Titles')
        plt.ylabel('Rating')
        plt.title('Top 5 shows rating')
        plt.show()

    def showCircleDiagram(self):
        show_count_for_genres = self.statistics_provider.get_show_count_for_genres()
        genres, show_count = zip(*show_count_for_genres)

        plt.pie(show_count, labels=genres, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title('Genre percentage')
        plt.show()

    def showGraph(self):
        actor_count_for_show = self.statistics_provider.get_actor_count_for_show()
        title, actor_count = zip(*actor_count_for_show)

        plt.plot(title, actor_count, marker='o', linestyle='-')
        plt.ylabel('Actors number')
        plt.title('Actors number in shows')
        plt.xticks(rotation=15)
        plt.show()


def main():
    statistics_visualizer = StatisticsVisualizer()
    statistics_visualizer.showHistogram()
    statistics_visualizer.showCircleDiagram()
    statistics_visualizer.showGraph()


if __name__ == "__main__":
    main()
