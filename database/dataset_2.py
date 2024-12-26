
import itertools
import pandas as pd

# Define the lists
outfit_input = ['FORMAL']
style_input = ['PROFESSIONAL']
belt_input = ['YES','NO']
watch_input = ['YES','NO']
shoes_input=['YES','NO']
belt_yes_output = ['BLACK','BROWN']
belt_no_output = ['NO']
watch_yes_output = ['ANALOG']
watch_no_output = ['NO']
shoes_yes_output = ['BLACK', 'BROWN']
shoes_no_output = ['NO']
shirt_output = ["BLACK", "WHITE", "BROWN", "ASH", "NAVY BLUE", "MAROON", "PURPLE", "YELLOW", "GREEN", "ORANGE"]
pants_output = ["BLACK", "WHITE", "BROWN", "ASH", "NAVY BLUE", "MAROON", "PURPLE", "YELLOW", "GREEN", "ORANGE"]

# Generate all combinations
combinations = list(itertools.product(outfit_input, style_input, belt_input, watch_input, shoes_input, shirt_output, pants_output))
data = []

for combination in combinations:
    outfit, style, belt, watch, shoes, shirt, pants = combination
    
    # Skip combinations where shirt_output and pant_output are not the same
    if shirt != pants:
        continue

    # Determine outputs based on inputs
    belt_output = 'NO' if belt == 'NO' else 'BROWN' if pants == 'BROWN' else 'BLACK'
    watch_output = watch_yes_output[0] if watch == 'YES' else watch_no_output[0]
    shoes_output = shoes_yes_output if shoes == 'YES' else shoes_no_output
    
    # Create rows for each shoe color
    for shoe_color in (shoes_output if isinstance(shoes_output, list) else [shoes_output]):
        data.append([outfit, style, belt, watch, shoes, belt_output, watch_output, shoe_color, shirt, pants])

# Create DataFrame with updated columns
columns = ["outfit_input", "style_input", "belt_input", "watch_input", "shoes_input", 
           "belt_output", "watch_output", "shoes_output", "shirt_output", "pant_output"]
df = pd.DataFrame(data, columns=columns)

# Save to Excel
df.to_excel("matching_combinations2.xlsx", index=False)

print("Excel file 'matching_combinations.xlsx' has been created with matching shirt and pant outputs.")