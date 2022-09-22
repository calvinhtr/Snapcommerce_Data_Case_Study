import pandas as pd
import re

class TableParser():
    '''
    Init function where you input the data as a string. Init function will split the input_data based on a set of delimiters and group the rows into individual lists.
    Then, it will extract the rows and columns from the split data and create a pandas dataframe
    '''
    def __init__(self, input_data: str, num_cols: int, delimiters: list) -> None:
        split = self.mult_split(input_data, delimiters)
        # Only iterate through a multiple of num_cols, so that any non-filled row is removed
        all_data = [split[x:x+num_cols] for x in range(0, len(split)-len(split)%num_cols, num_cols)]
        self.data = all_data[1:]
        self.cols = all_data[0]
        self.df = pd.DataFrame(self.data, columns=self.cols)

    '''
    Helper function to split a string based on a list of delimiters
    '''
    def mult_split(self, input_data: str, delimiters: list) -> list:
        for i in range(1, len(delimiters)):
            new_data = input_data.replace(delimiters[i], delimiters[0])
        return new_data.split(delimiters[0])

    '''
    Replace the 'To_From' column with two separate columns
    '''
    def format_to_from(self):
        if 'To_From' in self.cols:
            self.df[['To', 'From']] = self.df.To_From.str.split('_', expand=True)
            self.df = self.df.drop('To_From', axis=1)

    '''
    Make the specified column into upper case only
    '''
    def to_upper(self, col_name: str):
        if col_name in self.cols:
            self.df[col_name] = self.df[col_name].map(lambda elem: elem.upper())

    '''
    Remove all numbers and special characters except for spaces from the specified column
    '''
    def remove_special_chars(self, col_name: str):
        if col_name in self.cols:
            for _, row in self.df.iterrows():
                row[col_name] = re.sub(r'[^a-zA-Z ]', '', row[col_name])

    '''
    Fill in missing data points in 'FlightCodes' and convert column to int
    '''
    def fix_flight_codes(self):
        for i in range(len(self.df)):
            if self.df.loc[i, 'FlightCodes'] == '':
                # Check if previous and following entry in 'FlightCodes' column is valid
                if self.df.loc[i-1, 'FlightCodes'] != '' and self.df.loc[i+1, 'FlightCodes'] != '' and int(float(self.df.loc[i-1, 'FlightCodes'])) == int(float(self.df.loc[i+1, 'FlightCodes']))-20:
                    self.df.loc[i, 'FlightCodes'] = int(float(self.df.loc[i-1, 'FlightCodes'])) + 10
        # Convert column to int
        self.df['FlightCodes'] = self.df['FlightCodes'].astype(float).astype(int)

    '''
    For testing purposes
    '''
    def print_table(self):
        print(self.df)


data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'
t = TableParser(data, 4, [';','\n'])
t.to_upper('To_From')
t.remove_special_chars('Airline Code')
t.fix_flight_codes()
t.format_to_from()
t.print_table()