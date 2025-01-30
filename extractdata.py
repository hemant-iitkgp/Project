import pandas as pd

def extract_values(file_path, subdistrict_columns, column_name, parameter_name):
    """
    Extracts values for specified parameters from the CSV file.
    
    Parameters:
        file_path (str): The path to the CSV file.
        subdistrict_columns (list): The list of subdistrict column names.
        column_name (str): The name of the column to filter parameters (e.g., 'Parameters').
        parameter_name (str): The parameter to extract values for.
    
    Returns:
        list: A list of values for the specified parameter in the order of subdistrict columns.
    """
    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return []

    # Filter rows where the specified column matches the parameter name
    filtered_row = df[df[column_name] == parameter_name]
    
    # Extract values for the subdistrict columns
    if not filtered_row.empty:
        result = filtered_row[subdistrict_columns].values.flatten().tolist()
        return result
    else:
        print(f"No data found for parameter '{parameter_name}' in column '{column_name}'")
        return []
    

def extract_variables(content):
    """
    Extracts variables from a section of text.
    
    Parameters:
        content (str): The text content of a section
        
    Returns:
        tuple: (heading, dependent_vars, control_vars)
    """
    dependent_vars = []
    control_vars = []
    heading = None
    
    # Split content into lines
    lines = content.split('\n')
    
    dep_section = False
    ctrl_section = False
    
    for line in lines:
        line = line.strip()
        
        # Capture heading (first non-empty line)
        if heading is None and line:
            heading = line
            continue
            
        # Toggle sections based on keywords
        if line.startswith("Dependent variables:"):
            dep_section = True
            ctrl_section = False
            continue
        elif line.startswith("Control vriables:"):
            dep_section = False
            ctrl_section = True
            continue
        elif line.startswith("-") or not line:
            # Skip divider lines or empty lines
            continue
            
        # Append variables to respective lists
        if dep_section and line:
            dependent_vars.append(line)
        elif ctrl_section and line:
            control_vars.append(line)
            
    return heading, dependent_vars, control_vars