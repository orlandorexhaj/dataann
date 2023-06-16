import json
import statistics

# Sales Inquiry table
date = input("Enter date: ")

date = date.replace("/", "_")
day = date.split("_")[1]

current_json = open(f"{date}.json", "r")
sales_inquiry = eval(current_json.read())
current_json.close()


# Ask for new sales
wait_input = input("\nAre there any new sales? (y/n) ")
if wait_input == "y":
    new_json = open(f"1_{int(day)+1}_2023.json", "x")
    for product, sales in sales_inquiry.items():
        print(f"Enter sales for {product} on 1/{int(day)+1}/2023: ", end="")
        value = input()
        while not value.isdigit():
            value = input("Invalid input. Enter sales: ")
        sales_inquiry[product][f"1/{int(day)+1}/2023"] = int(value)

    new_json.write(json.dumps(sales_inquiry, indent=4))
    new_json.close()
elif wait_input != "n":
    print("Invalid input.")



# Calculate mean, median, and standard deviation
inquiry_values = [quantity for sales in sales_inquiry.values() for quantity in sales.values()]
mean = statistics.mean(inquiry_values)
stdev = statistics.stdev(inquiry_values)

# Calculate z-score and identify anomalies
threshold = 2
anomalies = []
print("\nAnomalies:")
for product, sales in sales_inquiry.items():
    for date, quantity in sales.items():
        z_score = (quantity - mean) / stdev
        if abs(z_score) > threshold:
            anomalies.append((product, date, quantity, z_score))

# Print the anomalies
if len(anomalies) > 0:
    print("Product\t\tDate\t\tQuantity\tZ-Score")
    for anomaly in anomalies:
        print(f"{anomaly[0]}\t\t{anomaly[1]}\t{anomaly[2]}\t\t{anomaly[3]}")
else:
    print("No anomalies found.")

# Write the Sales Inquiry table

table = 'Product|'
for date, quantity in sales_inquiry["Apples"].items():
    table += date + "|"
table += "\n"
for date, quantity in sales_inquiry["Apples"].items():
    table += "---|"
table += "---\n"

for product, sales in sales_inquiry.items():
    table += product + "|"
    for date, quantity in sales.items():
        table += str(quantity) + "|"
    table += "\n"
with open("table.md", "w") as f:
    f.write(table)

# Printing the Sales Inquiry table
print("Sales Inquiry table written in table.md")