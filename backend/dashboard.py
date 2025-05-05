import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import math


def startDashboard(flaskserver):
    # Load dataset
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

    # Add custom CSS
    app = dash.Dash(__name__,server=flaskserver,url_base_pathname="/dashboard/", external_stylesheets=[dbc.themes.DARKLY])

    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                .kpi-card {
                    background-color: #0E0E0E;
                    text-align: center;
                    border: 1px solid #333;
                    box-shadow: 0 4px 8px rgba(228, 55, 33, 0.2);
                    transition: transform 0.3s, box-shadow 0.3s;
                    cursor: pointer;
                    border-radius: 5px;
                    padding: 15px;
                }

                .kpi-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 8px 16px rgba(228, 55, 33, 0.4);
                    border: 1px solid #e43721;
                }

                .date-filter-container {
                    margin: 20px auto;
                    padding: 15px;
                    background-color: #111;
                    border-radius: 5px;
                    border: 1px solid #333;
                    max-width: 800px;
                    text-align: center;
                }

                .pagination-controls {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 15px;
                    margin-bottom: 15px;
                }

                .pagination-button {
                    background-color: #0E0E0E;
                    color: #e43721;
                    border: 1px solid #e43721;
                    padding: 5px 15px;
                    margin: 0 5px;
                    border-radius: 3px;
                    cursor: pointer;
                    transition: all 0.3s;
                }

                .pagination-button:hover {
                    background-color: #e43721;
                    color: #0E0E0E;
                }

                .pagination-info {
                    color: #ffffff;
                    margin: 0 15px;
                }

                .row-selector {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 15px;
                    margin-bottom: 15px;
                }

                .row-selector label {
                    color: #e43721;
                    margin-right: 10px;
                }

                .data-table-container {
                    border: 1px solid #333;
                    border-radius: 5px;
                    padding: 5px;
                    box-shadow: 0 4px 8px rgba(228, 55, 33, 0.2);
                    margin-top: 15px;
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    # KPI Cards
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([
            html.H4("Total Energy (kWh)", className="card-title", style={"color": "#ffffff"}),
            html.H2(f"{total_energy:.2f}", className="card-text", style={"color": "#e43721"})
        ], body=True, className="kpi-card"), width=4),

        dbc.Col(dbc.Card([
            html.H4("Avg Voltage (V)", className="card-title", style={"color": "#ffffff"}),
            html.H2(f"{avg_voltage:.2f}", className="card-text", style={"color": "#e43721"})
        ], body=True, className="kpi-card"), width=4),

        dbc.Col(dbc.Card([
            html.H4("Max Intensity (A)", className="card-title", style={"color": "#ffffff"}),
            html.H2(f"{max_intensity:.2f}", className="card-text", style={"color": "#e43721"})
        ], body=True, className="kpi-card"), width=4),
    ], className="g-3", style={"margin-bottom": "20px", "justify-content": "center"})

    # Figures
    fig_energy = px.line(df, x="Datetime", y="Energy_kWh_cummlative",
                        title="Cumulative Energy Consumption Over Time",
                        labels={"Energy_kWh_cummlative": "Cumulative Energy (kWh)"},
                        template="plotly_dark")
    fig_energy.update_traces(line_color='#e43721')
    fig_energy.update_layout(
        title_font=dict(color='#ffffff'),
        xaxis=dict(color='#ffffff'),
        yaxis=dict(color='#ffffff'))

    fig_active_power = px.line(df, x="Datetime", y="Global_active_power",
                            title="Global Active Power Over Time",
                            labels={"Global_active_power": "Active Power (kW)"},
                            template="plotly_dark")
    fig_active_power.update_layout(
        title_font=dict(color='#ffffff'),
        xaxis=dict(color='#ffffff'),
        yaxis=dict(color='#ffffff'))
    fig_active_power.update_traces(line_color='#e43721')

    fig_reactive_power = px.line(df, x="Datetime", y="Global_reactive_power",
                                title="Global Reactive Power Over Time",
                                labels={"Global_reactive_power": "Reactive Power (kVAR)"},
                                template="plotly_dark")
    fig_reactive_power.update_layout(
        title_font=dict(color='#ffffff'),
        xaxis=dict(color='#ffffff'),
        yaxis=dict(color='#ffffff'))
    fig_reactive_power.update_traces(line_color='#e43721')

    fig_voltage = px.line(df, x="Datetime", y="Voltage",
                        title="Voltage Over Time",
                        labels={"Voltage": "Voltage (V)"},
                        template="plotly_dark")
    fig_voltage.update_layout(
        title_font=dict(color='#ffffff'),
        xaxis=dict(color='#ffffff'),
        yaxis=dict(color='#ffffff'))
    fig_voltage.update_traces(line_color='#e43721')

    fig_power_factor = px.histogram(df, x="power_factor", nbins=50,
                                    title="Power Factor Distribution",
                                    labels={"power_factor": "Power Factor"},
                                    template="plotly_dark")
    fig_power_factor.update_layout(
        title_font=dict(color='#ffffff'),
        xaxis=dict(color='#ffffff'),
        yaxis=dict(color='#ffffff'))
    fig_power_factor.update_traces(marker_color='#e43721')

    # Dash App Layout
    app.layout = html.Div([
        html.Div(
    [
        html.H1(
            [
                html.Span("Energy Consumption ", style={"color": "#ffffff", 'fontWeight': "bold"}),
                html.Span("Dashboard", style={"color": "#e43721", 'fontWeight': "bold"}),
            ],
            style={
                "textAlign": "center",
                "margin": "0"
            }
        )
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'marginBottom': '26px'
    }
),


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
            dbc.Col(dcc.Graph(id="power-factor-graph", figure=fig_power_factor), width=12),
        ], className="g-3"),

        html.Div([
            html.H4("Filter by Date:", style={"color": "#e43721", "marginBottom": "15px"}),

            dcc.DatePickerRange(
                id="date-picker",
                start_date=df["Datetime"].min().date(),
                end_date=df["Datetime"].max().date(),
                display_format="DD/MM/YYYY"
            ),

            html.Div([
                html.Label("Rows per page:", className="mr-2", style={"color": "#e43721"}),
                dcc.Dropdown(
                    id="page-size-dropdown",
                    options=[
                        {"label": "10", "value": 10},
                        {"label": "20", "value": 20},
                        {"label": "50", "value": 50},
                        {"label": "100", "value": 100}
                    ],
                    value=20,
                    clearable=False,
                    style={
                        "width": "100px",
                        "display": "inline-block",
                        "color": "#0E0E0E"
                    }
                )
            ], className="row-selector"),

            html.Div([
                dash_table.DataTable(
                    id="filtered-table",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_current=0,
                    page_size=20,
                    page_action="custom",
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "backgroundColor": "#0E0E0E",
                        "color": "#ffffff",
                        "border": "1px solid #333",
                        "padding": "8px"
                    },
                    style_header={
                        "backgroundColor": "#1a1a1a",
                        "color": "#e43721",
                        "fontWeight": "bold",
                        "borderBottom": "2px solid #333",
                        "textAlign": "center"
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "#111"
                        },
                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "#333",
                            "border": "1px solid #e43721"
                        }
                    ],
                    style_as_list_view=True
                )
            ], className="data-table-container"),

            html.Div([
                html.Button("Previous", id="prev-page-button", className="pagination-button"),
                html.Div(id="page-indicator", className="pagination-info"),
                html.Button("Next", id="next-page-button", className="pagination-button")
            ], className="pagination-controls")
        ], className="date-filter-container")
    ], style={"backgroundColor": "#0E0E0E", "color": "#e43721", "padding": "20px"})

    # Callback to update table based on date filter and pagination
    @app.callback(
        [Output("filtered-table", "data"),
        Output("page-indicator", "children")],
        [Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("prev-page-button", "n_clicks"),
        Input("next-page-button", "n_clicks"),
        Input("page-size-dropdown", "value")],
        [State("filtered-table", "page_current")]
    )
    def update_table(start_date, end_date, prev_clicks, next_clicks, page_size, page_current):
        # Convert string dates to datetime
        if start_date is not None:
            start_date = pd.to_datetime(start_date)
        else:
            start_date = df["Datetime"].min()

        if end_date is not None:
            end_date = pd.to_datetime(end_date)
        else:
            end_date = df["Datetime"].max()

        # Filter based on date range
        filtered_df = df[(df["Datetime"] >= start_date) & (df["Datetime"] <= end_date)]

        # Initialize page_current if it's None
        if page_current is None:
            page_current = 0

        # Handle page navigation button clicks
        ctx = dash.callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == "prev-page-button" and page_current > 0:
                page_current = page_current - 1
            elif button_id == "next-page-button" and (page_current + 1) * page_size < len(filtered_df):
                page_current = page_current + 1

        # Calculate page slice
        page_start = page_current * page_size
        page_end = min((page_current + 1) * page_size, len(filtered_df))

        # Page indicator text
        total_pages = max(1, math.ceil(len(filtered_df) / page_size))
        page_indicator = f"Page {page_current + 1} of {total_pages} ({len(filtered_df)} records)"

        return filtered_df.iloc[page_start:page_end].to_dict('records'), page_indicator

    # Update page current when page size changes to avoid empty pages
    @app.callback(
        Output("filtered-table", "page_current"),
        [Input("page-size-dropdown", "value")]
    )
    def reset_page_index(page_size):
        return 0
    return app


    # old colors
    #1E90FF
    #0E0E0E
    #white