"""
linear regression
"""

import pandas as pd
import datetime
import plotly.express as px
from data_cleanup import keep_for_value, remove_columns, dates_to_datetime

supply_chain_data = pd.read_csv('data/supply_chain_data.csv')
keep_for_value(supply_chain_data, {'Performance indicators': 'Containers, port dwell time East Coast ports'})
remove_columns(supply_chain_data, [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14])
dates_to_datetime(supply_chain_data, 'REF_DATE')
print(supply_chain_data)

fig = px.line(supply_chain_data, x="REF_DATE", y="VALUE")
fig.show()
