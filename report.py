import os
import sys
import testcasestruct
import pandas as pd
class report:
    def __init__(self) -> None:
        pass
    # Function to apply color formatting based on the result
    def color_format(val):
        color = 'green' if val == 'Pass' else 'red'
        return f'background-color: {color}'
    
    def process_xlsx(self):
        print(testcasestruct.final_json_result)

        # Create a DataFrame from the JSON results
        data = testcasestruct.final_json_result
        df = pd.DataFrame(data)

        # Remove 'case' from 'ID' and convert to integer for sorting
        df['ID'] = df['ID'].str.replace('case', '').astype(int)

        # Sort the DataFrame by 'ID' column to ensure order
        df.sort_values(by='ID', inplace=True)

        # Convert 'ID' back to string with 'case' prefix for display
        df['ID'] = 'case' + df['ID'].astype(str)

        # Determine overall result for each case
        def overall_result(row):
            if 'Fail' in row.values:
                return 'Fail'
            return 'Pass'

        # Apply the function to each row and create a new column 'Overall Result'
        df['Overall Result'] = df.apply(overall_result, axis=1)

        # Create an Excel file using ExcelWriter
        with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
            # Write the DataFrame to the Excel file
            df.to_excel(writer, sheet_name='Results', index=False)

            # Get the workbook and the worksheet for formatting
            workbook  = writer.book
            worksheet = writer.sheets['Results']
            
            # Define formats for 'Pass', 'Fail'
            format_pass = workbook.add_format({'bg_color': '#E2EFDA', 'font_color': '#256029'})
            format_fail = workbook.add_format({'bg_color': '#FCE4D6', 'font_color': '#9C0006'})

            # Set the column width
            worksheet.set_column('A:A', 20)  # For ID column, wider to better fit data
            worksheet.set_column('B:G', 15)  # For result columns

            # Apply the conditional formatting to the Result columns only
            result_columns = ['32 gcc', '32 clang', '64 gcc', '64 clang', 'Overall Result']  # Specify the result columns
            for col_name in result_columns:
                col_num = df.columns.get_loc(col_name)
                worksheet.conditional_format(1, col_num, len(df), col_num, {
                    'type':     'text',
                    'criteria': 'containing',
                    'value':    'Pass',
                    'format':   format_pass
                })
                worksheet.conditional_format(1, col_num, len(df), col_num, {
                    'type':     'text',
                    'criteria': 'containing',
                    'value':    'Fail',
                    'format':   format_fail
                })

        print("Excel file has been created with all data in a single sheet and styled formatting.")