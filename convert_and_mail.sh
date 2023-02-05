

# Check if input file exists
if [ ! -f "$1" ]; then
  echo "Input file does not exist"
  exit 1
fi

# Replace all tabs with commas
sed 's/\t/,/g' "$1" > "$1.csv"

# Email the CSV file as an attachment
mail -s "Converted report" -a "$1.csv" recipient@example.com <<< "The report has been converted and attached."

# Print success message
echo "Conversion and email successful."
