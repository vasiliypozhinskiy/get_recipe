from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import request_to_spoonacular
import food_api_ui
import you_sure_ui
import sys
import database


class Application(QtWidgets.QMainWindow, food_api_ui.Ui_Food_api):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Spoonacular api")
        self.setFixedSize(1523, 627)

        recipe_list = database.local_recipes_db.get_recipe_names()
        self.local_recipes.addItems(recipe_list)
        self.local_recipes.currentIndexChanged.connect(self.local_recipes_clicked)

        self.get_recipe.clicked.connect(self.get_recipe_button_clicked)
        self.get_random_recipe.clicked.connect(self.get_random_recipe_button_clicked)
        self.clear_db.clicked.connect(self.clear_db_button_clicked)
        self.delete_from_db.clicked.connect(self.delete_from_local_db_button_clicked)
        self.image = QPixmap("default_img.jpg")
        self.image_area.setPixmap(self.image)

        self.are_you_sure_dialog = AreYouSure()

    def clear_db_button_clicked(self):
        self.are_you_sure_dialog.show()

    def delete_from_local_db_button_clicked(self):
        current_recipe_title = self.local_recipes.currentText()
        current_recipe_id = database.local_recipes_db.get_id_by_title(current_recipe_title)
        database.local_recipes_db.delete_from_db(current_recipe_id)
        self.local_recipes_update()

    def get_recipe_button_clicked(self):
        if not self.check_api_key():
            return
        ingredients = self.lineEdit.text()
        self.lineEdit.clear()
        try:
            recipes = request_to_spoonacular.Get_findByIngredients(ingredients)
        except Exception as error:
            self.textBrowser.append("Error in request 'find by ingredients'")
            self.textBrowser.append(f"{error.__class__}")
            return
        for recipe in recipes:
            recipe_id = recipe["id"]
            try:
                instructions = request_to_spoonacular.Get_Analyzed_Recipe_Instructions(recipe_id)
            except Exception as error:
                self.textBrowser.append("Error in request 'get recipe instructions'")
                self.textBrowser.append(f"{error.__class__}")
                return
            if not instructions:
                continue
            try:
                if database.local_recipes_db.get_recipe_by_id(recipe_id):
                    continue
            except Exception as error:
                self.textBrowser.append("Error in checking database")
                self.textBrowser.append(f"{error.__class__}")
                return
            try:
                database.local_recipes_db.insert_table(recipe)
                instruction = instructions[0]
                database.recipe_instructions.insert_table(recipe["id"], instruction)
                try:
                    self.local_recipes_update()
                    self.local_recipes.setCurrentIndex(self.local_recipes.findText(recipe["title"]))
                except Exception as error:
                    self.textBrowser.append("Error in update local recipes")
                    self.textBrowser.append(f"{error.__class__}")
                self.show_recipe_info(recipe_id)
                self.update_image(recipe_id)
                return
            except Exception as error:
                self.textBrowser.append("Error in insert into database")
                self.textBrowser.append(f"{error.__class__}")
                return
        self.textBrowser.clear()
        self.textBrowser.append("All recipes by this request is already in local database, make request more details")

    def get_random_recipe_button_clicked(self):
        if not self.check_api_key():
            return
        try:
            recipes = request_to_spoonacular.Get_Random_Recipes()
        except Exception as error:
            self.textBrowser.append("Error in request 'get random recipes'")
            self.textBrowser.append(f"{error.__class__}")
            return
        for recipe in recipes:
            recipe_id = recipe["id"]
            try:
                instructions = request_to_spoonacular.Get_Analyzed_Recipe_Instructions(recipe_id)
            except Exception as error:
                self.textBrowser.append("Error in request 'get recipe instructions'")
                self.textBrowser.append(f"{error.__class__}")
                return
            if not instructions:
                continue
            try:
                if database.local_recipes_db.get_recipe_by_id(recipe_id):
                    continue
            except Exception as error:
                self.textBrowser.append("Error in checking database")
                self.textBrowser.append(f"{error.__class__}")
                return
            try:
                database.local_recipes_db.insert_table(recipe)
                instruction = instructions[0]
                database.recipe_instructions.insert_table(recipe["id"], instruction)

                try:
                    self.local_recipes_update()
                    self.local_recipes.setCurrentIndex(self.local_recipes.findText(recipe["title"]))
                except Exception as error:
                    self.textBrowser.append("Error in update local recipes")
                    self.textBrowser.append(f"{error.__class__}")
                self.show_recipe_info(recipe_id)

                self.update_image(recipe_id)
                return
            except Exception as error:
                self.textBrowser.append("Error in insert into database")
                self.textBrowser.append(f"{error.__class__}")
                return

    def local_recipes_clicked(self):
        if self.local_recipes.currentIndex() != -1:
            title = self.local_recipes.currentText()
            recipe_id = database.local_recipes_db.get_id_by_title(title)
            self.show_recipe_info(recipe_id)
            self.update_image(recipe_id)
        else:
            pass

    def local_recipes_update(self):
        try:
            recipe_list = database.local_recipes_db.get_recipe_names()
            self.local_recipes.clear()
            self.local_recipes.addItems(recipe_list)
            self.local_recipes.update()
        except Exception as error:
            self.textBrowser.append(error.__class__)

    def show_recipe_info(self, recipe_id: int):
        self.textBrowser.clear()

        if recipe_id != -1:
            try:
                recipe = database.local_recipes_db.get_recipe_by_id(recipe_id)
                instruction = database.recipe_instructions.get_instruction_by_id(recipe_id)

            except Exception as error:
                self.textBrowser.append("Error in reading from database")
                self.textBrowser.append(f"{error.__class__}")
                return

            try:
                title = recipe["title"]
                recipe_ingredients = recipe["usedIngredients"] + recipe["missedIngredients"]
                self.textBrowser.append(title)
                for ingredient in recipe_ingredients:
                    name = ingredient['name']

                    amount = ingredient['amount']
                    if amount.is_integer():
                        amount = int(amount)
                    else:
                        amount = round(amount, 2)

                    unit = ingredient["unitLong"]
                    buffer_string = f"Ingredient: {name}. Amount: {amount} {unit}"
                    self.textBrowser.append(buffer_string)
            except Exception as error:
                self.textBrowser.append("Error in recipe ingredients")
                self.textBrowser.append(f"{error.__class__}")

            try:
                for step in instruction["steps"]:
                    self.textBrowser.append("Step " + str(step["number"]) + ":")
                    if step["equipment"]:
                        self.textBrowser.append("With " + step["equipment"][0]["name"] + ":")
                    self.textBrowser.append(step["step"])
                self.textBrowser.append("")
            except Exception as error:
                self.textBrowser.append("Error in instructions")
                self.textBrowser.append(f"{error.__class__}")
        else:
            self.textBrowser.append('Database is empty')

    def update_image(self, recipe_id):
        try:
            if request_to_spoonacular.Get_image(recipe_id):
                img_path = "current_img.jpg"
            else:
                img_path = "default_img.jpg"
            self.image = QPixmap(img_path)
            self.image_area.setPixmap(self.image)
            self.image_area.update()
        except Exception as error:
            self.textBrowser.append("Error in image update")
            self.textBrowser.append(f"{error.__class__}")

    def check_api_key(self) -> bool:
        if not request_to_spoonacular.api_key:
            self.textBrowser.clear()
            self.textBrowser.append("API KEY not found, check you system variables")
            return False
        return True


class AreYouSure(QtWidgets.QDialog, you_sure_ui.Ui_AreYouSure):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(478, 159)
        self.setWindowTitle("Are you sure?")

        self.buttonBox.accepted.connect(self.accept_button)

    def accept_button(self):
        database.local_recipes_db.clear_db()
        database.recipe_instructions.clear_db()
        window.local_recipes.clear()
        self.close()


app = QtWidgets.QApplication(sys.argv)
window = Application()
window.show()


def run_app():
    app.exec_()