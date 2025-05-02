# Canteen Management System

A comprehensive Python-based system designed to streamline food ordering and management processes within educational institutions. This system provides separate interfaces for students and administrators, offering features like digital wallet integration, food ordering, and inventory management.

## Features

### For Students
- **User Registration & Authentication**: Secure login system for students
- **Browse Menu**: View available food items with descriptions and prices
- **Cart Management**: Add items to cart, adjust quantities, and place orders
- **Multiple Payment Options**: 
  - Digital wallet (requires wallet password)
  - Cash payment with queue number system
- **Order History**: Track past orders and expenditures
- **Wallet Management**: Check wallet balance

### For Administrators
- **Menu Management**: Add, update, or remove food items
- **Price Management**: Update prices as needed
- **Student Wallet Management**: Add or subtract funds from student wallets

## System Architecture

The system follows object-oriented design principles with classes including:

- `User`: Base class with common user attributes
- `Student`: Extended user class with student-specific functionality
- `Admin`: Extended user class with administrative privileges
- `FoodItem`: Manages food item details
- `Menu`: Handles the collection of food items
- `Cart`: Manages the shopping cart experience
- `Order`: Processes and records orders

## File Structure

The system relies on several text files for data persistence:

- `users.txt`: Stores user credentials and roles
- `students.txt`: Contains student-specific details including wallet passwords
- `wallet.txt`: Maintains wallet balances for each student
- `food_items.txt`: Stores the menu items with prices and availability
- `bill_history.txt`: Records all transactions and order details

## Installation and Setup

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/your-username/canteen-management-system.git
   ```

2. Navigate to the project directory:
   ```
   cd canteen-management-system
   ```

3. Update the `BASE_DIR` in the script to your project location:
   ```python
   BASE_DIR = "/path/to/your/project/directory"
   ```

4. Run the application:
   ```
   python foodcanteenupdated.py
   ```

## Usage Instructions

### Student Workflow
1. Register a new account or log in with existing credentials
2. Browse the available menu items
3. Add desired items to your cart
4. Place an order using wallet or cash payment
   - For wallet payment: Enter your wallet password
   - For cash payment: Note the generated queue number and present it at the canteen counter

### Administrator Workflow
1. Log in with admin credentials
2. Manage menu items (add/remove/update)
3. Update student wallet balances as needed

## Payment System

### Wallet Payment
- Students must have sufficient balance in their digital wallet
- Transactions require wallet password verification
- Balance is automatically deducted upon successful order placement

### Cash Payment
- System generates a unique 4-digit queue number
- Students present the queue number at the counter
- Payment is made in person and food is collected at the counter

## Dependencies
- Python 3.6+
- Standard Python libraries (os, random)

## Error Handling

The system includes custom exception classes:
- `CanteenException`: Base exception class
- `InsufficientBalanceException`: For wallet payment failures
- `InvalidPasswordException`: For authentication failures
- `UserNotFoundException`: For login attempts with non-existent users
- `UserAlreadyExistsException`: For registration with existing usernames

## Security Features
- Password protection for user accounts
- Separate wallet passwords for financial transactions
- File-based data persistence for all transactions and user data

## Future Enhancements
- Graphical user interface (GUI)
- Enhanced reporting for administrators
- Menu categorization
- Promotions and discounts
- Feedback system for food items
- Notification system for order status updates

## License
This project is licensed under the Apache License 2.0 - see the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) for details.
