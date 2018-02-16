import pandas as pd
from matplotlib import pyplot as plt

season_df = pd.read_csv("cusa_season_avgs.csv")

column_names = [c for c in season_df]
print(column_names)

fig, axes = plt.subplots(3,5)

# print(season_df)

# Where does UAB sit among its UAB peers?
# This is a really obtuse way to view these stats
for statistic in column_names[1:]:

    season_df = season_df.sort_values(statistic)
    season_df.plot(x='TEAM',
                   y=statistic,
                   kind='bar',
                   sort_columns=True)
    plt.show()
