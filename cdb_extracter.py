import pandas as pd

# Replace the file path with the actual path to your CSV file
file_path = "data/cards_text/datas.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, delimiter='|')

# Now you can work with the DataFrame 'df'

print(df.head(10))


from lupa import LuaRuntime

# Create a Lua runtime
lua = LuaRuntime(unpack_returned_tuples=True)

# Load your Lua script
lua.execute("dofile('myluafile.lua')")

# Access the 'params' table from Lua
params_table = lua.globals.params

# Convert the Lua table to a Python dictionary
param_dict = dict(params_table)

# Now, param_dict contains the parameter name-value pairs
print(param_dict)
