from src.mortgages.mortgage_utils import *
import pandas as pd
from datetime import date
import os

today = date.today()
DESIRED_START_DATE = today.strftime("%d/%m/%Y")
TABLE_PATH = "data/primary_data/master_mortgage_info_table.csv" # change this path to whatever you want if you do not want to use the given CSV structure, 
                                                                # make sure to have the same table structure *** for your file, along with column names 

def generate_required_columns():
    """
    Generated desired columns for Dataframe **
    This is a function for general control of the remaining ones
    :return:
    """
    columns_for_output_dataframe = [
        "Monthly_Payment",
        "Interests_Paid",
        "Principal_Paid",
    ]
    return columns_for_output_dataframe

def create_bank_mortgage_info_dict(
    info_table
):
    """
    Functions returns a dictionary with banks names as keys
    and dataframe objects storred within a dictionary. The function iterates over
    the rows in a dataframe, which assumes the first elements in the dataframe is Bank*
    :param info_table:
    :return: a dictionary with meta information from each row.
    """
    master_dict = {}
    column_list = list(info_table.columns)
    # ToDo: Make the function look for the column position index "Bank" so it walwas  takes "Bank"
    for index, row in info_table.iterrows():
        master_dict[row[0]] = {} # making banks names dictionary keys
        for column in column_list:
            master_dict[row[0]][column] = row[column_list.index(column)]
    return master_dict

def create_multiple_mortgage_tables(
        info_table_path
):
    
    """
    The function iterates over the CSV file, making each Bank a Key withina  repository. 
    For each bank a backbone empty table is created with the desired periods, 
    and then it is populated with a mortgage monthly, interest and principal payment calculator. 
    
    The pipeline outputs a series of tables (in csv format) with all the mortgage calculations 
    for each inputed bank, and the csv files are saved with the information name of said bank. 
    """
    info_table = pd.read_csv(info_table_path)
    info_table["Bank "] = info_table["Bank "].str.replace(' ', '_')
    master_dictionary = create_bank_mortgage_info_dict(info_table)
    for item in master_dictionary.keys():
        monthly_breakdown_dict = mortgage_monthly_payment_breakdown(
            master_dictionary[item]
        )
        mortgage_base_table = create_base_mortgage_table(
            DESIRED_START_DATE,
            monthly_breakdown_dict,
            "PERIODS",
            generate_required_columns(),
        )
        populated_break_table = populate_base_mortgage_table(
            monthly_breakdown_dict,
            mortgage_base_table
        )
        populated_break_table = populated_break_table.\
            append(populated_break_table.sum(numeric_only=True), ignore_index=True)
        populated_break_table.iloc[-1,0] = "Running Total" # creating a running total element at the end
        # Creating Output File
        output_path = os.path.join(
            "data",
            "output_data",
            "mortgage_calculations",
            item,
        )
        os.makedirs(output_path, exist_ok = True)
        filename = os.path.join(output_path,f"mortgage_with_{item}_breakdown.csv")
        populated_break_table.to_csv(filename)

    return populated_break_table


# Run Calculations for Mortgages
create_multiple_mortgage_tables(TABLE_PATH)
