# algorithm.py

import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

def create_df_image(df):
    norm = matplotlib.colors.Normalize(-1, 1)

    colors = [
        [norm(-1), "white"],
        [norm(1), "blue"]
    ]

    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "", colors
    )

    fig, ax = plt.subplots()

    sns.heatmap(
        df,
        annot=True,
        cmap=cmap,
        cbar=False,
        ax=ax
    )

    return fig

def generate_teams(num_players, num_teams):
    base_size, extra = divmod(num_players, num_teams)

    teams = []
    for team in range(1, num_teams + 1):
        size = base_size + (1 if team <= extra else 0)
        teams.extend([team] * size)

    return teams

def summarize_teams(df):
    summary_df = df.groupby('Team')[
        ['Gender', 'Height', 'Serve', 'Receive', 'Set', 'Hit',
        'Reaction', 'Consistency', 'Comms', 'Skill']
    ].mean()

    summary_df = summary_df.round(2)

    team_names_dict = df.groupby('Team')['Name'].apply(list).to_dict()
    team_names_df = pd.DataFrame({
        f'Team {team}': pd.Series(names)
        for team, names in team_names_dict.items()
    })

    team_names_df.fillna('', inplace=True)

    return summary_df, team_names_df

def binary_team_algorithm(df):
    df.sort_values(['Gender', 'Height', 'Skill'], ascending=[False, False, False], inplace=True)
    df['Rank'] = range(1, len(df) + 1)
    df['Reversed'] = df.Rank.apply(lambda x: int(f'{x:06b}'[::-1], 2))

    df.sort_values(by='Reversed', ascending=True, inplace=True)
    new_df = df.copy()
    return new_df

def create_teams(df, num_of_teams):

    df = binary_team_algorithm(df)

    df['Team'] = generate_teams(len(df), num_of_teams)

    summarized_df, team_names_df = summarize_teams(df)
    new_df = df.copy()

    return summarized_df, team_names_df, new_df