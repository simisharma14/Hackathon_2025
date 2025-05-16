# 🌱 Green Thumb: AI-Driven Clean Energy Investment Platform

**Green Thumb** is an **AI-powered investment platform** designed to democratize access to **high-quality financial data and actionable insights** for retail investors—especially those interested in **clean energy and nuclear sectors**.  

By integrating **machine learning, sentiment analysis, and advanced financial modeling**, Green Thumb delivers:  
✅ **Comprehensive stock profiles**  
✅ **Personalized investment strategies**  
✅ **Macro outlook reports** tailored to the evolving clean energy landscape  

---

## Table of Contents  

- [Overview](#overview)  
- [Features](#features)  
- [Problem Statement & Background](#problem-statement--background)  
- [Data Sources](#data-sources)  
- [Project Architecture](#project-architecture)  
- [Setup & Installation](#setup--installation)
- [Contributors](#contributors)
- [Acknowledgements](#acknowledgements)

---

## Overview  

Green Thumb **leverages multiple data sources** such as **Yahoo Finance, Polygon.io, government regulatory data, and macroeconomic reports** to generate:  
- **Detailed financial profiles**  
- **Technical analysis charts**  
- **AI-generated reports** on stocks and ETFs in the clean energy space  

It also **performs sentiment analysis** from financial news and regulatory announcements to provide **forward-looking insights**.

---

## Features  

### **Stock & ETF Profiles**  
- **Company financials** (Balance Sheet, Income Statement, Cash Flows)  
- **AI-generated reports** combining historical data, metrics, and market sentiment  
- **Interactive charts** for stock price trends over multiple time horizons  

### **Investment Strategy**  
- **Personalized strategies** based on user risk tolerance  
- **Stock ranking system** using sentiment scores, financial ratios & technical indicators  

### **Macro Outlook**  
- **Energy sector macro reports**, integrating policy updates and regulatory shifts  
- **Real-time regulatory news analysis** affecting clean & nuclear energy  

### **User Experience**  
- **Modern UI** (React + Material-UI + Recharts)  
- **Global user context** stores preferences like risk tolerance  
- **Easy navigation** (Sidebar with Account, ETFs, Top Performers, Macro Reports, Strategy)  

---

## Problem Statement & Background  

### **Problem Statement**  

**Enhancing Investment Strategies in Clean Energy Amid Regulatory Uncertainty**  

The clean energy sector **faces uncertainty** due to:  
- **Shifting government policies**  
- **Fluctuating subsidies**  
- **Evolving environmental mandates**  

**Traditional investment analysis often overlooks** regulatory shifts and investor sentiment. Green Thumb **bridges this gap** by providing:  
✔️ **Data-driven AI-powered insights**  
✔️ **Comprehensive financial + qualitative analysis**  
✔️ **Objective, transparent stock recommendations**  

### **Background**  

- The clean energy sector (solar, wind, nuclear, hydrogen) is at a **critical juncture**.  
- **Retail investors** struggle with access to **institutional-grade** analysis tools.  
- **Green Thumb’s approach:** AI-powered financial modeling, sentiment analysis, and policy tracking.

---

## Data Sources  

**Stock & ETF Data:**  
- [Yahoo Finance API](https://finance.yahoo.com/)  
- [Polygon.io](https://polygon.io/)  

**Macro & Regulatory Data:**  
- U.S. Energy Information Administration (EIA)  
- International Renewable Energy Agency (IRENA)  
- Kaggle datasets on energy markets  

**News & Sentiment Analysis:**  
- Reuters, CNBC, Bloomberg, Seeking Alpha  
- Government filings & regulatory updates  
- Custom NLP web scrapers for macro news  

---

## Project Architecture  

### **Backend (Flask)**  
- **API server** for stock data, sentiment analysis & macro reports  
- **ML integration** with OpenAI & FinBERT for AI-generated insights  
- **Third-party APIs:** Yahoo Finance, Polygon.io, OpenAI  

### **Frontend (React)**  
- **Built with React + Material-UI + Recharts**  
- **Real-time financial charts** with smooth UI/UX  
- **Global state management** using React Context API  

---

## Setup & Installation  

### **Backend Setup (Flask)**  

```bash
# Clone the repository
git clone https://github.com/yourusername/GreenThumb.git
cd GreenThumb

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys (create a .env file)
echo "OPENAI_API_KEY=your_openai_api_key" >> .env
echo "POLYGON_API_KEY=your_polygon_api_key" >> .env

# Start the backend server
python app.py
```
### **Backend Setup (Flask)** 

```bash
cd frontend/hackathon-dashboard

# Install dependencies
npm install

# Start the development server
npm start
```

### **Contributors**

Simran Sharma (simisharma14), Jeslyn Guo (jeslyn-guo), Andrew Verzino (drewverzino), Chloe Nicola (chloen3).


### **Acknowledgements**

A special thanks to all those working toward making clean energy investments accessible and data-driven.
A special thanks to the organizers of Hacklytics 2025.




https://github.com/user-attachments/assets/22f3c336-e86c-4e11-8356-4f0c028dc5c9

