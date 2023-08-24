🌤 Weather App

Dive into meteorological insights with the Weather Comparison App. Built using the robust Django framework, this application seamlessly fetches and displays weather metrics for cities worldwide, offering users a meticulous comparative analysis.

🌟 Features

Dual City Input: Users can juxtapose the climatic conditions of two cities simultaneously.
Dynamic 5-day Forecast: The app extends its functionality beyond current conditions, giving users a glimpse of the week ahead.
Interactive UI: Featuring intuitive controls and vibrant icons that bring the forecast to life.

🛠️ Tech Stack

Django 4.1
OpenWeatherMap API
SQLite (Default Django database)
Bootstrap (For UI components)

🚀 Getting Started

Prerequisites
Python 3.x
Pip (Python Package Installer)

Installation Steps

Clone the Repository:
git clone https://github.com/yourusername/weather_project.git
cd weather_project

Virtual Environment Setup (Highly recommended to keep dependencies clean):
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Dependency Installation:
pip install -r requirements.txt  # Ensure you have a requirements.txt file listing all dependencies

Set Up Environment Variables:
Create a .env file in the project root.
Add your OpenWeatherMap API key and Django SECRET_KEY like so:
OPEN_WEATHER_MAP_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
Note: Obtain your own OpenWeatherMap API key from the official site if you haven't already.

Migrate the Database:
python3 manage.py migrate

Fire Up the Development Server:
python3 manage.py runserver

Accessing the Web App:
Simply open your preferred browser and navigate to:
http://localhost:8000/

📘 Usage Guide

City Selection: Use the input fields on the homepage to enter the names of the cities you're keen on comparing.
Data Presentation: Upon pressing "Compare," the application fetches the requisite data and renders it in an aesthetically pleasing format, presenting current conditions along with a comprehensive 5-day forecast.

🤝 Contributing

We encourage you to contribute to Weather Comparison App! Please check out the Contributing guidelines for guidelines about how to proceed.

📄 License

This project is licensed under the MIT License.
