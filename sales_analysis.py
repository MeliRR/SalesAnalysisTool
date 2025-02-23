
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load sales data from a CSV file
def load_sales_data(file_path):
    """
    This function loads the sales data from the specified CSV file.
    
    Args:
    file_path (str): The path to the CSV file containing the sales data.
    
    Returns:
    pd.DataFrame: The loaded sales data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)  # Reads the CSV file
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Function to clean the data
def clean_data(data):
    """
    Cleans the sales data by handling missing values and ensuring correct data types.
    
    Args:
    data (pd.DataFrame): The raw sales data.
    
    Returns:
    pd.DataFrame: The cleaned sales data.
    """
    # Drop rows with missing values
    data.dropna(inplace=True)
    
    # Convert 'Date' to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    
    # Ensure 'Quantity Sold' and 'Sale Price' are numeric
    data['Quantity Sold'] = pd.to_numeric(data['Quantity Sold'], errors='coerce')
    data['Sale Price'] = pd.to_numeric(data['Sale Price'], errors='coerce')
    
    # Calculate the 'Total Sale' if it's not already provided
    if 'Total Sale' not in data.columns:
        data['Total Sale'] = data['Quantity Sold'] * data['Sale Price']
    
    # Drop rows with invalid data (after coercion)
    data.dropna(inplace=True)
    
    return data

# Function to analyze basic sales metrics
def basic_analysis(data):
    """
    Analyzes basic sales metrics like total sales, average sales, and top products.
    
    Args:
    data (pd.DataFrame): The cleaned sales data.
    
    Returns:
    tuple: A tuple containing total sales, average sales, and top products.
    """
    # Total sales (sum of 'Total Sale')
    total_sales = data['Total Sale'].sum()

    # Average sale
    avg_sales = data['Total Sale'].mean()

    # Top products by total sales
    top_products = data.groupby('Product Name')['Total Sale'].sum().sort_values(ascending=False).head(10)

    return total_sales, avg_sales, top_products

# Function to plot a bar chart for top products
def plot_top_products(top_products):
    """
    Plots a bar chart for the top-selling products.
    
    Args:
    top_products (pd.Series): The top products by total sales.
    """
    top_products.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title("Top 10 Products by Sales")
    plt.xlabel("Product Name")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to plot a line graph for sales trends over time
def plot_sales_trends(data):
    """
    Plots a line graph for sales trends over time (monthly).
    
    Args:
    data (pd.DataFrame): The cleaned sales data.
    """
    # Group by month and sum the sales
    data['Month'] = data['Date'].dt.to_period('M')
    monthly_sales = data.groupby('Month')['Total Sale'].sum()

    monthly_sales.plot(kind='line', figsize=(10, 6), color='green')
    plt.title("Sales Trends Over Time")
    plt.xlabel("Month")
    plt.ylabel("Total Sales ($)")
    plt.tight_layout()
    plt.show()

# Main function to execute the program
def main():
    """
    The main function that drives the program, allowing the user to load and analyze sales data.
    """
    # Prompt user to input the path to the sales data CSV file
    file_path = input("Enter the path to the sales data CSV file: ")

    # Load the sales data from the provided file path
    data = load_sales_data(file_path)
    
    if data is not None:
        # Clean the data
        data = clean_data(data)

        # Perform basic analysis on the cleaned data
        total_sales, avg_sales, top_products = basic_analysis(data)

        # Print the basic analysis results
        print(f"Total Sales: ${total_sales:,.2f}")
        print(f"Average Sales per Transaction: ${avg_sales:,.2f}")
        print("Top 10 Products by Sales:")
        print(top_products)

        # Plot the top products bar chart
        plot_top_products(top_products)

        # Plot the sales trends over time
        plot_sales_trends(data)
    else:
        print("Failed to load the data. Please check the file format and try again.")

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
