import itertools
import pandas as pd

# Data
outfit = ['FORMAL']
style = ['MINIMAL']
belt = ['NO']
watch = ['STARPPED ANALOG', 'STARPPED DIGITAL', 'METAL GOLD', 'METAL ROSE GOLD', 'METAL SILVER', 'METAL BLACK']
shoes = ['BLACK', 'BROWN']
shirt = ["ASH", "BEIGE", "MINT", "LIGHT BROWN", "GREY", "WHITE"]
pants = ["ASH", "BEIGE", "BLACK", "BROWN", "GREEN", "GREY", "MAROON", "NAVY BLUE", "OLIVE", "ORANGE", "PURPLE", "WHITE", "YELLOW"]

# Generate combinations where shirt and pant colors match
matching_combinations = [
    (o, s, b, w, sho,sh, p)  # Include all variables
    for o, s, b, w, sho, sh, p in itertools.product(outfit, style, belt, watch, shoes, shirt, pants)
    if sh == p  # Shirt and pants colors must match
]

# Save to Excel
df = pd.DataFrame(matching_combinations, columns=["Outfit", "Style", "Belt", "Watch", "Shoes", "Shirt","Pants"])
file_path = 'FORMAL_PROFESSIONAL_MONO_WITH_BELT.xlsx'
df.to_excel(file_path, index=False)

print(f"Matching combinations saved to {file_path}")
