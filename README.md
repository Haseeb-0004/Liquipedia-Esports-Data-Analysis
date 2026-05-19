# Liquipedia – Esports Data Analysis

A Streamlit-based esports analytics dashboard that performs data analysis on competitive gaming datasets using Pandas and Plotly. The project provides insights into team performance, win rates, round efficiency, player statistics, and tournament predictions for esports events such as Counter-Strike.

The project also includes web scraping modules that collect esports data directly from Liquipedia using BeautifulSoup.

---

## Features

- Interactive Streamlit dashboard
- Team performance metrics analysis
- Team win rate visualization
- Round efficiency analysis
- Average rounds won/lost per stage
- Tournament winner prediction
- Player performance analysis
- Radar chart visualization for players
- Multi-year esports data analysis (2021–2024)
- Plotly-based interactive charts and graphs
- Web scraping system for collecting esports datasets

---

## Project Structure

```bash
├── app.py                                   # Main Streamlit application
├── headers.py                               # Data processing and visualization functions
├── requirements.txt                         # Project dependencies
├── README.md                                # Project documentation
│
├── Years/                                   # Contains yearly esports datasets
│   ├── 2021.csv
│   ├── 2022.csv
│   ├── 2023.csv
│   ├── 2024.csv
│   ├── AllYears.csv
│
├── Player Stats/                            # Player statistics datasets
│   ├── *.csv
│
├── Web Scrapping/                           # Web scraping notebooks
│   ├── scrapping-player_stats.ipynb
│   ├── scrapping-matches_data.ipynb
│
├── bin/
│   └── img/
│       ├── Counter-Strike.png
│       ├── Dota.png
```

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- BeautifulSoup
- Requests

---

## Data Collection

All datasets used in this project were collected from:

[:contentReference[oaicite:0]{index=0}](https://liquipedia.net/counterstrike/Main_Page)

The project uses **BeautifulSoup** and **Requests** libraries to scrape:
- Match statistics
- Team performance data
- Player statistics
- Tournament information

Web scraping notebooks are included inside the `Web Scrapping/` folder.

---

## How It Works

1. Esports data is scraped from Liquipedia using BeautifulSoup.
2. The scraped datasets are cleaned and stored as CSV files.
3. The Streamlit dashboard loads datasets dynamically for analysis.
4. Users can select:
   - Esports title
   - Analysis type
   - Tournament year
5. The system generates:
   - Interactive charts
   - Team performance metrics
   - Tournament predictions
   - Player radar analysis
6. Plotly visualizations are displayed directly in the dashboard.

---

## Analysis Modules

### Team Metrics
Displays:
- Average win rate
- Average round difference (RD)
- Playoff appearances

### Team Win Rate
Calculates and visualizes win rates for teams across tournament stages.

### Rounds Per Stage
Shows:
- Average rounds won
- Average rounds lost

### Round Efficiency
Ranks teams based on round efficiency percentages.

### Tournament Prediction
Predicts:
- Likely qualifying teams
- Top tournament winners

### Player Analysis
Provides:
- Radar chart visualization
- Average kills
- Average deaths
- Average assists
- Match-wise player statistics

---

## Supported Esports

- Counter-Strike
