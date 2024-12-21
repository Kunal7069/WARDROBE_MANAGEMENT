
import itertools
import pandas as pd

# Define the lists
outfit = ['FORMAL']
style = ['MINIMAL']
belt = ['NO']
watch = ['NO']
shoes = ['BLACK', 'BROWN']
shirt = ["WHITE", "BLACK", "GREY", "YELLOW", "ORANGE", "SKY BLUE", "BABY PINK", "MINT", "LIGHT GREEN"]
pants = ["BLACK", "NAVY BLUE", "MAROON","GREEN","ASH"]

# Generate all combinations
combinations = list(itertools.product(outfit, style, belt, watch, shoes, shirt, pants))

# Create a DataFrame
columns = ['Outfit', 'Style', 'Belt', 'Watch', 'Shoes', 'Shirt', 'Pants']
df = pd.DataFrame(combinations, columns=columns)

# Save to Excel
output_file = 'FORMAL_MINIMAL_CONTRAST_WITHOUT_WATCH.xlsx'
df.to_excel(output_file, index=False)

print(f"Excel file '{output_file}' has been created successfully!")
