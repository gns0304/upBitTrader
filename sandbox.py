import jwt, uuid, json, requests, math
import numpy, pandas

def RSItest(self, length=14):

    preMinuteData = self.getMinuteCandle("KRW-BTC", 1, 200)
    df = pandas.DataFrame(columns=["date", "tradingPrice", "difference", "up", "down"])

    for i in range(len(preMinuteData)):

        if i == 0:

            df.loc[i] = [preMinuteData[len(preMinuteData) - 1 - i]['candle_date_time_kst'],
                         preMinuteData[len(preMinuteData) - 1 - i]['trade_price'], 0,
                         0, 0]

        else:
            df.loc[i] = [preMinuteData[len(preMinuteData) - 1 - i]['candle_date_time_kst'],
                         preMinuteData[len(preMinuteData) - 1 - i]['trade_price'],
                         preMinuteData[len(preMinuteData) - 1 - i]['trade_price'] - df.loc[i - 1, 'tradingPrice'],
                         0, 0]

            if df.loc[i, 'difference'] > 0:
                df.loc[i, 'up'] = abs(df.loc[i, 'difference'])
                df.loc[i, 'down'] = 0
            else:
                df.loc[i, 'down'] = abs(df.loc[i, 'difference'])
                df.loc[i, 'up'] = 0



    dfMean = pandas.DataFrame(columns=['AU', 'AD'])

    AU = 0
    AD = 0

    for i in range(len(preMinuteData)):

        if i <= length-2 :

            AU = AU + df.loc[i, 'up']
            AD = AD + df.loc[i, 'down']

        if i == length-1:

            dfMean.loc[length - 1, 'AU'] = AU
            dfMean.loc[length - 1, 'AD'] = AD

        if i >= length:
            dfMean.loc[i, 'AU'] = (dfMean.loc[i - 1, 'AU'] * (length - 1) + df.loc[i - 1, 'up']) / length
            dfMean.loc[i, 'AD'] = (dfMean.loc[i - 1, 'AD'] * (length - 1) + df.loc[i - 1, 'down']) / length



    rsi = pandas.DataFrame(columns=["rsi"])
    for i in range(len(preMinuteData)):
        if i >= length-1 :
            rsi.loc[i, 'rsi'] = 100 * dfMean.loc[i, 'AU'] / (dfMean.loc[i, 'AU'] + dfMean.loc[i, 'AD'])

    result = pandas.concat([df, dfMean, rsi], axis=1)
    pandas.set_option('display.max_columns', 10)
    pandas.set_option('display.max_rows', 200)
    pandas.set_option('display.width', None)
    print(result.loc[199,'rsi'])
    print(result)
