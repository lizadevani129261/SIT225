# SIT225 Week 8.2C – Smooth Accelerometer Dashboard

This activity demonstrates incremental visualisation of smartphone accelerometer X, Y and Z data using Python, Plotly and Dash.

The SmoothStream wrapper maintains a rolling buffer of accelerometer samples. A Dash interval callback adds one new sample at a time and refreshes the graph every 250 ms. This avoids waiting for a complete batch of samples before updating the visualisation.

Files:
- smooth_accelerometer_dash.py – Plotly Dash application and reusable SmoothStream wrapper.
- accelerometer_combined.csv – accelerometer X, Y and Z dataset captured during the Arduino IoT Cloud activity.

The dashboard displays the three accelerometer axes continuously as the stored sensor samples are replayed incrementally.
