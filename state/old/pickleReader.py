import os
import pprint
import pickle

# Get the list of files in the current directory
files = os.listdir()

# Iterate over the files
for file in files:
  # Check if the file has a .pkl extension
  if file.endswith('.pkl'):
    # Open the file and read the contents
    with open(file, 'rb') as f:
      contents = pickle.load(f)
      
    # Create a copy of the contents
    contents_copy = contents.copy()
    
    # Replace the value in the key "layer2" with just the first element
    contents_copy["layer2"] = contents_copy["layer2"][0]
    contents_copy["metaTiles"] = contents_copy["metaTiles"][0]
    contents_copy["enemyList"] = contents_copy["enemyList"][0]
    

    # Use pprint to pretty-print the modified contents
    print(file)
    print('-------------')
    print('')
    pprint.pprint(contents_copy)