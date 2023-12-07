import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Read CSV file
df = pd.read_csv('/Users/andreidanila/Desktop/System engineering/mapped_data.csv')

# Parse timestamp column
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create a subplot with buttons
fig = make_subplots(rows=1, cols=1, subplot_titles=["CO2, PV, and Demand"])

# Add trace for each column
for column, unit in [('Co2', 'CO2 / kWh'), ('PV', 'kW'), ('Demand', 'kW')]:
    trace = go.Scatter(x=df['Timestamp'], y=df[column], mode='lines', name=f'{column} ({unit})')
    fig.add_trace(trace, row=1, col=1)

    # Update y-axis label
    fig.update_yaxes(title_text=f'{column} ({unit})', row=1, col=1)

# Create buttons for switching between columns
buttons = [
    dict(label=f'{column} ({unit})',
         method="update",
         args=[{"visible": [col == column for col in ['Co2', 'PV', 'Demand']]}])
    for column, unit in [('Co2', 'CO2 / kWh'), ('PV', 'kW'), ('Demand', 'kW')]
]

# Update layout to include buttons
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=buttons,
            x=1.2,
            y=0.5,
        ),
    ]
)

# Update layout for better visibility
fig.update_layout(title_text="CO2, PV, and Demand Over Time", xaxis_title="Timestamp", yaxis_title="Value")

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='line-plot', figure=fig),
    html.Label('Select Date Range:'),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=df['Timestamp'].min(),
        end_date=df['Timestamp'].max(),
        display_format='YYYY-MM-DD',
    ),
])

# Define callback to update the plot based on the selected date
@app.callback(
    Output('line-plot', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_plot(start_date, end_date):
    filtered_df = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]

    # Create a subplot with buttons
    updated_fig = make_subplots(rows=1, cols=1, subplot_titles=["CO2, PV, and Demand"])

    # Add trace for each column
    for column, unit in [('Co2', 'CO2 / kWh'), ('PV', 'kW'), ('Demand', 'kW')]:
        trace = go.Scatter(x=filtered_df['Timestamp'], y=filtered_df[column], mode='lines', name=f'{column} ({unit})')
        updated_fig.add_trace(trace, row=1, col=1)

        # Update y-axis label
        updated_fig.update_yaxes(title_text=f'{column} ({unit})', row=1, col=1)

    # Update layout for better visibility
    updated_fig.update_layout(title_text=f"CO2, PV, and Demand Over Time ({start_date} to {end_date})",
                              xaxis_title="Timestamp", yaxis_title="Value")

    return updated_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
