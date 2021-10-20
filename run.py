import gspread
from google.oauth2.service_account import Credentials
import os

proxy = "127.0.0.1:41091"

os.environ["http_proxy"] = proxy
os.environ["HTTP_PROXY"] = proxy
os.environ["https_proxy"] = proxy
os.environ["HTTPS_PROXY"] = proxy


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

    
def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        list(map(int, values))
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


    
def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet.
    Updates the relevant worksheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet.capitalize()} worksheet updated successfully.\n")       

    
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = list(map(int, stock[-1]))
    surplus_data = []
    for sale_num, stock_num in zip(sales_row, stock_row):
        surplus_data.append(stock_num - sale_num)
   
    return surplus_data    

def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = list(map(int, data))
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    
if __name__ == '__main__':
    print("Welcome to Love Sandwiches Data Automation\n")
    main()