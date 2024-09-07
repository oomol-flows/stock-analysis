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

  data['SMA_50'] = data['Close'].rolling(window=50).mean()
  data['SMA_200'] = data['Close'].rolling(window=200).mean()

  # 生成交易信号
  data['Signal'] = 0.0
  data['Signal'][data['SMA_50'] > data['SMA_200']] = 1.0
  data['Signal'][data['SMA_50'] < data['SMA_200']] = -1.0

  # 计算策略收益
  data['Return'] = data['Close'].pct_change() * data['Signal'].shift()
  data['Cumulative_Return'] = (1 + data['Return']).cumprod()

  # 创建 Plotly 图表
  fig = go.Figure()

  # 添加股价数据
  fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))

  # 添加50日移动平均线
  fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='50 Day SMA'))

  # 添加200日移动平均线
  fig.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], name='200 Day SMA'))

  # 添加累计收益曲线
  fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Return'], name='Cumulative Return'))

  # 设置图表标题和轴标签
  fig.update_layout(
      title='Moving Average Crossover Strategy for ' + stock_name,
      yaxis_title='Price / Cumulative Return',
      xaxis_title='Date',
      legend_title='Legend Title',
      font=dict(family='Arial', size=12)
  )

  # 显示图表
  fig.show()


  return { "df": data }
