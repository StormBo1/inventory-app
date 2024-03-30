# Shoe Class created
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = int(quantity)

    def get_cost(self):
        print("Cost of shoe is", str(self.cost))

    def get_quantity(self):
        print(f"Quantity is {self.quantity}")

    def __str__(self):
        return (f"Shoe {self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}")

# populated list with shoe types
shoe_list = []

# automatically read shoe list including try except if file not found
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as inventory:
            stock = inventory.readlines()
            for line_num, lines in enumerate(stock):
                if line_num == 0:
                    continue
                data = lines.strip().split(",")
                print(f"Debug: Line {line_num + 1} - Data: {data}")
                if len(data) == 5:
                    shoe = Shoe(*data)
                    shoe_list.append(shoe)
                else:
                    print(f"Skipping line {line_num + 1}: Invalid data format")
    except FileNotFoundError:
        print("File inventory.txt not found")
    except Exception as e:
        print(f"An error occurred: {e}")

# captures new data into text file
def capture_shoes():
    country = input("From which country is the shoe from?\n")
    code = input("What is the product code of the shoe?\n")
    # Validate code format
    if not code.startswith("SKU") or not code[3:].isdigit():
        print("Invalid code format. Please use the format 'SKU123'.")
        return
    product = input("What brand of shoe is it?\n")
    # will not write to file if value entered is not a number
    try:
        cost = float(input("How much does is cost?\n"))
        quantity = int(input("How many shoes of the same make are there?\n"))
    except ValueError:
        print("Invalid input. Cost must be a number, and quantity must be an integer.")
        return

    new_shoe = Shoe(country, code, product, cost, quantity)
    with open("inventory.txt", "a+") as inventory:
        inventory.write(f"\n{new_shoe.country}, {new_shoe.code}, {new_shoe.product}, {new_shoe.cost}, {new_shoe.quantity}")
    shoe_list.append(new_shoe)

# view all products
def view_all():
    for shoe in shoe_list:
        print(f"Code: {shoe.code}, Product: {shoe.product}, Quantity: {shoe.quantity}, Cost: {shoe.cost}")

# determines what the lowest stock in shoes and restock where necessary
def re_stock():
    if not shoe_list:
        print("No shoes in the inventory.")
        return

    # Find the shoe with the lowest quantity
    lowest_quantity_shoe = min(shoe_list, key=lambda x: x.quantity)

    try:
        # Get the new quantity from the user
        new_quantity = int(input(f"Enter the new quantity for {lowest_quantity_shoe.product}:\n"))

        # Update the shoe object
        lowest_quantity_shoe.quantity = new_quantity

        # Update only the quantity in the text file for the line with the lowest quantity
        with open("inventory.txt", "r") as inventory_file:
            lines = inventory_file.readlines()

        with open("inventory.txt", "w") as inventory_file:
            for line in lines:
                if lowest_quantity_shoe.code in line:
                    # Extract the quantity part and replace it
                    line_parts = line.split(",")
                    line_parts[-1] = f" {new_quantity}\n"
                    updated_line = ",".join(line_parts)
                    inventory_file.write(updated_line)
                else:
                    inventory_file.write(line)

        print(f"Restocked {lowest_quantity_shoe.product} to {new_quantity} quantity.")
    except ValueError:
        print("Invalid quantity. Please enter a valid number.")

        
# search for a specified shoes using its Unique code
def search_shoe():
    while True:
        shoe_code = input("Please insert the product code of the shoe(include SKU in entry):\n").strip().lower()
        if shoe_code.startswith("sku") and shoe_code[3:].isdigit():
            found_shoes = [shoe for shoe in shoe_list if shoe.code.lower() == shoe_code]
            if found_shoes:
                print("Found shoe(s):")
                for found_shoe in found_shoes:
                    print(found_shoe)
            else:
                print(f"No shoes found with product code {shoe_code}")
            break
        else:
            print("Invalid input. Please enter a valid product code (e.g., SKU12345).")

# prints out the total value of shoes per brand name.
def value_per_item():
    for shoe in shoe_list:
        try:
            cost = float(shoe.cost)
            quantity = int(shoe.quantity)
            value = cost * quantity
            print(f"Value for {shoe.product}: R{value}")
        except (ValueError, TypeError):
            print(f"Invalid data for{shoe.product}: cost ={shoe.cost}, quantity={shoe.quantity}")

# prints out the highest quantity of shoes in list
def highest_qty():
    if not shoe_list:
        print("No shoes in the list.")
        return

    max_quantity_shoe = None
    max_quantity = 0

    for shoe in shoe_list:
        try:
            quantity = int(shoe.quantity)
            if quantity > max_quantity:
                max_quantity = quantity
                max_quantity_shoe = shoe
        except ValueError:
            print(f"Invalid quantity for {shoe.product}: {shoe.quantity}")

    if max_quantity_shoe:
        print(f"The shoe with the highest quantity on sale is: {max_quantity_shoe}")
    else:
        print("No shoes in the list.")


print(read_shoes_data())

menu = True
while True:
    user_choice = int(input('''Please select from the list below what you would like to do:

1. Capture data
2. View all shoes
3. Re stock shoes
4. Search for a shoe
5. Value per item
6. Item for sale
7. Exit\n'''))

    if user_choice == 1:
        capture_shoes()
    elif user_choice == 2:
        view_all()
    elif user_choice == 3:
        re_stock()
    elif user_choice == 4:
        search_shoe()
    elif user_choice == 5:
        value_per_item()
    elif user_choice == 6:
        highest_qty()
    elif user_choice == 7:
        print("Thank you and goodbye")
        break
    else:
        print("Invalid option")
