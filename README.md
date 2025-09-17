# Personal Finance Tracker

A simple web-based personal finance tracking application built with HTML, CSS, JavaScript, and Python Flask.

## Features

- **Dashboard**: Overview of your financial status with total balance, recent transactions, and spending by category
- **Transaction Management**: Add, view, and categorize income, expenses, savings, and investments
- **Budget Planning**: Set budgets for different categories and track spending against them
- **Account Management**: Manage multiple accounts (bank, mobile money, cash, etc.)
- **Income Allocation**: Built-in 50/20/20/10 rule calculator for budgeting

## Installation

1. Make sure you have Python installed on your system
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Navigate to the project directory
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open your web browser and go to `http://localhost:5000`

## Usage

### Getting Started
1. **Add Accounts**: Start by adding your bank accounts, mobile money accounts, and cash
2. **Set Up Categories**: The app comes with default categories, but you can add more if needed
3. **Add Transactions**: Record your income, expenses, savings, and investments
4. **Create Budgets**: Set monthly budgets for different spending categories
5. **Monitor Progress**: Use the dashboard to track your financial health

### Key Features

#### Dashboard
- View total balance across all accounts
- See recent transactions at a glance
- Monitor monthly spending by category
- Quick action buttons to add transactions

#### Transactions
- Add income, expenses, savings, and investments
- Categorize transactions for better tracking
- Filter transactions by type, category, or account
- View transaction history in a clean table format

#### Budget Planning
- Set budgets for different categories
- Track spending against budgets
- Use the income allocation planner (50/20/20/10 rule)
- Visual progress bars for budget tracking

#### Account Management
- Add multiple accounts (bank, mobile money, cash, etc.)
- View account balances and types
- Edit or delete accounts as needed
- Account summary with totals by type

## Database

The application uses SQLite database (`finance.db`) which will be created automatically when you first run the app. The database includes tables for:
- Accounts
- Categories
- Transactions
- Budgets

## Future Enhancements

- Integration with actual bank APIs and mobile money services
- Data export/import functionality
- Advanced reporting and analytics
- Mobile app version
- Multi-user support with authentication

## Contributing

Feel free to fork this project and submit pull requests for any improvements!
