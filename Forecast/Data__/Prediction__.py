from pandas import read_csv
from pandas import to_datetime
from pandas import DataFrame
from fbprophet import Prophet
from matplotlib import pyplot
from pandas.core.indexes.datetimes import DatetimeIndex

path = input('Enter path to csv file: ')
df = read_csv(path, header=0)

n = int(input('Enter number of months to predict(1-10): '))
while n<1 or n>10:
    n = int(input('Enter number of months to predict(1-10): '))

df.columns = ['ds', 'y']
df['ds']= to_datetime(df['ds'])

model = Prophet()
model.fit(df)

future = list()
for i in range(3,n+3):
    if i in {1,3,5,7,8,10,12}:
        for j in range(1,31):
            date = '2021-%02d-%02d' % (i,j)
            future.append([date])
    elif i in {4,6,9,11}:
        for j in range(1,30):
            date = '2021-%02d-%02d' % (i,j)
            future.append([date])
    else:
        for j in range(1,28):
            date = '2021-%02d-%02d' % (i,j)
            future.append([date])
future = DataFrame(future)
future.columns = ['ds']
future['ds']= to_datetime(future['ds'])

forecast = model.predict(future)

df_ = DataFrame(forecast[['ds','yhat']])
df_['ds'].apply(lambda x: x.strftime('%Y/%m/%d'))
df_.columns = ['month','total waste generated (kg/day)']
df_.to_csv('out.csv', index=False)

model.plot(forecast)
pyplot.show()