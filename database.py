import sqlite3
import functools


def db_connection(func):
    @functools.wraps(func)
    def connect_close(self, *args, **kwargs):
        self.connection = sqlite3.connect(f"{self.db_path}")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""PRAGMA foreign_keys = ON""")
        func_value = func(self, *args, **kwargs)
        self.cursor.close()
        return func_value

    return connect_close


class LocalRecipesDB:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @db_connection
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS local_recipes (
        id INT PRIMARY KEY,
        title TEXT,
        recipe TEXT
        )""")
        self.connection.commit()

    @db_connection
    def get_recipe_names(self) -> list:
        self.cursor.execute("""SELECT title from local_recipes ORDER BY id""")
        recipe_names = []
        for recipe_name in self.cursor:
            recipe_names.append(recipe_name[0])
        return recipe_names

    @db_connection
    def get_id_by_title(self, title: str) -> int:
        self.cursor.execute(f"""SELECT id from local_recipes WHERE title = :title""",
                            {"title": title})
        recipe_id = self.cursor.fetchone()[0]
        return int(recipe_id)

    @db_connection
    def insert_table(self, recipe):
        self.cursor.execute(f"""SELECT id from local_recipes WHERE id = {recipe["id"]}""")
        if not self.cursor.fetchone():
            self.cursor.execute(f"""INSERT INTO local_recipes (id, title, recipe) VALUES (:id,
                                                                                          :title,
                                                                                          :recipe)""",
                                {"id": recipe["id"], "title": recipe["title"], "recipe": str(recipe)})
            self.connection.commit()

    @db_connection
    def check_db(self):
        self.cursor.execute("""SELECT * from local_recipes ORDER BY id""")
        for row in self.cursor:
            print(row)

    @db_connection
    def clear_db(self):
        self.cursor.execute("""DROP TABLE local_recipes""")
        self.create_table()
        self.connection.commit()

    @db_connection
    def delete_from_db(self, recipe_id: int):
        self.cursor.execute(f"""DELETE FROM local_recipes WHERE id = {recipe_id}""")
        self.connection.commit()

    @db_connection
    def get_recipe_by_id(self, recipe_id: int):
        self.cursor.execute(f"""SELECT * from local_recipes WHERE id = {recipe_id}""")
        line = self.cursor.fetchone()
        if line:
            recipe = eval(line[2])
        else:
            recipe = None
        return recipe


class RecipeInstructionsDB:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @db_connection
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS recipe_instructions (
            id INT,
            instruction TEXT,
            FOREIGN KEY (id) REFERENCES local_recipes (id) ON DELETE CASCADE)""")
        self.connection.commit()

    @db_connection
    def insert_table(self, recipe_id: int, instruction):
        self.cursor.execute(f"""SELECT id from recipe_instructions WHERE id = {recipe_id}""")
        if not self.cursor.fetchone():
            self.cursor.execute(f"""INSERT INTO recipe_instructions (id, instruction) VALUES (:id, :instruction)""",
                                {"id": recipe_id, "instruction": str(instruction)})
        self.connection.commit()

    @db_connection
    def get_instruction_by_id(self, recipe_id: int):
        self.cursor.execute(f"""SELECT * from recipe_instructions WHERE id = {recipe_id}""")
        line = next(self.cursor)
        instruction = eval(line[1])
        return instruction

    @db_connection
    def clear_db(self):
        self.cursor.execute("""DROP TABLE recipe_instructions""")
        self.create_table()
        self.connection.commit()


if __name__ != "__main__":
    db_path = "food_api.db"
    local_recipes_db = LocalRecipesDB(db_path)
    recipe_instructions = RecipeInstructionsDB(db_path)
    local_recipes_db.create_table()
    recipe_instructions.create_table()











