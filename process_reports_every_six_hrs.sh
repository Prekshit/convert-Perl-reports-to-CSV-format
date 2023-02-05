#!/bin/bash

# Set the sender email address and recipient email address
sender="sender@example.com"
recipient="recipient@example.com"

# Check if there are any new emails from the specified sender
new_emails=$(grep "^From:.*$sender" /var/spool/mail/user | wc -l)

# Process new emails if any
if [ "$new_emails" -gt 0 ]; then

  # Loop through all new emails from the sender
  for email in $(grep "^From:.*$sender" /var/spool/mail/user); do

    # Extract the subject of the email
    subject=$(echo "$email" | awk -F'Subject: ' '{print $2}' | awk -F'\n' '{print $1}')

    # Extract the attachments of the email
    attachments=$(echo "$email" | awk '/^--.*$/{x=0}; x; /^Content-Disposition: attachment/{x=1}')

    # Loop through all attachments
    for attachment in "$attachments"; do

      # Check if the attachment is a Perl report
      if [ "${attachment##*.}" == "pl" ]; then

        # Replace all tabs with commas in the Perl report
        echo "$attachment" | awk 'BEGIN{RS="\n\n";FS="\n"} {print $2}' | sed 's/\t/,/g' > "$subject.csv"

        # Email the CSV file as an attachment
        mail -s "Converted report" -a "$subject.csv" "$recipient" <<< "The attached Perl report has been converted to CSV format."

        # Print success message
        echo "Conversion and email successful."

      fi

    done

  done

fi

# Sleep for 6 hours
sleep 6h
