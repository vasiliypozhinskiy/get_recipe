import requests
import json
import os


api_key = os.getenv("food_api_key")


def Get_findByIngredients(ingredients: str):
    """Search Recipes by Ingredients
        return recipe, example:
        https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients"""
    findByIngredients_url = "https://api.spoonacular.com/recipes/findByIngredients"
    findByIngredients_options = {"apiKey": api_key,
                                 "ingredients": ingredients,
                                 "ignorePantry": "True",
                                 "number": 10,
                                 "ranking": 2}
    findByIngredients_request = requests.get(findByIngredients_url, findByIngredients_options)
    json_result = findByIngredients_request.text
    recipes = json.loads(json_result)
    return recipes


def Get_Analyzed_Recipe_Instructions(recipe_id: int):
    """Get an analyzed breakdown of a recipe's instructions.
    Each step is enriched with the ingredients and equipment required.
    Example: https://spoonacular.com/food-api/docs#Get-Analyzed-Recipe-Instructions"""

    Get_Analyzed_Recipe_Instructions_url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    Get_Analyzed_Recipe_Instructions_options = {"apiKey": api_key, "stepBreakdown": "True"}
    Get_Analyzed_Recipe_Instructions_request = requests.get(Get_Analyzed_Recipe_Instructions_url,
                                                            Get_Analyzed_Recipe_Instructions_options)

    instructions = json.loads(Get_Analyzed_Recipe_Instructions_request.text)
    return instructions


def Get_Similar_Recipes(recipe_id: int):
    """Find recipes which are similar to the given one."""

    Get_Similar_Recipes_url = f"https://api.spoonacular.com/recipes/{recipe_id}/similar"
    Get_Similar_Recipes_options = {"apiKey": api_key}
    Get_Similar_Recipes_request = requests.get(Get_Similar_Recipes_url,
                                               Get_Similar_Recipes_options)
    json_result = Get_Similar_Recipes_request.text
    recipe = json.loads(json_result)
    return recipe


def Get_Random_Recipes():
    """Recipe format is returned to the standard format. As in Get_findByIngredients function"""

    Get_Random_Recipes_url = f"https://api.spoonacular.com/recipes/random"
    Get_Random_Recipes_options = {"apiKey": api_key,
                                  "number": 10}
    Get_Random_Recipes_request = requests.get(Get_Random_Recipes_url,
                                              Get_Random_Recipes_options)
    json_result = Get_Random_Recipes_request.text
    recipes = json.loads(json_result)
    for recipe in recipes["recipes"]:
        recipe["usedIngredients"] = recipe.pop("extendedIngredients")
        for ingredient in recipe["usedIngredients"]:
            ingredient["unitLong"] = ingredient["measures"]["us"].pop("unitLong")
            ingredient.pop("measures")
        recipe["missedIngredients"] = []
        unused_keys = ['vegetarian', 'vegan', 'glutenFree', 'dairyFree', 'veryHealthy', 'cheap', 'veryPopular',
                       'sustainable', 'weightWatcherSmartPoints', 'gaps', 'lowFodmap', 'aggregateLikes',
                       'spoonacularScore', 'creditsText', 'license', 'sourceName', 'healthScore', 'pricePerServing',
                       'readyInMinutes', 'servings', 'sourceUrl', 'summary', 'cuisines', 'dishTypes', 'diets',
                       'winePairing', 'instructions', 'occasions', 'analyzedInstructions', 'originalId',
                       'spoonacularSourceUrl', 'preparationMinutes', 'cookingMinutes']
        for key in unused_keys:
            try:
                recipe.pop(key)
            except KeyError:
                pass
    return recipes["recipes"]


def Get_image(recipe_id: int) -> bool:
    Get_image_url = f"https://spoonacular.com/recipeImages/{recipe_id}-556x370.jpg"
    Get_image_options = {"apiKey": api_key}
    Get_image_request = requests.get(Get_image_url,
                                     Get_image_options)
    if Get_image_request.status_code == 200:
        with open("current_img.jpg", "wb") as current_img:
            current_img.write(Get_image_request.content)
            return True
    else:
        return False




if __name__ == "__main__":
    print(Get_Random_Recipes())


