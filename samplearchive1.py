import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

def validate_and_convert_numeric(df, columns):
    """
    Validate and convert columns to numeric type
    Returns DataFrame with numeric columns
    """
    for col in columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except Exception as e:
            print(f"Error converting {col}: {str(e)}")
            print(f"Unique values in {col}:", df[col].unique())
    return df

def create_tertiles(df, column):
    """
    Create tertiles for a given column in the dataframe
    Returns the dataframe with a new column containing tertile labels (1,2,3)
    """
    try:
        df[f'{column}_tertile'] = pd.qcut(df[column], q=3, labels=[1,2,3])
    except Exception as e:
        print(f"Error creating tertiles for {column}: {str(e)}")
        print(f"Column values: {df[column].describe()}")
    print(df[column])
    print(df[f'{column}_tertile'])
    return df

def run_health_analysis(data, dependent_var, independent_vars, control_vars=None):
    """
    Run adjusted linear regression for health outcomes by tertiles
    """
    # Convert data to DataFrame if it's not already
    data = pd.DataFrame(data)
    
    # Validate and convert numeric columns
    all_numeric_cols = [dependent_var] + independent_vars
    if control_vars:
        all_numeric_cols.extend(control_vars)
    
    data = validate_and_convert_numeric(data, all_numeric_cols)
    
    # Drop rows with NaN values
    data = data.dropna(subset=all_numeric_cols)
    
    # Print data info for debugging
    print("\nData Info:")
    print(data[all_numeric_cols].info())
    print("\nData Description:")
    print(data[all_numeric_cols].describe())
    
    results = []
    
    for indep_var in independent_vars:
        try:
            # Create tertiles
            # data = create_tertiles(data, indep_var)
            
            # Create dummy variables for tertiles
            tertile_dummies = pd.get_dummies(data[f'{indep_var}_tertile'], 
                                           prefix=f'{indep_var}_tertile')
            tertile_dummies = tertile_dummies.drop(f'{indep_var}_tertile_1', axis=1)
            
            # Prepare regression variables
            X = tertile_dummies.copy()
            if control_vars:
                X = pd.concat([X, data[control_vars]], axis=1)
            X = add_constant(X)
            y = data[dependent_var]
            
            # Ensure all data is numeric
            X = X.astype(float)
            y = y.astype(float)
            
            # Run regression
            model = OLS(y, X).fit(cov_type='HC1')
            
            # Store results
            for tertile in [2, 3]:
                results.append({
                    'Independent_Variable': indep_var,
                    'Tertile': tertile,
                    'Prevalence_Difference': model.params[f'{indep_var}_tertile_{tertile}'],
                    'CI_Lower': model.conf_int()[0][f'{indep_var}_tertile_{tertile}'],
                    'CI_Upper': model.conf_int()[1][f'{indep_var}_tertile_{tertile}'],
                    'P_Value': model.pvalues[f'{indep_var}_tertile_{tertile}']
                })
                
        except Exception as e:
            print(f"Error processing {indep_var}: {str(e)}")
    
    return pd.DataFrame(results)

# Example usage with error handling
# if __name__ == "__main__":
#     try:
#         # Create sample data
#         data = pd.DataFrame({
#             'subdistrict': ['Sub1', 'Sub2', 'Sub3', 'Sub4', 'Sub5','Sub6','Sub7','Sub8','Sub9','Sub10','Sub11','Sub12'],
#             'health_outcome': [-0.400671376,-0.412863478,-0.193155878,-0.299162728,-0.036560988,-0.172060134,-0.386021514,3.154409748,-0.329455094,-0.314641185,-0.208821613,-0.400995761],
#             'transportation_score': [2.50,0.00,5.00,7.50,7.50,10.00,2.50,10.00,10.00,5.00,0.00,0.00],
#             # 'poverty_score': [],
#             # 'nature_score': [],
#             'Pregnant':[-0.375383605,-0.538061318,-0.234436258,-0.228309723,-0.163646795,-0.267026481,-0.271018323,3.157314663,-0.200315688,-0.192864085,-0.274107528,-0.412144858],
#             'first_trimester':[-0.271209468,-0.551955357,-0.383052918,0.049601702,-0.283434373,-0.29630743,-0.182949516,3.137976136,-0.247267701,-0.214572184,-0.254872092,-0.501956801],
#             'JSY':[-0.373985846,-0.538004703,-0.234378692,-0.230292386,-0.163589007,-0.266969017,-0.270960872,3.157382862,-0.200258015,-0.192806389,-0.274050086,-0.412087849],

#         })
        
#         # Define variables
#         dependent_var = 'health_outcome'
#         independent_vars = ['transportation_score']
#         control_vars = ['Pregnant','first_trimester','JSY']
        
#         # Run analysis
#         results = run_health_analysis(data, dependent_var, independent_vars, control_vars)
        
#         # Print results
#         print("\nAnalysis Results:")
#         print(results.round(3))
        
#         # Save results to CSV
#         results.to_csv('regression_results.csv', index=False)
#         print("\nResults saved to regression_results.csv")
        
#     except Exception as e:
#         print(f"Main execution error: {str(e)}")