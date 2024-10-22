import os
# Base directory for files - Modified to use current directory for better portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def setup_files():
    """Initialize necessary files with sample data if they don't exist"""
    files_data = {
        'users.txt': 'admin1|admin123|admin|Main Canteen\nstudent1|pass123|student|S001|1000|wallet123\n',
        'wallet.txt': 'S001|500.0\n',
        'food_items.txt': '1|Burger|Delicious burger|100|True\n2|Pizza|Cheesy pizza|200|True\n',
        'bill_history.txt': ''
    }
    
    for filename, initial_data in files_data.items():
        file_path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(initial_data)
# File paths
users_file = os.path.join(BASE_DIR, 'users.txt')
wallet_file = os.path.join(BASE_DIR, 'wallet.txt')
bill_history_file = os.path.join(BASE_DIR, 'bill_history.txt')
food_items_file = os.path.join(BASE_DIR, 'food_items.txt')
# Exception Classes
class CanteenException(Exception):
    """Base exception class for canteen-related errors"""
    pass
class InsufficientBalanceException(CanteenException):
    def __init__(self, message="Insufficient balance to complete the transaction"):
        super().__init__(message)
class InvalidPasswordException(CanteenException):
    def __init__(self, message="Invalid password"):
        super().__init__(message)
class UserNotFoundException(CanteenException):
    def __init__(self, message="User not found"):
        super().__init__(message)
# User class
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    def greet_user(self):
        """Base greeting method - Polymorphism example"""
        print(f"Welcome {self.username}!")
    def authenticate(self, password):
        """Authenticate user"""
        return self.password == password

# Student class (Inheritance)
class Student(User):
    def __init__(self, username, password, role, student_id, canteen_card_balance, wallet_password):
        super().__init__(username, password, role)
        self.student_id = student_id
        self.canteen_card_balance = float(canteen_card_balance)
        self.wallet_password = wallet_password
        self.cart = Cart()
        self.order_history = []

    def greet_user(self):
        """Override greeting method - Polymorphism example"""
        print(f"\n{'='*50}")
        print(f"Welcome back, {self.username}!")
        print(f"Student ID: {self.student_id}")
        print(f"Canteen Card Balance: ₹{self.canteen_card_balance:.2f}")
        print(f"{'='*50}")

    def student_menu(self, menu):
        """Main menu for student interactions"""
        while True:
            print("\n=== Student Menu ===")
            print("1. View Menu")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Place Order")
            print("5. View Order History")
            print("6. Check Wallet Balance")
            print("7. Logout")
            print("="*20)

            try:
                choice = input("Enter your choice (1-7): ")
                
                if choice == "1":
                    self.browse_menu(menu)
                elif choice == "2":
                    self.add_items_to_cart(menu)
                elif choice == "3":
                    self.view_cart()
                elif choice == "4":
                    self.process_order()
                elif choice == "5":
                    self.view_order_history()
                elif choice == "6":
                    self.check_wallet_balance()
                elif choice == "7":
                    print("\nLogging out. Thank you for using the canteen system!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def browse_menu(self, menu):
        print("\n=== Available Menu Items ===")
        if not menu.food_items:
            print("No items available in menu")
            return
            
        for item in menu.food_items:
            status = "✓ Available" if item.availability else "✗ Unavailable"
            print(f"\nID: {item.item_id}")
            print(f"Item: {item.name}")
            print(f"Description: {item.description}")
            print(f"Price: ₹{item.price:.2f}")
            print(f"Status: {status}")
            print("-" * 30)

    def add_items_to_cart(self, menu):
        self.browse_menu(menu)
        try:
            item_id = int(input("\nEnter Item ID to add to cart (0 to cancel): "))
            if item_id == 0:
                return
                
            selected_item = None
            for item in menu.food_items:
                if item.item_id == item_id:
                    selected_item = item
                    break
                    
            if not selected_item:
                print("Item not found")
                return
                
            if not selected_item.availability:
                print("This item is currently unavailable")
                return
                
            while True:
                try:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Quantity must be greater than 0")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number")
            
            self.cart.add_item(selected_item, quantity)
            print(f"\nSuccess! Added {quantity}x {selected_item.name} to cart")
            
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"Error adding to cart: {e}")

    def view_cart(self):
        if not self.cart.cart_items:
            print("\nYour cart is empty!")
            return
            
        print("\n=== Your Cart ===")
        for item, quantity in self.cart.cart_items:
            print(f"{quantity}x {item.name:<20} ₹{item.price:.2f} each")
            print(f"Subtotal: ₹{item.price * quantity:.2f}")
            print("-" * 30)
        print(f"Total: ₹{self.cart.total_price:.2f}")

    def process_order(self):
        if not self.cart.cart_items:
            print("\nYour cart is empty!")
            return
            
        self.view_cart()
        print("\n=== Payment Options ===")
        print("1. Canteen Card")
        print("2. Wallet")
        print("3. Cash")
        print("4. Cancel")
        
        try:
            choice = input("Choose payment method (1-4): ")
            
            if choice == "1":
                if self.cart.total_price > self.canteen_card_balance:
                    print("Insufficient balance in canteen card")
                    return
                self.canteen_card_balance -= self.cart.total_price
                self.complete_order("canteen_card")
                
            elif choice == "2":
                # Load wallet balance
                wallet_balance = 0
                try:
                    with open(wallet_file, 'r') as f:
                        for line in f:
                            sid, balance = line.strip().split('|')
                            if sid == self.student_id:
                                wallet_balance = float(balance)
                                break
                except FileNotFoundError:
                    print("Wallet not found")
                    return
                
                if wallet_balance < self.cart.total_price:
                    print("Insufficient wallet balance")
                    return
                    
                wallet_pwd = input("Enter wallet password: ")
                if wallet_pwd != self.wallet_password:
                    print("Invalid wallet password")
                    return
                
                # Update wallet balance
                with open(wallet_file, 'r') as f:
                    lines = f.readlines()
                with open(wallet_file, 'w') as f:
                    for line in lines:
                        sid, balance = line.strip().split('|')
                        if sid == self.student_id:
                            f.write(f"{sid}|{float(balance) - self.cart.total_price}\n")
                        else:
                            f.write(line)
                
                self.complete_order("wallet")
                
            elif choice == "3":
                self.complete_order("cash")
                
            elif choice == "4":
                print("Order cancelled")
                return
                
            else:
                print("Invalid choice")
                
        except Exception as e:
            print(f"Error processing order: {e}")

    def complete_order(self, payment_method):
        order = Order(self, self.cart.cart_items, self.cart.total_price)
        print(f"\nOrder placed successfully using {payment_method}!")
        if payment_method == "canteen_card":
            print(f"Remaining canteen card balance: ₹{self.canteen_card_balance:.2f}")
        self.cart.clear_cart()

    def view_order_history(self):
        try:
            print("\n=== Order History ===")
            found = False
            with open(bill_history_file, 'r') as f:
                for line in f:
                    sid, items, total = line.strip().split('|')
                    if sid == self.student_id:
                        found = True
                        print(f"\nItems: {items}")
                        print(f"Total: ₹{float(total):.2f}")
                        print("-" * 30)
            
            if not found:
                print("No order history found")
                
        except FileNotFoundError:
            print("No order history found")
        except Exception as e:
            print(f"Error viewing order history: {e}")

    def check_wallet_balance(self):
        try:
            with open(wallet_file, 'r') as f:
                for line in f:
                    sid, balance = line.strip().split('|')
                    if sid == self.student_id:
                        print(f"\nWallet Balance: ₹{float(balance):.2f}")
                        return
            print("Wallet not found")
        except FileNotFoundError:
            print("Wallet system is not available")
        except Exception as e:
            print(f"Error checking wallet balance: {e}")

# Admin class
# [Previous imports and class definitions remain the same until Admin class]

class Admin(User):
    def __init__(self, username, password, role, canteen_name):
        super().__init__(username, password, role)
        self.canteen_name = canteen_name

    def greet_user(self):
        """Override greeting method - Polymorphism example"""
        print(f"\n{'='*50}")
        print(f"Welcome Admin {self.username}")
        print(f"Managing: {self.canteen_name}")
        print(f"{'='*50}")

    def manage_menu(self, menu):
        while True:
            print("\n=== Admin Menu ===")
            print("1. Add new item")
            print("2. Show menu items")
            print("3. Update price")
            print("4. Remove item")
            print("5. Update student wallet")
            print("6. Exit")
            print("="*20)

            try:
                choice = input("Enter your choice (1-6): ")
                if choice == "1":
                    self.add_menu_item(menu)
                elif choice == "2":
                    self.show_menu_items(menu)
                elif choice == "3":
                    self.update_price(menu)
                elif choice == "4":
                    self.remove_item(menu)
                elif choice == "5":
                    self.update_wallet_balance()
                elif choice == "6":
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def add_menu_item(self, menu):
        """Add a new item to the menu"""
        try:
            print("\n=== Add New Menu Item ===")
            # Get the next available ID
            item_id = max([item.item_id for item in menu.food_items], default=0) + 1
            
            name = input("Enter Item Name: ").strip()
            description = input("Enter Description: ").strip()
            while True:
                try:
                    price = float(input("Enter Price: "))
                    if price <= 0:
                        print("Price must be greater than 0")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number for price")

            food_item = FoodItem(item_id, name, description, price, True)
            menu.food_items.append(food_item)
            menu.save_menu()
            print(f"\nSuccess! {name} added to the menu with ID {item_id}")
        except Exception as e:
            print(f"Error adding menu item: {e}")

    def show_menu_items(self, menu):
        """Display all menu items"""
        print("\n=== Current Menu Items ===")
        if not menu.food_items:
            print("No items in menu")
            return
            
        for item in menu.food_items:
            status = "✓ Available" if item.availability else "✗ Unavailable"
            print(f"ID: {item.item_id}")
            print(f"Name: {item.name}")
            print(f"Description: {item.description}")
            print(f"Price: ₹{item.price:.2f}")
            print(f"Status: {status}")
            print("-" * 30)

    def update_price(self, menu):
        """Update the price of a menu item"""
        try:
            self.show_menu_items(menu)
            item_id = int(input("\nEnter the Item ID to update price: "))
            
            for item in menu.food_items:
                if item.item_id == item_id:
                    current_price = item.price
                    while True:
                        try:
                            new_price = float(input(f"Enter new price (current: ₹{current_price:.2f}): "))
                            if new_price <= 0:
                                print("Price must be greater than 0")
                                continue
                            break
                        except ValueError:
                            print("Please enter a valid number for price")
                    
                    item.price = new_price
                    menu.save_menu()
                    print(f"\nSuccess! Price of {item.name} updated from ₹{current_price:.2f} to ₹{new_price:.2f}")
                    return
                    
            print("Item not found")
        except ValueError:
            print("Please enter a valid number for Item ID")
        except Exception as e:
            print(f"Error updating price: {e}")

    def remove_item(self, menu):
        """Remove an item from the menu"""
        try:
            self.show_menu_items(menu)
            item_id = int(input("\nEnter the Item ID to remove: "))
            
            original_length = len(menu.food_items)
            menu.food_items = [item for item in menu.food_items if item.item_id != item_id]
            
            if len(menu.food_items) < original_length:
                menu.save_menu()
                print(f"Success! Item {item_id} removed from the menu")
            else:
                print("Item not found")
                
        except ValueError:
            print("Please enter a valid number for Item ID")
        except Exception as e:
            print(f"Error removing item: {e}")

    def update_wallet_balance(self):
        """Update student wallet balance"""
        try:
            student_id = input("Enter student ID: ").strip()
            
            # Load current wallet data
            wallet_data = {}
            try:
                with open(wallet_file, 'r') as f:
                    for line in f:
                        sid, balance = line.strip().split('|')
                        wallet_data[sid] = float(balance)
            except FileNotFoundError:
                print("Wallet file not found. Creating new file.")
            
            if student_id not in wallet_data:
                create_new = input("Student not found. Create new wallet? (y/n): ").lower()
                if create_new != 'y':
                    return
                wallet_data[student_id] = 0
            
            current_balance = wallet_data[student_id]
            print(f"Current balance: ₹{current_balance:.2f}")
            
            action = input("Do you want to add or subtract balance? (add/sub): ").lower()
            if action not in ['add', 'sub']:
                print("Invalid action")
                return
                
            while True:
                try:
                    amount = float(input("Enter amount: "))
                    if amount <= 0:
                        print("Amount must be greater than 0")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number")
            
            if action == 'add':
                wallet_data[student_id] += amount
                print(f"Added ₹{amount:.2f}")
            else:
                if amount > wallet_data[student_id]:
                    print("Insufficient balance")
                    return
                wallet_data[student_id] -= amount
                print(f"Subtracted ₹{amount:.2f}")
            
            # Save updated wallet data
            with open(wallet_file, 'w') as f:
                for sid, balance in wallet_data.items():
                    f.write(f"{sid}|{balance}\n")
            
            print(f"New balance: ₹{wallet_data[student_id]:.2f}")
            
        except Exception as e:
            print(f"Error updating wallet: {e}")

# [Rest of the code remains the samen


# Other classes remain the same...
class FoodItem:
    def __init__(self, item_id, name, description, price, availability=True):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = float(price)
        self.availability = availability == True or availability == "True"

class Menu:
    def __init__(self):
        self.food_items = []
        self.load_menu()

    def load_menu(self):
        """Load menu items from file"""
        try:
            with open(os.path.join(BASE_DIR, 'food_items.txt'), 'r') as f:
                for line in f:
                    item_id, name, desc, price, avail = line.strip().split('|')
                    self.food_items.append(FoodItem(int(item_id), name, desc, float(price), avail))
        except FileNotFoundError:
            print("Menu file not found. Starting with empty menu.")
        except Exception as e:
            print(f"Error loading menu: {e}")

    def save_menu(self):
        """Save menu items to file"""
        try:
            with open(os.path.join(BASE_DIR, 'food_items.txt'), 'w') as f:
                for item in self.food_items:
                    f.write(f"{item.item_id}|{item.name}|{item.description}|{item.price}|{item.availability}\n")
        except Exception as e:
            print(f"Error saving menu: {e}")

class Order:
    def __init__(self, student, order_items, total_price):
        self.student = student
        self.order_items = order_items
        self.total_price = total_price
        self.save_order()

    def save_order(self):
        """Save order to bill history"""
        try:
            with open(bill_history_file, 'a') as f:
                items_str = '; '.join([f"{item[1]}x {item[0].name}" for item in self.order_items])
                f.write(f"{self.student.student_id}|{items_str}|{self.total_price}\n")
        except Exception as e:
            print(f"Error saving order: {e}")

class Cart:
    def __init__(self):
        self.cart_items = []
        self.total_price = 0

    def add_item(self, food_item, quantity):
        self.cart_items.append((food_item, quantity))
        self.total_price += food_item.price * quantity

    def clear_cart(self):
        self.cart_items = []
        self.total_price = 0

def main():
    """Main function to run the canteen management system"""
    setup_files()
    menu = Menu()
    
    while True:
        print("\n=== Canteen Management System ===")
        print("1. Login")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            
            try:
                # Read users from file
                with open(users_file, 'r') as f:
                    for line in f:
                        user_data = line.strip().split('|')
                        if user_data[0] == username:
                            if user_data[1] == password:
                                if user_data[2] == 'admin':
                                    admin = Admin(username, password, 'admin', user_data[3])
                                    admin.greet_user()
                                    admin.manage_menu(menu)
                                else:
                                    student = Student(username, password, 'student', 
                                                    user_data[3], user_data[4], user_data[5])
                                    student.greet_user()
                                    student.student_menu(menu)
                                break
                            else:
                                raise InvalidPasswordException()
                    else:
                        raise UserNotFoundException()
                        
            except (InvalidPasswordException, UserNotFoundException) as e:
                print(e)
            except Exception as e:
                print(f"An error occurred: {e}")
                
        elif choice == "2":
            print("Thank you for using the Canteen Management System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()