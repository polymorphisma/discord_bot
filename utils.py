from prettytable import PrettyTable


def format_to_table(data):
    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Name", "From", "To", "Event", "Substitute"]

    # Add rows to the table
    for entry in data:
        table.add_row([entry['Name'], entry['From'], entry['To'], entry['Event'], entry['Substitute'] or "None"])

    # Return the table as a string
    return f"```\n{table}\n```"
