from oocana import Context
import plotly.graph_objects as go

# "in", "out" is the default node key.
# Redefine the name and type of the node, change it manually below.
# Click on the gear(⚙) to configure the input output UI


def main(inputs: dict, context: Context):
    # inputs.get("in") -> help you get node input value
    data = inputs.get("df")
    stock_name = inputs.get("stock_name")
    # context.preview(df)

    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    data["SMA_200"] = data["Close"].rolling(window=200).mean()

    data["Signal"] = 0.0
    data["Signal"][data["SMA_50"] > data["SMA_200"]] = 1.0
    data["Signal"][data["SMA_50"] < data["SMA_200"]] = -1.0

    data["Return"] = data["Close"].pct_change() * data["Signal"].shift()
    data["Cumulative_Return"] = (1 + data["Return"]).cumprod()

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close Price"))

    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_50"], name="50 Day SMA"))

    fig.add_trace(go.Scatter(x=data.index, y=data["SMA_200"], name="200 Day SMA"))

    fig.add_trace(
        go.Scatter(x=data.index, y=data["Cumulative_Return"], name="Cumulative Return")
    )

    fig.update_layout(
        title="Moving Average Crossover Strategy for " + stock_name,
        yaxis_title="Price / Cumulative Return",
        xaxis_title="Date",
        legend_title="Legend Title",
        font=dict(family="Arial", size=12),
    )

    fig.show()

    return {"df": data}
