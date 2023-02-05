
# Check if input file exists
if [ ! -f "$1" ]; then
  echo "Input file does not exist"
  exit 1
fi

# Replace all tabs with commas
sed 's/\t/,/g' "$1" > "$1.csv"

# Print success message
echo "Conversion successful. Output file: $1.csv"
