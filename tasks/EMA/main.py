from oocana import Context
import plotly.graph_objects as go

# "in", "out" is the default node key.
# Redefine the name and type of the node, change it manually below.
# Click on the gear(⚙) to configure the input output UI

def main(inputs: dict, context: Context):
  # inputs.get("in") -> help you get node input value

  # 计算短期和长期的 EMA
  data = inputs.get("df")
  stock_name = inputs.get("stock_name")
  short_window = inputs.get("short_window")
  long_window = inputs.get("long_window")
  
  data[f'EMA_{short_window}'] = data['Close'].ewm(span=short_window, adjust=False).mean()
  data[f'EMA_{long_window}'] = data['Close'].ewm(span=long_window, adjust=False).mean()

  # 生成交易信号
  data['Signal'] = 0.0
  data['Signal'][data[f'EMA_{short_window}'] > data[f'EMA_{long_window}']] = 1.0
  data['Signal'][data[f'EMA_{short_window}'] < data[f'EMA_{long_window}']] = -1.0

  # 计算策略收益
  data['Return'] = data['Close'].pct_change() * data['Signal'].shift()
  data['Cumulative_Return'] = (1 + data['Return']).cumprod()

  # 创建 Plotly 图表
  fig = go.Figure()

  # 添加股价数据
  fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))

  # 添加短期 EMA
  fig.add_trace(go.Scatter(x=data.index, y=data[f'EMA_{short_window}'], name=f'{short_window} Day EMA'))

  # 添加长期 EMA
  fig.add_trace(go.Scatter(x=data.index, y=data[f'EMA_{long_window}'], name=f'{long_window} Day EMA'))

  # 添加累计收益曲线
  fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Return'], name='Cumulative Return'))

  # 设置图表标题和轴标签
  fig.update_layout(
      title='Exponential Moving Average Crossover Strategy for ' + stock_name,
      yaxis_title='Price / Cumulative Return',
      xaxis_title='Date',
      legend_title='Legend Title',
      font=dict(family='Arial', size=12)
  )

  # 显示图表
  fig.show()

  return { "df": data }
