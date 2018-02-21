'''
explore_cusa.py
'''

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib

matplotlib.style.use('ggplot')

# These two files have data taken from ESPN, avg_df is how teams in CUSA has
# performed all year.  vs_uab_df has data from how CUSA teams have performed
# against UAB
avg_df = pd.read_csv("cusa_season_avgs.csv")
vs_uab_df = pd.read_csv("cusa_matchup.csv")

# lets format our df to something more readable
avg_df = avg_df.set_index('TEAM')

vs_uab_df['TEAM'] = vs_uab_df['OPPONENT']
vs_uab_df = vs_uab_df.drop('OPPONENT', axis=1)
vs_uab_df = vs_uab_df.set_index('TEAM')

# transform the data to use percentages instead of make/miss columns
vs_df = vs_uab_df.loc[:][['WIN', 'HOME', 'OREB', 'DREB', 'REB', 'AST', 'STL',
                          'BLK', 'TO', 'PF', 'PTS']]
vs_df['FG%'] = vs_uab_df['FGA']/vs_uab_df['FGM']
vs_df['3P%'] = vs_uab_df['3PA']/vs_uab_df['3PM']
vs_df['FT%'] = vs_uab_df['FTA']/vs_uab_df['FTM']

# start working data into comparisons vs UAB
print("Both DF's have same index? -->", all(vs_df.index == avg_df.index))
comp_df = pd.DataFrame()

# Positive means team performed well against UAB
# Negative means team performed poorly against UAB
comp_df['PTS'] =  vs_df['PTS'] - avg_df['PPG']
comp_df['TO'] =   avg_df['TPG'] - vs_df['TO'] # reversed b/c its better to have less turnovers
comp_df['REB'] =  vs_df['REB'] - avg_df['RPG']
comp_df['AST'] =  vs_df['AST'] - avg_df['APG']
comp_df['STL'] =  vs_df['STL'] - avg_df['SPG']
comp_df['BLK'] =  vs_df['BLK'] - avg_df['BPG']
comp_df['FG%'] = (vs_df['FG%'] - avg_df['FG%'])*100
comp_df['3P%'] = (vs_df['3P%'] - avg_df['3P%'])*100
comp_df['FT%'] = (vs_df['FT%'] - avg_df['FT%'])*100

# lets see what that performance looks like
desc = comp_df.describe()
mean = desc[desc.index == 'mean'].T
mean.rename(columns={'mean':'All Games'}, inplace=True)

colorstring = ''
for val in mean['All Games']:
    if val < 0:
        colorstring += 'r'
    else:
        colorstring += 'g'

# And in the wins?
wins = (vs_df['WIN'] == 1)
desc = comp_df[wins].describe()
mean['In UAB Wins'] = desc[desc.index == 'mean'].T
colorstring2 = ''
for val in mean['In UAB Wins']:
    if val < 0:
        colorstring2 += 'r'
    else:
        colorstring2 += 'g'

# and the losses?
losses = ~wins
desc = comp_df[losses].describe()
mean['In UAB Losses'] = desc[desc.index == 'mean'].T

colorstring3 = ''
for val in mean['In UAB Losses']:
    if val < 0:
        colorstring3 += 'r'
    else:
        colorstring3 += 'g'

print(mean.plot(kind='bar',
               title='CUSA Opponent Peformance versus UAB',
               color=[colorstring, colorstring2, colorstring3],
               legend=False,
               ylim=(-7,5),
               subplots=True,
               sharey=True,
               sharex=True))


# plt.text(-1.5, .7, 'Deviation from season Avg', rotation='vertical')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.show()



