# Green Thumb: AI-Driven Clean Energy Investment Platform

Green Thumb is an AI-powered investment platform designed to democratize access to high-quality financial data and actionable insights for retail investors—especially those interested in the clean energy and nuclear sectors. By integrating machine learning, sentiment analysis, and advanced financial modeling, Green Thumb delivers comprehensive stock profiles, personalized investment strategies, and macro outlook reports tailored to the evolving landscape of clean energy investments.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Problem Statement & Background](#problem-statement--background)
- [Data Sources](#data-sources)
- [Project Architecture](#project-architecture)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Green Thumb leverages multiple data sources—such as Yahoo Finance, Polygon.io, government regulatory data, and macroeconomic reports—to generate detailed financial profiles, technical analysis charts, and AI-generated reports for stocks and ETFs within the clean energy space. The platform also includes sentiment analysis from financial news and regulatory announcements, providing investors with a forward-looking perspective.

---

## Features

- **Stock & ETF Profiles**
  - Detailed company profiles with balance sheets, income statements, cash flows, and advanced financial metrics.
  - AI-generated stock reports that combine historical data, financial metrics, and market sentiment.
  - Interactive charts showing stock price movement for various time horizons (day, week, year, all time).

- **Investment Strategy**
  - Personalized investment strategies based on user risk tolerance.
  - Aggregation of sentiment scores, financial ratios, and technical indicators to rank stocks.
  
- **Macro Outlook**
  - Comprehensive macro outlook reports for the energy sector, integrating policy updates and regulatory changes.
  - Emphasis on current events and regulatory news affecting clean and nuclear energy.

- **User Experience**
  - Modern, responsive UI built with React, Material-UI, and Recharts.
  - Global user context stores user preferences (e.g., name, risk tolerance) across all pages.
  - Sidebar navigation with account management, ETF breakdown, top performers, macro outlook, and personalized strategy.

---

## Problem Statement & Background

### Problem Statement

**Enhancing Investment Strategies in Clean Energy Amid Regulatory Uncertainty**  
The clean energy industry is rapidly evolving with technological advances, yet investors face uncertainty due to shifting government policies, fluctuating subsidies, and evolving environmental mandates. Traditional financial analysis often overlooks the impact of investor sentiment and policy changes. Green Thumb aims to bridge this gap by providing a data-driven, AI-powered approach that integrates both quantitative metrics and qualitative insights to inform investment decisions.

### Background

- **Industry Context:**  
  The clean energy sector—including solar, wind, nuclear, and hydrogen—is at a crossroads. Despite growing demand and technological breakthroughs, the sector remains highly sensitive to regulatory and policy changes.
  
- **Investment Challenges:**  
  Retail investors traditionally lack access to institutional-grade tools and analysis, making it difficult to assess the true potential of clean energy investments.
  
- **Our Approach:**  
  By combining historical stock data, advanced financial metrics, sentiment analysis from regulatory news and market articles, and machine learning forecasts, Green Thumb provides actionable insights to empower retail investors with transparent, objective recommendations.

---

## Data Sources

Potential data sets and APIs include:

- **Stock & ETF Data:**
  - [Yahoo Finance API](https://finance.yahoo.com/)
  - [Polygon.io](https://polygon.io/)
  - [Alpha Vantage](https://www.alphavantage.co/)
  - [Quandl](https://www.quandl.com/)

- **Financial Performance & Investment Data:**
  - SEC EDGAR
  - Morningstar
  - Crunchbase & CB Insights

- **Macro & Regulatory Data:**
  - U.S. Energy Information Administration (EIA)
  - International Renewable Energy Agency (IRENA)
  - Kaggle datasets on energy crises and stock prices

- **News & Sentiment:**
  - Financial news outlets (Reuters, CNBC, Bloomberg, Seeking Alpha)
  - Government regulatory filings
  - Custom web scrapers for regulatory and macroeconomic articles

---

## Project Architecture

- **Backend (Flask):**
  - Serves API endpoints to fetch stock profiles, historical price data, sentiment analysis, and macro outlook reports.
  - Integrates with third-party APIs (Yahoo Finance, Polygon, OpenAI).
  - Uses Pandas for data aggregation and manipulation.
  - Implements CORS to enable frontend access.

- **Frontend (React):**
  - Built with React and Material-UI.
  - Uses Recharts for interactive financial charts.
  - Global state is managed via a custom React Context.
  - Provides routing for pages like Home, Stock Profile, ETF Breakdown, Macro Outlook, and Investment Strategy.

- **AI & Sentiment Analysis:**
  - Utilizes OpenAI’s GPT models to generate stock and macro reports.
  - Incorporates sentiment analysis models (e.g., FinBERT) for real-time news evaluation.

---

## Setup & Installation

### Backend

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/GreenThumb.git
   cd GreenThumb

2. **Set Up a Python Virtual Environment:**
  '''bash 
  python3 -m venv venv
  source venv/bin/activate

3. **Install Dependencies:**
  '''bash
  pip install -r requirements.txt

4. **Configure Environment Variables:**
  Create a .env file in the backend directory with:
  dotenv
  OPENAI_API_KEY=your_openai_api_key
  POLYGON_API_KEY=your_polygon_api_key

5. **Start the Flask Server:**
  '''bash
  python app.py

Frontend
Navigate to the Frontend Directory:

bash
Copy
cd frontend/hackathon-dashboard
Install Dependencies:

bash
Copy
npm install
Start the React Development Server:

bash
Copy
npm start
Usage
Access the App:
Open your web browser and navigate to http://localhost:3000.

Navigation:

Landing Page: Enter your name and risk tolerance.
Home: View a list of stocks (dropdown) and access detailed profiles.
Stock Profile: Access comprehensive financial data, interactive stock movement charts, and AI-generated reports.
ETF Breakdown & Macro Outlook: View comparative charts and market trends.
Project Structure
backend/
Contains the Flask server code, API endpoints, data processing scripts, and AI integration.

frontend/
Contains the React application, including components, pages, and styles.

data/
Stores CSV files, AI-generated reports, and financial data used by the application.

.env
Contains sensitive environment variables (API keys).

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch for your changes.
Commit your changes.
Submit a pull request with a detailed description of your changes.
License
This project is licensed under the MIT License.

Acknowledgements
APIs & Data Sources:
Yahoo Finance, Polygon.io, SEC EDGAR, EIA, IRENA, Kaggle
Tools & Libraries:
React, Material-UI, Recharts, Flask, Pandas, OpenAI
Special Thanks:
To the hackathon organizers, contributors, and open-source communities for their support.
