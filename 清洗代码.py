import pandas as pd
import numpy as np
df=pd.read_csv('order_data_2100.csv')
print(df.head())
print(df.tail())

# 检查数据数值整体情况
print(df['pay_amount'].describe())

# 检测，清除重复值
print(df.duplicated(subset='order_id',keep="first").sum())
df.drop_duplicates(subset='order_id',keep='first',inplace=True)
print(df.duplicated(subset='order_id',keep="first").sum())
print(df['pay_amount'].sum())

# 检测数据空值
print(df.isna().sum())
print(df.dropna().count())

# 填充city空值为未知
df['city']=df['city'].fillna('未知')
print(df['city'].count())
print(df['city'].value_counts())

# 金融、日期缺失行单独剔除
pay_missing=df[df['pay_amount'].isna()]
date_missing=df[df['order_date'].isna()]

# 城市、支付方式的空格剔除
print(df['city'].unique())
df['city'] = df['city'].str.strip()
df['pay_type'] = df['pay_type'].str.strip()
print(df['city'].unique())

# 格式不对的日期统计与有效日期统计
df['order_date_dt'] = pd.to_datetime(df['order_date'], errors='coerce')
bad_date = df[df['order_date_dt'].isna()]
print("非法日期数量：", len(bad_date))
print(bad_date['order_date'].value_counts())
mouth_date=df['order_date_dt'].dt.to_period('M')
print(mouth_date.value_counts())

# 支付方式不规范的处理和统计
print(df['pay_type'].unique())
print(df['pay_type'].value_counts())
pay_map={'支付 宝':'支付宝','zhifubao':'支付宝','微 信':'微信','微xin':'微信','花呗':'支付宝','微信支付':'微信'}
df['pay_type_clean'] = df['pay_type'].replace(pay_map)
print(df['pay_type_clean'].value_counts())

# 金额异常-负数的数据
pay_amount_negative=df[df['pay_amount']<0]
print(len(pay_amount_negative))
print(pay_amount_negative['pay_amount'].sum())

# 金额异常-大额离散的数据
# 仅用正金额计算阈值
temp = df[df['pay_amount'] >= 0]['pay_amount']
Q1 = temp.quantile(0.25)
Q3 = temp.quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 3 * IQR  # 极端异常用3倍IQR
outlier_df = df[df['pay_amount'] > upper_limit]
print(len(outlier_df['pay_amount']))
print(outlier_df['pay_amount'].sum())

# 统计有效数据并对异常数据进行标记
df['is_valid'] = True
# 标记各类无效订单
df.loc[df['pay_amount'].isna(), 'is_valid'] = False          # 金额空值
df.loc[df['order_date_dt'].isna(), 'is_valid'] = False       # 日期无效/空值
df.loc[df['pay_amount'] < 0, 'is_valid'] = False             # 负数金额（退款/冲正）
df.loc[df['pay_amount'] > upper_limit, 'is_valid'] = False  # 大额异常
# 快速统计
print("总订单数：", len(df))
print("有效订单数：", df['is_valid'].sum())
print("无效订单数：", (~df['is_valid']).sum())
# 计算有效总金额
valid_total = df.loc[df['is_valid'], 'pay_amount'].sum()
print("有效订单总金额：", round(valid_total, 2))
