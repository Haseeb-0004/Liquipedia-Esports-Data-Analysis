import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from difflib import get_close_matches
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load and process data for all years (2021 to 2024)
def load_data():
    # Loads and processes data for all years (2021 to 2024).# 
    data = {}  #dictionary banai
    for year in range(2021, 2025):  #2021 se 2024 tk loop chala rhy (for years)
        file_path = os.path.join(script_dir, "Years", f"{year}.csv")
        df = pd.read_csv(file_path) #csv read ki
        df.drop('Unnamed: 1', axis=1, inplace=True)  # Removing index column
        df.rename(columns={'Unnamed: 0': 'Stage'}, inplace=True)  # Required for prediction
        data[year] = df  #os year ka data osi year ki key me daal do

    return data #end me jab saare yeras ka df ban gya to ose return kar do


# Function to calculate team metrics   // app me call ho rha
def calculate_avg_metrics(df):
    # Calculates average team metrics for each team.# 
    team_stats = df.groupby('Team').apply(_calculate_team_metrics).reset_index()
    return team_stats

#plot of team metrics
def team_performance_chart(df):
    team_stats = df.groupby('Team').apply(_calculate_team_metrics).reset_index()
    team_stats['Playoff Appearances'] = team_stats['Playoff Appearances'].replace({0:0.3})
    fig = px.scatter(
    team_stats,
    y="Avg Win Rate",
    x="Avg RD",
    size="Playoff Appearances",
    color="Team",
    title="Teams Performance",
    labels={"Avg Win Rate": "Average Win Rate", "Avg RD": "Average RD"},
    template="plotly_dark"  
    )
    return fig


# Helper function to calculate metrics for a single team
def _calculate_team_metrics(group):
    # Helper function to calculate metrics for a single team group.# 
    total_wins = group['Matches'].apply(lambda x: int(x.split('-')[0])).sum() #matches wala column utha k osme 3-1 3 aur 1 ko split kar dia
    total_losses = group['Matches'].apply(lambda x: int(x.split('-')[1])).sum()
    total_matches = total_wins + total_losses
    avg_win_rate = total_wins / total_matches
    avg_rd = group['RD'].mean()
    stages = group['Stage'].tolist()
    playoff_appearances = stages.count('Playoff Stage')
    return pd.Series({  #it allows all these metrics to be returned together as a single object
        'Avg Win Rate': avg_win_rate,
        'Avg RD': avg_rd,
        'Playoff Appearances': playoff_appearances
    })


# Function to predict likely qualifiers and winners based on metrics
def predict_outcome( playoff_threshold=2, win_rate_threshold=0.4):
    #Predicts and displays likely qualifiers and winners based on metrics for each year (2021 to 2024).
    all_years_path = os.path.join(script_dir, "Years", "AllYears.csv")
    df = pd.read_csv(all_years_path)
    team_stats = df.groupby('Team',group_keys=False).apply(calculate_avg_metrics).reset_index()

    likely_qualifiers = team_stats[
        (team_stats['Playoff Appearances'] >= playoff_threshold) &
        (team_stats['Avg Win Rate'] >= win_rate_threshold)
    ]
    
    likely_winners = likely_qualifiers.sort_values(by=['Avg RD', 'Avg Win Rate'], ascending=False).head(3)
    
    likely_qualifiers = likely_qualifiers['Team'].tolist()
    likely_winners =  likely_winners['Team'].tolist()

    #plotting
    top_teams = team_stats[team_stats['Team'].isin(likely_winners)]

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Average Win Rate", "Average RD", "Playoff Appearances"),
        horizontal_spacing=0.1
    )

    fig.add_trace(
        go.Bar(
            x=top_teams["Team"],
            y=top_teams["Avg Win Rate"],
            name="Avg Win Rate",
            marker=dict(color="lightblue"),
            width=0.6
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=top_teams["Team"],
            y=top_teams["Avg RD"],
            name="Avg RD",
            marker=dict(color="lightgreen"),
            width=0.6
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(
            x=top_teams["Team"],
            y=top_teams["Playoff Appearances"],
            name="Playoff Appearances",
            marker=dict(color="lightcoral"),
            width=0.6
        ),
        row=1, col=3
    )

    fig.update_layout(
        title="Top 3 Predicted Winners - Performance Metrics",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        height=500,
        width=1100,
    )

    return likely_qualifiers , likely_winners , fig


# Function to calculate win rate for each match  // app me call hua hai
def call_cal_win_rate(df):
    # Adds Win Rate and Win Rate % columns to the DataFrame and displays them.# 
    if 'Win Rate' not in df.columns:
        df['Win Rate'] = df.apply(calculate_win_rate, axis=1)

    df['Win Rate %'] = (df['Win Rate'] * 100).apply(lambda x: f"{x:.0f}%")

    # stage_counts = df['Stage'].value_counts().reset_index()
    # stage_counts.columns = ['Stage', 'Count']

    fig= px.bar(df, 
        x='Win Rate', 
        y='Team', 
        title='Win Rate Per Stage', 
        labels={'Win Rate': 'Win Rate', 'Team': 'Team' , 'Stage' : df['Stage']}, 
        color='Win Rate', 
        color_continuous_scale='Viridis', 
        orientation='h', 
        template="plotly_dark"
    )

    return df[['Stage','Team', 'Win Rate %']] , fig


# HELPER Function to calculate win rate from Matches column 
def calculate_win_rate(row):
    # Calculates the win rate from the Matches column.# 
    wins = int(row['Matches'].split('-')[0])
    losses = int(row['Matches'].split('-')[1])
    total_matches = wins + losses
    return wins / total_matches


# Function to calculate total rounds won and lost per match  // app me call kia hai
def rounds_per_game(df):
    # Calculates and displays columns for average rounds won/lost per match.# 
    if not 'Total Matches' in df.columns:
        df['Total Matches'] = df.apply(total_matches, axis=1)
    if 'Rounds Won' or 'Rounds Lost' not in df.columns:
        df['Rounds Won'] = df['Rounds'].str.split('-').str[0].astype(int)
        df['Rounds Lost'] = df['Rounds'].str.split('-').str[1].astype(int)
    df['Avg Rounds Won'] = (df['Rounds Won'] / df['Total Matches']).astype(int)
    df['Avg Rounds Lost'] = (df['Rounds Lost'] / df['Total Matches']).astype(int)

    fig = px.bar(
    df,
    x="Team",
    y=["Avg Rounds Won", "Avg Rounds Lost"],
    title="Average Rounds Won and Lost per Team",
    labels={"value": "Average Rounds", "variable": "Metric"},
    barmode="group",
    template="plotly_dark"
    )

    # return df[['Team', 'Avg Rounds Won', 'Avg Rounds Lost']]
    return df , fig

# Function to calculate total matches played
def total_matches(row):
    # Calculates total matches played from the Matches column.# 
    wins = int(row['Matches'].split('-')[0])
    losses = int(row['Matches'].split('-')[1])
    return wins + losses


# Function to calculate and display round efficiency ranking // app me call hua hai
def rounds_efficiency(df):
    # Calculates and displays round efficiency ranking.# 
    if 'Rounds Won' or 'Rounds Lost' not in df.columns:
        df['Rounds Won'] = df['Rounds'].str.split('-').str[0].astype(int)
        df['Rounds Lost'] = df['Rounds'].str.split('-').str[1].astype(int)
    df['Total Rounds Played'] = df['Rounds Won'] + df['Rounds Lost']
    df['Round Efficiency'] = df['Rounds Won'] / df['Total Rounds Played']
    df['Round Efficiency %'] = (df['Round Efficiency'] * 100).apply(lambda x: f"{x:.2f}%")

    fig = px.bar(
        df,
        x='Round Efficiency',
        y='Team',
        title='Teams Ranked by Round Efficiency',
        labels={'Round Efficiency': 'Round Efficiency', 'Team': 'Teams'},
        color='Round Efficiency', 
        color_continuous_scale='Viridis',
        orientation='h',
        template="plotly_dark"
    )
    return df[['Stage','Team', 'Round Efficiency %']] , fig


# Function to display top 3 teams by Win Rate
def Winners_of_each_stage(df):
    # Displays the top 3 teams by Win Rate.# 
    if 'Win Rate' not in df.columns:
        df['Win Rate'] = df.apply(calculate_win_rate, axis=1)

    top_3_teams = df.sort_values(by='Win Rate', ascending=False).head().reset_index()
    top_3_teams['Win Rate'] = (top_3_teams['Win Rate'] * 100).apply(lambda x: f"{x:.0f}%")
    return top_3_teams[['Stage','Team', 'Win Rate']]


def playersearch(name):
    player_stats_path = os.path.join(script_dir, "Player Stats", "*.csv")
    csv_files = glob.glob(player_stats_path)
    target_name = name.lower()  # lowercasing the name input

    total_kills, total_deaths, total_assists, total_adr = 0, 0, 0, 0
    total = 0

    for file in csv_files:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()

        df['Name'] = df['Name'].astype(str).str.lower().str.strip()
        filtered_row = df[df["Name"] == target_name]

        if not filtered_row.empty:
            total_kills += filtered_row["Kills"].iloc[0] 
            total_deaths += filtered_row["Deaths"].iloc[0]  
            total_assists += filtered_row["Assists"].iloc[0]  
            total_adr += filtered_row["ADR"].iloc[0]  
            total += 1

    if total > 0:
        avg_kills = round(total_kills / total)
        avg_deaths = round(total_deaths / total)
        avg_assists = round(total_assists / total)
        return avg_kills, avg_deaths, avg_assists
    else:
        return None  

def did_you_mean(name):
    player_stats_path = os.path.join(script_dir, "Player Stats", "*.csv")
    csv_files = glob.glob(player_stats_path)
    name = name.lower()  # lowercasing the name input

    for file in csv_files:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()

        df['Name'] = df['Name'].astype(str).str.lower().str.strip()
        filtered_row = df["Name"].tolist()

        close_matches = get_close_matches(name, filtered_row, n=1, cutoff=0.6)
    
        if close_matches:
            return f"Did you mean '{close_matches[0]}'?"
        
    else:
        return "No close match found."

# Function to generate and display radar chart for a player
def display_radar_chart(name):

    stats = playersearch(name)

    if stats is None:
        return None

    avg_kills, avg_deaths, avg_assists = stats

    labels = ['Kills', 'Deaths', 'Assists']
    values = [avg_kills, avg_deaths, avg_assists]
    values += values[:1]  # closing the loop [5 , 10 , 15 , 5]
    labels += labels[:1]  # closing the loop 
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=name,
        line=dict(color='red'),
        marker=dict(size=8, color='red'),
        showlegend=True,
        hovertemplate='%{r}<extra></extra>', #r==placeholder , extra me additional info daal sakte jo k nhi daalni thi
        hoverlabel=dict(
            bgcolor="black",  
            font=dict(color='cyan', size=15)
        )
    ))

    fig.update_layout(
        polar=dict(   # circular data dikhaane k liye as we were using spider charts
            bgcolor='black',
            angularaxis=dict(
                linewidth=2,
                linecolor='gray',
                gridcolor='gray',
                showgrid=True,
                tickfont=dict(size=14, color='cyan'),
            ),
            radialaxis=dict(
                gridcolor='gray',
                showline=False,
                range=[0, 50],
                tickfont=dict(color='black'),
            )
        ),
        paper_bgcolor='black',
    )

    fig.update_layout(
        annotations=[
            dict(
                x=1.05,  
                y=0.78,
                text=f'• Average Kills: {avg_kills}',
                showarrow=False,
                font=dict(size=14, color='cyan'),
            ),
            dict(
                x=1.05,
                y=0.65,
                text=f'• Average Deaths: {avg_deaths}',
                showarrow=False,
                font=dict(size=14, color='cyan'),
            ),
            dict(
                x=1.05,
                y=0.55,
                text=f'• Average Assists: {avg_assists}',
                showarrow=False,
                font=dict(size=14, color='cyan'),
            )
        ]
    )

    return fig

def player_details_perMatch(name):

    player_stats_path = os.path.join(script_dir, "Player Stats", "*.csv")
    csv_files = glob.glob(player_stats_path)
    target_name = name.lower() 

    i=1
    result = {}

    for file in csv_files:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()  

        df['Name'] = df['Name'].astype(str).str.lower().str.strip()

        filtered_row = df[df["Name"] == target_name]
        
        if not filtered_row.empty:
            result[f"Match {i}"] = filtered_row.iloc[0]
            i+=1
    
    return result
    

