# Data Analysis Project

This is a Django project that fetches weather data from an API, visualizes the data, and performs data analysis on it.
Deployed web-site here: http://ec2-15-222-246-250.ca-central-1.compute.amazonaws.com

## Features

- Fetches weather data from the API and stores it in the database.
- Visualizes the weather data using plots and charts.
- Performs data analysis on the weather data, including descriptive statistics and correlation analysis.
- Allows users to interact with the weather data through a web interface.

## Installation

1. Clone the repository:

   git clone [https://github.com/your-username/weather-analysis.git](https://github.com/YaleDevUni/data_analyzer.git)

2. Create and activate a virtual environment:

   python -m venv myenv
   source myenv/bin/activate

3. Install the project dependencies:

   pip install -r requirements.txt

4. Set up the database by running migrations:

   python manage.py migrate

5. Start the Django development server:

   python manage.py runserver

6. Access the application in your web browser at http://localhost:8000.

## Usage

- The homepage displays the current weather data fetched from the API.
- Click on the "Fetch Data" button to fetch new weather data from the API and store it in the database.
- Navigate to the "Visualize Data" page to view plots and charts representing the weather data.
- Explore the "Data Analysis" page to see descriptive statistics and correlation analysis of the weather data.

## Project Structure

- weatherapp/: Django application directory.
  - models.py: Defines the database models for weather data.
  - views.py: Contains the views and logic for handling HTTP requests.
  - templates/: Contains the HTML templates for rendering the web pages.
  - static/: Stores static files such as CSS stylesheets and JavaScript scripts.

## Credits

- The weather data is fetched from the WeatherAPI (https://www.weatherapi.com/).
- This project uses the Django web framework (https://www.djangoproject.com/).

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
