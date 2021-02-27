# Financial Planning 

This repository contains a mortgage calculator, along with other Financial Planning pipelines and utilities. 
Up to this point the repo contains a mortgage pipeline, but I will soon be including a salary calculator (relevant to Panamanian legislation and taxes). 

## Repositoy Structure: 
- Source ( where all the calculators and reporting pipelines will be placed, under their own relevant directory)
- Data ( which will hold output and primary tables
    - Primary tables will be tables which will be used to feed the calculators and reporting pipelines 
    - **Output** tables will be the result of the code's calculations. 

# Howt to Use & Available Utilities and Calculators (February 27 February 2020): 
### Unsure of which mortgage loan is best? 

Let us say Bank 1 is offering a 3.8% interest rate, for a 100,000 dollar mortgage over a period of 30 years. 
- How much will you pay monthly? 
- How much will I end up paying to the bank in the next 30 years?
- How much is the principal payment ? and How much is interest payment? 

Worry no more, just write down the banks information data in the excel/csv file of your desire and change the pipeline path. The pipeline will give you a calculation for each option, bank and variation. 

### What's inside? 
1. Inside the the directory **mortgages**, you will find a: 
      - Pipeline that calculates mortgage payments variations for an N number of desired Banks/Opportunities across the mortgages lifespan. 
      - Within the **primary_data** repository, write down the Banks, the offered Interest Rates, the lifespans and Downpayment Percents for your planning. 
      - The pipeline once run, will yield a series of csv files within the *output_data/mortgage_calculations* path with the mortgage payment breakdown for each input Bank. 
2.  A Mortgage payment utils file, which can be used individually to calculate mortgage payments based on the above information, but don't create the whole table. 
  
 
    
