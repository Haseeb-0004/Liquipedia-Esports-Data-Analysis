import streamlit as st
from headers import *
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout="wide")

col1, col2 , col3 = st.columns([1, 0.4, 3])


with col1:
    st.header("Esports")
    
    # Dropdown Menu for selecting esports
    esports_option = st.selectbox(
        "Select an Esport game:",
        ["Select", "Counter-Strike", "Dota 2"]
    )

    if esports_option == "Counter-Strike":
        st.write("You selected Counter-Strike!")

        # Dropdown for selecting Counter-Strike data analysis type
        cs_option = st.selectbox(
            "Select Counter-Strike data analysis type:",
            ["Select Data", "Teams Metrics", "Teams Win Rate", "Rounds Per Stage","Round Efficiency", 
             "Winners Of Each Stage" , "Prediction" , "Player Analysis"]
        )

        # Load data for all years
        data = load_data()

        # Year selection dropdown for each analysis section
        if cs_option == "Prediction" or cs_option == "Player Analysis":
            year_option = st.selectbox("Select Year:",['ALL'])
        else:
            year_option = st.selectbox("Select Year:", [ 2021, 2022, 2023, 2024 ])

st.markdown(
    "<hr style='border: 0.5px solid red;'>",
    unsafe_allow_html=True
)

with col2:
   st.markdown(
    """
    <style>
    .vertical-line {
        border-left: 1px solid red;
        height: 110vh;
    }
    </style>
    <div class="vertical-line"></div>
    """,
    unsafe_allow_html=True
)
    
with col3:
    
    if esports_option == "Dota 2":
        dota_logo_path = os.path.join(script_dir, "bin", "img", "Dota.png")
        st.logo(dota_logo_path)
        st.write("Coming Soon...")

    if esports_option == "Counter-Strike":
        st.header("Counter-Strike Data Analysis")
        cs_logo_path = os.path.join(script_dir, "bin", "img", "Counter-Strike.png")
        st.logo(cs_logo_path)
        # Based on the option selected in the dropdown, call the respective function
        
        if year_option != 'ALL':
            df = data[year_option]

        if cs_option == "Teams Metrics":
            team_stats = calculate_avg_metrics(df)
            chart = team_performance_chart(df)
            st.subheader("Average Metrics for Each Team:")
            st.write(team_stats)
            if chart:
                st.plotly_chart(chart)

        elif cs_option == "Prediction":
            qualifiers , winner , chart = predict_outcome() 
            st.subheader("Teams Likely To Qualify: ")
            st.write(pd.DataFrame(qualifiers , columns=['Team']))
            st.subheader("Winner Prediction:")
            st.write(pd.DataFrame(winner , columns= ["Team"]))
            if chart:
                st.plotly_chart(chart)

        elif cs_option == "Teams Win Rate":
            win_rate_data , chart = call_cal_win_rate(df)
            st.write(win_rate_data)
            if chart:
                st.plotly_chart(chart)

        elif cs_option == "Rounds Per Stage":
            st.subheader("Average Rounds Per Stage")
            rounds_data , chart = rounds_per_game(df)
            st.write(rounds_data[[ 'Stage','Team', 'Avg Rounds Won', 'Avg Rounds Lost']])
            if chart:
                st.plotly_chart(chart)

        elif cs_option == "Round Efficiency":
            st.subheader("Teams Rounds Efficiency")
            round_efficiency_data  , chart = rounds_efficiency(df)
            st.write(round_efficiency_data)
            if chart:
                st.plotly_chart(chart)

        elif cs_option == "Winners Of Each Stage":
            st.subheader("Top 5 Winners Of Each Stage :")
            top_3_teams = Winners_of_each_stage(df)
            st.write(top_3_teams)

        elif cs_option == "Player Analysis":
            st.subheader("Enter Player Name for Analysis:")
            
            target_name = st.text_input("Enter Player Name :")

            if target_name: 
                radar_fig = display_radar_chart(target_name)
                if radar_fig:
                    player_details = player_details_perMatch(target_name)
                    player = pd.DataFrame(player_details)
                    # player = player.T
                    st.write(player)
                    st.plotly_chart(radar_fig)
                else:
                    st.write(f"{did_you_mean(target_name)}")

                