import pandas as pd
import numpy as np
from datetime import date

def mortgage_monthly_payment_breakdown(
    individual_mortgage_dictionary
):
    """
    Function Calculates Mortage monthly payments, breaking the value down
    into interest payment and capital payment for an n number of years of the
    mortgages lifespan, and according to a particular interest rate.

    :param interest_rate:
    :param payments_a_year:
    :param mortgage_lifespan:
    :param mortgage_value:
    :return:
    """
    monthly_breakdown_dict = {}
    # Monthly Total Payment
    monthly_breakdown_dict["Monthly_Payment"] = -1 * np.pmt(
        individual_mortgage_dictionary["Interest_Rate"]/individual_mortgage_dictionary["Payments_a_year"],
        individual_mortgage_dictionary["Mortgage_lifespan"]*individual_mortgage_dictionary["Payments_a_year"],
        individual_mortgage_dictionary["Mortgage_value"]
    )
    # Interest Payment
    monthly_breakdown_dict["Interest_Payment"] = -1 * np.ipmt(
        individual_mortgage_dictionary["Interest_Rate"] / individual_mortgage_dictionary["Payments_a_year"],
        1,
        individual_mortgage_dictionary["Mortgage_lifespan"]*individual_mortgage_dictionary["Payments_a_year"],
        individual_mortgage_dictionary["Mortgage_value"]
    )
    # Principal Payment
    monthly_breakdown_dict["Principal_Payment"] = -1 * np.ppmt(
        individual_mortgage_dictionary["Interest_Rate"] / individual_mortgage_dictionary["Payments_a_year"],
        1,
        individual_mortgage_dictionary["Mortgage_lifespan"]*individual_mortgage_dictionary["Payments_a_year"],
        individual_mortgage_dictionary["Mortgage_value"]
    )

    # Returning Introduced Information
    monthly_breakdown_dict["Interest_Rate"] = individual_mortgage_dictionary["Interest_Rate"]
    monthly_breakdown_dict["Payments_a_year"] = individual_mortgage_dictionary["Payments_a_year"]
    monthly_breakdown_dict["Mortgage_lifespan"] = individual_mortgage_dictionary["Mortgage_lifespan"]
    monthly_breakdown_dict["Mortgage_value"] = individual_mortgage_dictionary["Mortgage_value"]

    return monthly_breakdown_dict


def create_base_mortgage_table(
    desired_start_date ,
    monthly_breakdown_dict,
    date_range_name: str,
    column_list
):
    """
    Creates an empty base dataframe, with a column
    detailing the payment dates based on an starting mortgage payment date
    and iterating over monthlypayments a year times the amunt of years the
    mortgage will be  alive.

    :param start_year:
    :param start_month:
    :param start_date:
    :param payements_a_year:
    :param mortgage_lifespan:
    :param date_range_name:
    :return:

    """

    # Creating the Data Range Column
    start_date = date(
        int(desired_start_date.split("/")[2]),
        int(desired_start_date.split("/")[1]),
        int(desired_start_date.split("/")[0])
    )
    rng = pd.date_range(
        start_date,
        periods=monthly_breakdown_dict["Mortgage_lifespan"] * monthly_breakdown_dict["Payments_a_year"],
        freq='MS'
    )
    # Create Empty Dataframe
    rng.name = date_range_name
    df = pd.DataFrame(
        index=rng, # the date range created
        columns= column_list,
        dtype='float'
    )
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "Period"
    return df


def populate_base_mortgage_table(
        monthly_breakdown_dict,
        mortgage_base_table,
):
    """
    Function populates the empy columns in a base mortgage equation in order with Monthly Paymenet,
    Interestes Paid at period x, principal paid at period x and the ending balance (or pending balance)
    at that particular perdiod.

    :param monthly_breakdown_dict: the dictionary with all the mortgage informaiton
    :param mortgage_base_table:
    :return:
    """
    # Populating table with Formulas
    mortgage_base_table["Monthly_Payment"] = monthly_breakdown_dict["Monthly_Payment"]

    mortgage_base_table["Interests_Paid"] = -1 * np.ipmt(
        monthly_breakdown_dict["Interest_Rate"]/monthly_breakdown_dict["Payments_a_year"],
        mortgage_base_table.index,
        monthly_breakdown_dict["Mortgage_lifespan"] * monthly_breakdown_dict["Payments_a_year"],
        monthly_breakdown_dict["Mortgage_value"]
    )
    mortgage_base_table["Principal_Paid"] = -1 * np.ppmt(
        monthly_breakdown_dict["Interest_Rate"] / monthly_breakdown_dict["Payments_a_year"],
        mortgage_base_table.index,
        monthly_breakdown_dict["Mortgage_lifespan"] * monthly_breakdown_dict["Payments_a_year"],
        monthly_breakdown_dict["Mortgage_value"]

    )
    return mortgage_base_table

