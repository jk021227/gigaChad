import csv
import time
import os
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_nutritional_info_batch(items):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            messages = [
                {"role": "system", "content": "You are a nutritional assistant. Provide estimates for calories, protein, fat, and carbs based on food descriptions."},
                {"role": "user", "content": "For each of the following food items, estimate the calories, protein (g), fat (g), and carbs (g). Respond with only the four numbers separated by commas for each item, with items separated by semicolons:\n" + "\n".join([f"{name}: {description}" for name, description in items])}
            ]
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            results = response.choices[0].message.content.strip().split(';')
            return [parse_nutrition_info(result.strip()) for result in results]
        except Exception as e:
            print(f"Error in API call (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                print("Max retries reached. Returning default values.")
                return [["N/A", "N/A", "N/A", "N/A"]] * len(items)
            time.sleep(5)  # Wait for 5 seconds before retrying

def parse_nutrition_info(info_string):
    try:
        values = info_string.split(',')
        return [value.strip() for value in values[:4]]  # Take only the first 4 values
    except:
        return ["N/A", "N/A", "N/A", "N/A"]

# Read the CSV file
input_file = 'restaurants_sample.csv'
output_file = 'restaurants_sample_with_nutrition.csv'

try:
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header
        header = next(reader)
        header.extend(['Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)'])
        writer.writerow(header)
        
        # Process rows in batches
        batch_size = 10
        batch = []
        for row in tqdm(reader, desc="Processing menu items"):
            try:
                batch.append(row)
                if len(batch) == batch_size:
                    items = [(row[2], row[3]) for row in batch]  # Name is in the third column, description in the fourth
                    nutrition_infos = get_nutritional_info_batch(items)
                    
                    for row, nutrition_info in zip(batch, nutrition_infos):
                        # Ensure we have 4 values, if not, pad with "N/A"
                        nutrition_info = (nutrition_info + ["N/A"]*4)[:4]
                        row.extend(nutrition_info)
                        writer.writerow(row)
                        print(f"Processed: {row[2]} - {row[3][:50]}...")  # Print name and first 50 chars of description
                        print(f"Nutrition: Calories: {nutrition_info[0]}, Protein: {nutrition_info[1]}, Fat: {nutrition_info[2]}, Carbs: {nutrition_info[3]}")
                        print("-" * 50)
                    
                    batch = []
                    time.sleep(3)  # Delay to avoid hitting rate limits
            except Exception as e:
                print(f"Error processing row: {e}")
                continue  # Skip this row and continue with the next
        
        # Process any remaining items
        if batch:
            items = [(row[2], row[3]) for row in batch]
            nutrition_infos = get_nutritional_info_batch(items)
            for row, nutrition_info in zip(batch, nutrition_infos):
                nutrition_info = (nutrition_info + ["N/A"]*4)[:4]
                row.extend(nutrition_info)
                writer.writerow(row)
                print(f"Processed: {row[2]} - {row[3][:50]}...")
                print(f"Nutrition: Calories: {nutrition_info[0]}, Protein: {nutrition_info[1]}, Fat: {nutrition_info[2]}, Carbs: {nutrition_info[3]}")
                print("-" * 50)

    print(f"Processing complete. Results written to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Script execution completed.")