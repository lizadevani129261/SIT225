from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from collections import deque


# =========================================================
# Reusable wrapper function for smooth streaming
# =========================================================
class SmoothStream:
    def __init__(self, csv_file, max_points=50):
        self.data = pd.read_csv(csv_file)

        self.data["time"] = pd.to_datetime(
            self.data["time"],
            format="mixed"
        )

        self.index = 0

        self.time_buffer = deque(maxlen=max_points)
        self.x_buffer = deque(maxlen=max_points)
        self.y_buffer = deque(maxlen=max_points)
        self.z_buffer = deque(maxlen=max_points)

    def get_next_sample(self):
        """
        Retrieves the next accelerometer sample and adds it
        to a rolling buffer.

        The rolling buffer prevents the complete dataset from
        being redrawn as a new batch each time.
        """

        if self.index >= len(self.data):
            self.index = 0

        row = self.data.iloc[self.index]

        self.time_buffer.append(row["time"])
        self.x_buffer.append(row["x"])
        self.y_buffer.append(row["y"])
        self.z_buffer.append(row["z"])

        self.index += 1

    def create_figure(self):
        """
        Creates the Plotly figure from the current rolling
        window of accelerometer samples.
        """

        figure = go.Figure()

        figure.add_trace(
            go.Scatter(
                x=list(self.time_buffer),
                y=list(self.x_buffer),
                mode="lines+markers",
                name="Accelerometer X"
            )
        )

        figure.add_trace(
            go.Scatter(
                x=list(self.time_buffer),
                y=list(self.y_buffer),
                mode="lines+markers",
                name="Accelerometer Y"
            )
        )

        figure.add_trace(
            go.Scatter(
                x=list(self.time_buffer),
                y=list(self.z_buffer),
                mode="lines+markers",
                name="Accelerometer Z"
            )
        )

        figure.update_layout(
            title="Smooth Accelerometer Data Stream",
            xaxis_title="Time",
            yaxis_title="Acceleration (m/s²)",
            uirevision="constant"
        )

        return figure


# =========================================================
# Create streaming object
# =========================================================

stream = SmoothStream(
    "accelerometer_combined.csv",
    max_points=50
)


# =========================================================
# Dash application
# =========================================================

app = Dash(__name__)

app.layout = html.Div([

    html.H1(
        "SIT225 - Smooth Accelerometer Dashboard",
        style={"textAlign": "center"}
    ),

    html.P(
        "Continuous X, Y and Z accelerometer visualisation",
        style={"textAlign": "center"}
    ),

    dcc.Graph(
        id="accelerometer-graph"
    ),

    dcc.Interval(
        id="stream-interval",
        interval=250,
        n_intervals=0
    )
])


@app.callback(
    Output("accelerometer-graph", "figure"),
    Input("stream-interval", "n_intervals")
)
def update_dashboard(n):

    # Add ONE new sample per update.
    # This avoids waiting for a complete batch.
    stream.get_next_sample()

    return stream.create_figure()


if __name__ == "__main__":

    print("Starting SIT225 smooth streaming dashboard...")

    app.run(debug=True)