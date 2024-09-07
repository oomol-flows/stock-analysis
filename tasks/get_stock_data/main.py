from oocana import Context
import yfinance as yf
from datetime import datetime
# "in", "out" is the default node key.
# Redefine the name and type of the node, change it manually below.
# Click on the gear(⚙) to configure the input output UI

def main(inputs: dict, context: Context):
  # inputs.get("in") -> help you get node input value
  stock_name = inputs.get("stock_name")
  # 下载苹果股票的历史数据
  start_time = inputs.get("start_time")
  end_time = inputs.get("end_time")
  data = yf.download(stock_name, start=trans_time(start_time), end=trans_time(end_time))

  # context.preview(data)

  # 计算50日和200日的简单移动平均线
  
  return { "df": data, "stock_name": stock_name }

def trans_time(time_str):

# 解析时间字符串为datetime对象
  dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")

  # 格式化输出只有日期的部分
  formatted_date = dt.strftime("%Y-%m-%d")  
  return formatted_date
