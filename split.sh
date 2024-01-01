
#!/bin/bash

# Directory where the mixed-data is located
mixed_data_dir="test-flight-user-mix"

# Loop over all files in the mixed-data directory
for file in "$mixed_data_dir"/*
do
    # Extract the date from the filename
    date=$(echo "$file" | grep -oP '\d{4}-\d{2}-\d{2}')

    # Create a new directory for this date if it doesn't exist
    mkdir -p "flight-user/$date"

    # Move the file to the new directory
    mv "$file" "flight-user/$date"
done