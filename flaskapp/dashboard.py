import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
def startDashboard(flaskserver):
    # Load dataset
    file_path = "https://raw.githubusercontent.com/Noorpr/Project-DEPI/refs/heads/main/resampled_15min_data.csv"
    df = pd.read_csv(file_path)

    # Convert 'Date' and 'Time' to a single datetime column
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], dayfirst=True)

    # Sort data
    df = df.sort_values("Datetime")

    # Compute KPI values
    total_energy = df["Energy_kWh"].sum()
    avg_voltage = df["Voltage"].mean()
    max_intensity = df["Global_intensity"].max()

    # KPI Cards
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            html.H4("Total Energy (kWh)", className="card-title", style={"color": "#e43721"}),
            html.H2(f"{total_energy:.2f}", className="card-text", style={"color": "#f0ab31"})
        ], body=True, style={"backgroundColor": "#0E0E0E", "textAlign": "center"}), width=4),

        dbc.Col(dbc.Card([
            html.H4("Avg Voltage (V)", className="card-title", style={"color": "#e43721"}),
            html.H2(f"{avg_voltage:.2f}", className="card-text", style={"color": "#f0ab31"})
        ], body=True, style={"backgroundColor": "#0E0E0E", "textAlign": "center"}), width=4),

        dbc.Col(dbc.Card([
            html.H4("Max Intensity (A)", className="card-title", style={"color": "#e43721"}),
            html.H2(f"{max_intensity:.2f}", className="card-text", style={"color": "#f0ab31"})
        ], body=True, style={"backgroundColor": "#0E0E0E", "textAlign": "center"}), width=4),
    ], className="g-3")

    # Figures
    fig_energy = px.line(df, x="Datetime", y="Energy_kWh_cummlative",
                        title="Cumulative Energy Consumption Over Time",
                        labels={"Energy_kWh_cummlative": "Cumulative Energy (kWh)"},
                        template="plotly_dark")
    fig_energy.update_traces(line_color='#e43721')
    fig_energy.update_layout(
        title_font=dict(color='#f0ab31'),
        xaxis=dict(color='#f0ab31'),
        yaxis=dict(color='#f0ab31'))

    fig_active_power = px.line(df, x="Datetime", y="Global_active_power",
                            title="Global Active Power Over Time",
                            labels={"Global_active_power": "Active Power (kW)"},
                            template="plotly_dark")
    fig_active_power.update_layout(
        title_font=dict(color='#f0ab31'),
        xaxis=dict(color='#f0ab31'),
        yaxis=dict(color='#f0ab31'))
    fig_active_power.update_traces(line_color='#e43721')
    fig_reactive_power = px.line(df, x="Datetime", y="Global_reactive_power",
                                title="Global Reactive Power Over Time",
                                labels={"Global_reactive_power": "Reactive Power (kVAR)"},
                                template="plotly_dark")
    fig_reactive_power.update_layout(
        title_font=dict(color='#f0ab31'),
        xaxis=dict(color='#f0ab31'),
        yaxis=dict(color='#f0ab31'))
    fig_reactive_power.update_traces(line_color='#e43721')

    fig_voltage = px.line(df, x="Datetime", y="Voltage",
                        title="Voltage Over Time",
                        labels={"Voltage": "Voltage (V)"},
                        template="plotly_dark")
    fig_voltage.update_layout(
        title_font=dict(color='#f0ab31'),
        xaxis=dict(color='#f0ab31'),
        yaxis=dict(color='#f0ab31'))
    fig_voltage.update_traces(line_color='#e43721')

    fig_power_factor = px.histogram(df, x="power_factor", nbins=50,
                                    title="Power Factor Distribution",
                                    labels={"power_factor": "Power Factor"},
                                    template="plotly_dark")
    fig_power_factor.update_layout(
        title_font=dict(color='#f0ab31'),
        xaxis=dict(color='#f0ab31'),
        yaxis=dict(color='#f0ab31'))
    fig_power_factor.update_traces(marker_color='#e43721')

    # Dash App Layout
    app = dash.Dash(__name__, server=flaskserver,url_base_pathname="/dashboard/", external_stylesheets=[dbc.themes.DARKLY])

    app.layout = html.Div([
        html.Div([
           
            html.H1("Energy Consumption Dashboard", style={"textAlign": "center", "color": "#e43721",'margin-left':'0px'})
        ], style={'display': 'flex', 'align-items': 'center', 'position' : 'center','justify-content':'center'}),

        kpi_cards,

        dbc.Row([
            dbc.Col(dcc.Graph(id="energy-graph", figure=fig_energy), width=6),
            dbc.Col(dcc.Graph(id="active-power-graph", figure=fig_active_power), width=6)
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Graph(id="reactive-power-graph", figure=fig_reactive_power), width=6),
            dbc.Col(dcc.Graph(id="voltage-graph", figure=fig_voltage), width=6)
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dcc.Graph(id="power-factor-graph", figure=fig_power_factor), width=6),
        ], className="g-3"),

        html.P("Filter by Date:", style={"textAlign": "center", "color": "#e43721"}),

        dcc.DatePickerRange(
            id="date-picker",
            start_date=df["Datetime"].min().date(),
            end_date=df["Datetime"].max().date(),
            display_format="DD/MM/YYYY"
        ),

        dbc.Row([
            dash_table.DataTable(
                id="filtered-table",
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
                style_header={"backgroundColor": "#0E0E0E", "color": "#e43721"},
                style_data={"backgroundColor": "#0E0E0E", "color": "#f0ab31"},
                style_as_list_view=True
            )
        ])
    ], style={"backgroundColor": "#0E0E0E", "color": "#e43721", "padding": "20px"})

    # Callback to update table based on date filter
    @app.callback(
        Output("filtered-table", "data"),
        [Input("date-picker", "start_date"),
        Input("date-picker", "end_date")]
    )
    def update_table(start_date, end_date):
        filtered_df = df[(df["Datetime"] >= start_date) & (df["Datetime"] <= end_date)]
        return filtered_df.to_dict("records")
    return app


    # old colors
    #1E90FF
    #0E0E0E
    #white