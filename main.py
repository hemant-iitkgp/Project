import pandas as pd
import extractdata
import samplearchive1
import Tertile
import os
import re

def process_section(heading, dependent_vars, control_vars, datafile, subdistrict_columns, column_name):
    # Extract values for control and dependent variables
    control_val = {var: extractdata.extract_values(datafile, subdistrict_columns, column_name, var) 
                  for var in control_vars}
    dependent_val = {var: extractdata.extract_values(datafile, subdistrict_columns, column_name, var) 
                    for var in dependent_vars}
    
    # Load tertile statistics
    folder_statistics = Tertile.folder_statistics
    tertile_results = Tertile.tertile_results

    # Initialize lists for variables
    Transportation = [0] * 12
    Nature = [0] * 12
    Poverty = [0] * 12
    Transportation_tertile = [0] * 12
    Nature_tertile = [0] * 12
    Poverty_tertile = [0] * 12

    independent_vars = ['Transportation', 'Nature', 'Poverty']

    # Extract tertile statistics
    for index, subdistrict in enumerate(subdistrict_columns):
        Transportation[index] = folder_statistics[subdistrict]['Transportation']
        Nature[index] = folder_statistics[subdistrict]['Nature']
        Poverty[index] = folder_statistics[subdistrict]['Poverty']

    # Assign tertile values
    for tertile_type, tertile_list in [('Transportation', Transportation_tertile), 
                                      ('Nature', Nature_tertile), 
                                      ('Poverty', Poverty_tertile)]:
        for level, value in [('highest', 3), ('medium', 2), ('lowest', 1)]:
            for subdistrict in tertile_results[tertile_type][level][0]:
                tertile_list[subdistrict_columns.index(subdistrict)] = value

    # Create DataFrame
    data = pd.DataFrame({
        'subdistrict': subdistrict_columns,
        'Transportation': Transportation,
        'Nature': Nature,
        'Poverty': Poverty,
        'Transportation_tertile': Transportation_tertile,
        'Nature_tertile': Nature_tertile,
        'Poverty_tertile': Poverty_tertile
    })

    # Add control variables to DataFrame
    for var in control_vars:
        data[var] = control_val[var]

    results_dict = {}  # Store results for all dependent variables

    # Iterate through dependent variables and run analysis
    for var in dependent_vars:
        data['health_outcome'] = dependent_val[var]
        result = samplearchive1.run_health_analysis(data, 'health_outcome', independent_vars, control_vars)
        results_dict[var] = result
        
    return results_dict

if __name__ == "__main__":
    variable_file = 'variables.txt'
    datafile = 'cleaned_output.csv'
    column_name = 'Parameters'
    result_file = "result.csv"
    
    # Create folder for results if it doesn't exist
    results_folder = "results"
    os.makedirs(results_folder, exist_ok=True)

    subdistrict_columns = [
        'SubDistrict-Chhanve', 'SubDistrict-City', 'SubDistrict-Hallia', 'SubDistrict-Jamalpur',
        'SubDistrict-Kone', 'SubDistrict-Lalganj', 'SubDistrict-Manjhwan', 'SubDistrict-Marihan Patehara',
        'SubDistrict-Naraynpur', 'SubDistrict-Pahadi', 'SubDistrict-Rajgarh', 'SubDistrict-Sikhar'
    ]
    
    # Read all sections from the file
    with open(variable_file, 'r') as file:
        content = file.read()
    
    # Split content into sections using ===============
    sections = content.split('===============================================================')
    
    # Remove any empty sections
    sections = [section.strip() for section in sections if section.strip()]
    
    # Process each section
    file_exists = os.path.exists(result_file)
    
    for section in sections:
        # Extract variables for this section
        heading, dependent_vars, control_vars = extractdata.extract_variables(section)
        
        print(f"\nProcessing section: {heading}")
        
        # Process the section and get results
        results_dict = process_section(heading, dependent_vars, control_vars, 
                                    datafile, subdistrict_columns, column_name)
        
        # Write results to file
        with open(result_file, 'a') as file:
            file.write(f"\n{heading}\n\n")
            for key, value in results_dict.items():
                file.write(f"\n{key}\n")
                file.write('Serial No.,Independent Variable,Tertile,Prevalence_Difference,CI_Lower,CI_Upper,P_Value\n')
                pd.DataFrame(value).to_csv(file, mode='a', header=not file_exists)
                file_exists = True
        
        print(f"Completed processing section: {heading}")