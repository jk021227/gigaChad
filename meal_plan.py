import pandas as pd

# Load the CSV file
file_path = 'restaurants_sample_with_nutrition.csv'  # Change this to the appropriate file name
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
    Generating a full day's meal plan.
    
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

def run_user_info(name, age, weight, height, gender, goal):
    """
    This function calculates the requirements, generates a meal plan,
    and prints the results for a given set of user parameters.
    """

    # mapping the integer-coded goal back to its corresponding string
    if goal == 1:
        goal_str = 'gain muscle'
    elif goal == 2:
        goal_str = 'lose weight'
    elif goal == 3:
        goal_str = 'maintain weight'


    print(f"\nGenerating {name}'s meal plan!\n")
    print(f"Age: {age}, Weight: {weight}kg, Height: {height}cm, Gender: {gender}, Goal: {goal_str}")

    # calling calculate_requirements with the string representation of the goal
    total_calories, protein_requirement = calculate_requirements(weight, height, age, gender, goal_str)
    print(f"Calorie requirement: {total_calories:.2f} calories")
    print(f"Protein requirement: {protein_requirement:.2f} grams")

    # generating meal plan based on the total calories and protein requirement
    meal_plan, total_calories_consumed, total_protein_consumed = generate_meal_plan(total_calories, protein_requirement, goal_str)
    
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
    print("Welcome to the Meal Plan Generator!")

    '''
    getting user info.
    '''
    # getting validated name (string)
    while True:
        name = input("Please enter your name: ").strip()
        # ensuring all parts of the name are alphabetic (excluding spaces)
        if all(part.isalpha() for part in name.split()):
            break
        else:
            print("Invalid input! Name must contain only letters and spaces. Please try again.")

    # getting validated age (integer)
    while True:
        try:
            age = int(input("Please enter your age: "))
            if age > 0:  # Basic validation for positive age
                break
            else:
                print("Age must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input! Please enter a valid number for age.")

    # getting validated weight (float)
    while True:
        try:
            weight = float(input("Please enter your weight in kg: "))
            if weight > 0:  # Basic validation for positive weight
                break
            else:
                print("Weight must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input! Please enter a valid number for weight.")

    # getting validated height (float)
    while True:
        try:
            height = float(input("Please enter your height in cm: "))
            if height > 0:  # Basic validation for positive height
                break
            else:
                print("Height must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input! Please enter a valid number for height.")

    # getting validated gender (either 'male' or 'female')
    while True:
        gender = input("Please enter your gender (male/female): ").lower()
        if gender in ['male', 'female']:
            break
        else:
            print("Invalid input! Please enter 'male' or 'female'.")

    # getting validated goal (integer with options)
    while True:
        try:
            goal = int(input("What is your fitness goal:\n 1. gain muscle\n 2. lose weight\n 3. maintain weight\n: "))
            if goal in [1, 2, 3]:
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input! Please enter a valid number (1, 2, or 3).")

    # Call the function to run the meal plan generator with the user's inputs
    run_user_info(name, age, weight, height, gender, goal)

if __name__ == "__main__":
    main()