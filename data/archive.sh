#!/bin/bash

# Get today's date in YYYY-MM-DD format
today=$(date +%F)

# New filename
new_filename="${today}.csv"

# Rename the file
mv solar.csv "$new_filename"

# Compress the renamed file
gzip "$new_filename"
