from calendar import c
import pandas as pd
import numpy as np
import re

class TableParser():
    '''
    
    '''
    def __init__(self, input_data: str, num_cols: int) -> None:
        split = self.mult_split(input_data, [';','\n'])
        # Only iterate through a multiple of num_cols
        all_data = [split[x:x+num_cols] for x in range(0, len(split)-len(split)%num_cols, num_cols)]
        self.data = all_data[1:]
        self.cols = all_data[0]
        self.df = pd.DataFrame(self.data, columns=self.cols)

    def mult_split(self, input_data: str, delimiters: list):
        for i in range(1, len(delimiters)):
            new_data = input_data.replace(delimiters[i], delimiters[0])
        return new_data.split(delimiters[0])

    def format_to_from(self):
        if 'To_From' in self.cols:
            self.df[['To', 'From']] = self.df.To_From.str.split('_', expand=True)
            self.df = self.df.drop('To_From', axis=1)

    def to_upper(self, col_name: str):
        if col_name in self.cols:
            self.df[col_name] = self.df[col_name].map(lambda elem: elem.upper())

    def remove_special_chars(self, col_name: str):
        if col_name in self.cols:
            for _, row in self.df.iterrows():
                row[col_name] = re.sub(r'[^a-zA-Z ]', '', row[col_name])

    def fix_flight_codes(self):
        for i in range(len(self.df)):
            if self.df.loc[i, 'FlightCodes'] == '':
                if self.df.loc[i-1, 'FlightCodes'] != '' and self.df.loc[i+1, 'FlightCodes'] != '' and int(float(self.df.loc[i-1, 'FlightCodes'])) == int(float(self.df.loc[i+1, 'FlightCodes']))-20:
                    self.df.loc[i, 'FlightCodes'] = int(float(self.df.loc[i-1, 'FlightCodes'])) + 10
        self.df['FlightCodes'] = self.df['FlightCodes'].astype(float).astype(int)


    def print_table(self):
        print(self.df)


data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'
t = TableParser(data, 4)
t.to_upper('To_From')
t.remove_special_chars('Airline Code')
t.fix_flight_codes()
t.format_to_from()
t.print_table()