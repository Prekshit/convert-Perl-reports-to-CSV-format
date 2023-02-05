#!/bin/bash

# Set the sender email address and recipient email address
sender="sender@example.com"
recipient="recipient@example.com"

# Path to the Outlook CLI tool
outlook="/usr/bin/outlook"

# Check if there are any new emails from the specified sender
new_emails=$("$outlook" search --folder Inbox --sender "$sender" | wc -l)

# Process new emails if any
if [ "$new_emails" -gt 0 ]; then

  # Loop through all new emails from the sender
  for email in $("$outlook" search --folder Inbox --sender "$sender"); do

    # Extract the subject of the email
    subject=$("$outlook" show --id "$email" --field Subject)

    # Extract the attachments of the email
    attachments=$("$outlook" show --id "$email" --field Attachments)

    # Loop through all attachments
    for attachment in "$attachments"; do

      # Check if the attachment is a Perl report
      if [ "${attachment##*.}" == "pl" ]; then

        # Replace all tabs with commas in the Perl report
        "$outlook" show --id "$email" --attachment "$attachment" | sed 's/\t/,/g' > "$subject.csv"

        # Email the CSV file as an attachment
        "$outlook" send --to "$recipient" --subject "Converted report" --body "The attached Perl report has been converted to CSV format." --attachment "$subject.csv"

        # Print success message
        echo "Conversion and email successful."

      fi

    done

  done

fi

# Sleep for 6 hours
sleep 6h
