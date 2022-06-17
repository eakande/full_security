import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("full_insecurity.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%m/%Y")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Nigeria Security Tracker!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="👋", className="header-emoji"),
                html.H1(
                    children=" CAPE Economic Research and Consulting Insecurity Tracker", className="header-title"
                ),
                html.P(
                    children="State-by-state security tracker in Nigeria"
                    ""
                    " From 2011 till date",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State", className="menu-title"),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[
                                {"label": state, "value": state}
                                for state in np.sort(data.state.unique())
                            ],
                            value="Adamawa",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="death-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="incidence-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("death-chart", "figure"), Output("incidence-chart", "figure")],
    [
        Input("state-filter", "value"),

    ],
)
def update_charts(state):
    mask = (
        (data.state == state)
    )
    filtered_data = data.loc[mask, :]
    death_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Death"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Number of Death Reported",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    incidence_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["incidence"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Number Incidence Occurrence",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return death_chart_figure, incidence_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)



