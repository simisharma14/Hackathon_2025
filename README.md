# Hacklytics_2025
Green Thumb Investment Platform
Green Thumb is an innovative web application that delivers comprehensive stock analysis, sentiment insights, and AI-generated investment reports focused on the renewable energy sector. The platform gathers financial data from multiple APIs, leverages OpenAI's GPT models for report generation, and presents the information in a modern, user-friendly interface.

Features
Stock Profiles:
Detailed profiles for stocks including financial data (Market Cap, PE Ratio, EBITDA, etc.), historical price charts, and AI-generated stock reports.

Sentiment Analysis:
Market sentiment derived from news sources and financial data to gauge investor mood.

Investment Strategy:
Personalized investment strategies based on user risk tolerance and top-performing stocks.

ETF Breakdown:
Visualization and comparison of ETFs by energy subsector (Nuclear, Solar, Wind, Clean Energy, Hydrogen, etc.).

Macro Outlook:
Comprehensive AI-generated macro reports on the energy sector, including discussions on regulatory changes, market trends, and government policies.

Responsive UI:
Built using React, Material-UI, and Recharts, ensuring a modern and responsive user experience across devices.

Global User Context:
User preferences (e.g., name and risk tolerance) are stored globally and persist across pages.

Technologies Used
Backend:

Python, Flask, Pandas
OpenAI API (GPT-4 / GPT-3.5-turbo)
Yahoo Finance API, Polygon API
Flask-CORS
Frontend:

React
Material-UI
Recharts
Axios, React Router
Other:

dotenv (for environment variable management)
Installation
Backend
Clone the repository:

bash
Copy
git clone https://github.com/yourusername/GreenThumb.git
cd GreenThumb
Set up the Python environment:

Create and activate a virtual environment:

bash
Copy
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy
pip install -r requirements.txt
Configure environment variables:

Create a .env file in the backend directory with the following content:

dotenv
Copy
OPENAI_API_KEY=your_openai_api_key
POLYGON_API_KEY=your_polygon_api_key
Start the Flask server:

bash
Copy
python app.py
Frontend
Navigate to the frontend directory:

bash
Copy
cd frontend/hackathon-dashboard
Install dependencies:

bash
Copy
npm install
Start the React development server:

bash
Copy
npm start
Usage
Access the App:
Open your web browser and navigate to http://localhost:3000.

Navigation:
Use the sidebar to switch between pages:

Home:
Enter your name and select your risk tolerance.
Stock Profile:
Select a stock from the dropdown to view detailed financial data, charts, and an AI-generated report.
ETF Breakdown:
View visual comparisons of ETFs by energy subsector.
Top Performers:
See the highest-ranked stocks based on our financial analysis.
Macro Outlook:
Read a comprehensive outlook report for the energy sector.
Investment Strategy:
Receive a personalized investment strategy based on your risk tolerance and top-ranked stocks.
Project Structure
backend/
Contains the Flask server code, including API endpoints for stock data, sentiment analysis, financial metrics, AI-generated reports, and investment strategy.

frontend/
Contains the React application with components for stock profiles, ETF charts, dashboards, and global navigation.

data/
Directory for storing CSV files, AI-generated reports, and financial data.

.env
Contains environment variables (API keys).

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch for your changes.
Make your changes and commit them.
Submit a pull request.
License
This project is licensed under the MIT License.

Acknowledgements
Yahoo Finance API
Polygon.io
OpenAI
Material-UI
React
Special thanks to the hackathon organizers and contributors.
