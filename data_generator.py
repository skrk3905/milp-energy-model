from pvlib.location import Location
import pandas as pd

# 1) Data preparation, 8760h PV CF and load
loc = Location(latitude=35.0116, longitude=135.7681, tz='Asia/Tokyo',
               altitude=50, name='Kyoto')

times = pd.date_range('2024-01-01', '2024-12-31 23:00', freq='h', tz=loc.tz)
clearsky = loc.get_clearsky(times, model='ineichen')
ghi = clearsky['ghi'] # [W/m2]
derate = 0.88 # 12%損失想定
pv_cf_hourly = (ghi / 1000) * derate # ghi -> cf

load = 1.0 + 1.8*np.sin((times.hour-18)/24*np.pi)**2
load *= 10_000 / load.sum()

df = pd.DataFrame({'pv_cf': pv_cf_hourly, 'load': load}, index=times)
df['daypart'] = ((df.index.hour >= 6) & (df.index.hour < 18)).astype(int)

# 3) 集計：month (1-12) × daypart (0/1)
agg = df.groupby([df.index.month, 'daypart']).agg(
        pv_cf=('pv_cf', 'mean'),
        load=('load', 'sum'),
        hours=('pv_cf', 'size')     # そのスライスの時間数
      ).reset_index()

# pivot → スライス番号 0…23
agg['slice'] = (agg['daypart'] + 2*(agg['index']-1)).astype(int)
agg = agg.sort_values('slice')
pv_cf_slice  = agg['pv_cf'].values           # 長さ24
load_slice   = agg['load'].values            # kWh
hours_slice  = agg['hours'].values           # h
