import pandas as pd
import random

# Load the CSV file
file_path = 'restaurants_data.csv'  # Change this to the appropriate file name
meal_data = pd.read_csv(file_path)

# Remove rows with missing or NaN values in essential columns
meal_data = meal_data.dropna(subset=['Calories', 'Protein (g)'])

# Convert 'Calories' and 'Protein (g)' to numeric, coercing errors to NaN
meal_data['Calories'] = pd.to_numeric(meal_data['Calories'], errors='coerce')
meal_data['Protein (g)'] = pd.to_numeric(meal_data['Protein (g)'], errors='coerce')

# Remove any rows where the conversion resulted in NaN
meal_data = meal_data.dropna(subset=['Calories', 'Protein (g)'])

def calculate_requirements(weight, height, age, gender, goal):
    """
    Calculate calorie and protein requirements based on user information.
    
    This function uses the Mifflin-St Jeor Equation to calculate BMR,
    then adjusts for activity level and goal to determine calorie needs.
    Protein requirement is set at 2g per kg of body weight.
    
    Args:
    weight (float): User's weight in kg
    height (float): User's height in cm
    age (int): User's age in years
    gender (str): User's gender ('male' or 'female')
    goal (str): User's fitness goal ('gain muscle', 'lose weight', or 'maintain weight')
    
    Returns:
    tuple: (total_calories, protein_requirement)
    """
    # Calculate Basal Metabolic Rate (BMR)
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Calculate Total Daily Energy Expenditure (TDEE)
    # Assuming moderate activity level (1.55 multiplier)
    tdee = bmr * 1.55

    # Adjust calories based on goal
    if goal.lower() == 'gain muscle':
        total_calories = tdee + 500  # Calorie surplus for muscle gain
    elif goal.lower() == 'lose weight':
        total_calories = tdee - 500  # Calorie deficit for weight loss
    else:
        total_calories = tdee  # Maintenance calories

    # Calculate protein requirement (2g per kg of body weight)
    protein_requirement = weight * 2.0

    return total_calories, protein_requirement

def select_meal(remaining_calories, min_calories, min_protein):
    """
    Select a meal based on calorie and protein criteria.
    
    This function filters the meal data based on the given criteria
    and randomly selects a meal that fits within the constraints.
    
    Args:
    remaining_calories (float): Remaining calories for the day
    min_calories (float): Minimum calories for the meal
    min_protein (float): Minimum protein for the meal
    
    Returns:
    pd.Series or None: Selected meal or None if no suitable meal found
    """
    # Filter meals based on calorie and protein criteria
    possible_meals = meal_data[
        (meal_data['Calories'] <= remaining_calories) &
        (meal_data['Calories'] >= min_calories) &
        (meal_data['Protein (g)'] >= min_protein)
    ]
    
    # If no meals meet the criteria, relax the protein requirement
    if possible_meals.empty:
        possible_meals = meal_data[meal_data['Calories'] <= remaining_calories]
    
    # If still no meals are found, return None
    if possible_meals.empty:
        return None
    
    # Randomly select a meal from the possible options
    return possible_meals.sample(1).iloc[0]

def generate_meal_plan(total_calories, protein_requirement, goal):
    """
    Generate a full day's meal plan.
    
    This function creates a meal plan by selecting meals for breakfast,
    lunch, dinner, and up to two snacks, aiming to meet the calorie
    and protein requirements.
    
    Args:
    total_calories (float): Total calories for the day
    protein_requirement (float): Protein requirement for the day
    goal (str): User's fitness goal
    
    Returns:
    tuple: (selected_meals, total_calories_consumed, total_protein_consumed)
    """
    selected_meals = {"breakfast": [], "lunch": [], "dinner": [], "snacks": []}
    total_calories_consumed = 0
    total_protein_consumed = 0

    # Select meals for breakfast, lunch, and dinner
    for meal_type in ["breakfast", "lunch", "dinner"]:
        remaining_calories = total_calories - total_calories_consumed
        min_calories = min(300, remaining_calories)
        min_protein = 15 if meal_type == "breakfast" else 25

        meal = select_meal(remaining_calories, min_calories, min_protein)
        if meal is not None:
            selected_meals[meal_type].append(meal)
            total_calories_consumed += meal['Calories']
            total_protein_consumed += meal['Protein (g)']

    # Add snacks if there's room in the calorie budget
    while total_calories_consumed < total_calories * 0.9 and len(selected_meals['snacks']) < 2:
        remaining_calories = total_calories - total_calories_consumed
        snack = select_meal(remaining_calories, 100, 5)
        if snack is not None:
            selected_meals['snacks'].append(snack)
            total_calories_consumed += snack['Calories']
            total_protein_consumed += snack['Protein (g)']
        else:
            break

    return selected_meals, total_calories_consumed, total_protein_consumed

def get_user_input(prompt, input_type):
    """
    Get and validate user input.
    
    This function prompts the user for input and validates it based on the expected type.
    It continues to prompt until valid input is received.
    
    Args:
    prompt (str): Prompt to display to the user
    input_type (str): Type of input expected ('int', 'float', or 'str')
    
    Returns:
    int, float, or str: Validated user input
    """
    while True:
        try:
            if input_type == 'int':
                return int(input(prompt))
            elif input_type == 'float':
                return float(input(prompt))
            elif input_type == 'str':
                value = input(prompt).lower()
                if value not in ['male', 'female', 'gain muscle', 'lose weight', 'maintain weight']:
                    raise ValueError("Invalid input, please try again.")
                return value
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def run_test_case(name, age, weight, height, gender, goal):
    """
    Run a test case and print the results.
    
    This function calculates the requirements, generates a meal plan,
    and prints the results for a given set of user parameters.
    
    Args:
    name (str): Name of the test case
    age (int): User's age
    weight (float): User's weight in kg
    height (float): User's height in cm
    gender (str): User's gender
    goal (str): User's fitness goal
    """
    print(f"\n--- Test Case: {name} ---")
    print(f"Age: {age}, Weight: {weight}kg, Height: {height}cm, Gender: {gender}, Goal: {goal}")

    total_calories, protein_requirement = calculate_requirements(weight, height, age, gender, goal)
    print(f"Calorie requirement: {total_calories:.2f} calories")
    print(f"Protein requirement: {protein_requirement:.2f} grams")

    meal_plan, total_calories_consumed, total_protein_consumed = generate_meal_plan(total_calories, protein_requirement, goal)
    
    print("\nMeal Plan:")
    for meal_time, meals in meal_plan.items():
        print(f"  {meal_time.capitalize()}:")
        for meal in meals:
            print(f"    {meal['Menu Item']} from {meal['Restaurant Name']}")
            print(f"      Calories: {meal['Calories']:.0f}, Protein: {meal['Protein (g)']:.1f}g")
            if 'Link' in meal and pd.notna(meal['Link']) and meal['Link']:
                print(f"      Order here: {meal['Link']}")

    print(f"\nTotal calories: {total_calories_consumed:.2f}")
    print(f"Total protein: {total_protein_consumed:.2f}g")

    calorie_diff = total_calories_consumed - total_calories
    protein_diff = total_protein_consumed - protein_requirement

    calorie_percent_diff = abs(calorie_diff) / total_calories * 100

    if calorie_percent_diff <= 10:
        print(f"Meal plan is within {calorie_percent_diff:.1f}% of calorie target.")
    elif calorie_diff > 0:
        print(f"Meal plan is {calorie_diff:.2f} calories ({calorie_percent_diff:.1f}%) over target.")
    else:
        print(f"Meal plan is {-calorie_diff:.2f} calories ({calorie_percent_diff:.1f}%) under target.")

    if protein_diff >= 0:
        print("Meal plan meets or exceeds protein target.")
    else:
        print(f"Meal plan is {-protein_diff:.2f} grams short of protein target.")

def main():
    """
    Main function to run the meal plan generator.
    
    This function defines test cases, runs them, and then offers
    the option for the user to input their own data for a custom meal plan.
    """
    print("Welcome to the Meal Plan Generator!")
    
    # Define test cases
    test_cases = [
        ("Weight Loss Female", 25, 70, 165, "female", "lose weight"),
        ("Muscle Gain Male", 30, 80, 180, "male", "gain muscle"),
        ("Maintenance Female", 40, 60, 160, "female", "maintain weight"),
        ("Weight Loss Male", 50, 90, 175, "male", "lose weight"),
        ("Muscle Gain Female", 35, 65, 170, "female", "gain muscle")
    ]

    # Run test cases
    for case in test_cases:
        run_test_case(*case)

    # Option for manual input
    if input("\nWould you like to enter your own data? (y/n): ").lower() == 'y':
        age = get_user_input("Please enter your age: ", 'int')
        weight = get_user_input("Please enter your weight in kg: ", 'float')
        height = get_user_input("Please enter your height in cm: ", 'float')
        gender = get_user_input("Please enter your gender (male/female): ", 'str')
        goal = get_user_input("What is your fitness goal (gain muscle, lose weight, maintain weight)?: ", 'str')

        run_test_case("Custom Input", age, weight, height, gender, goal)

if __name__ == "__main__":
    main()