Features:

* Fetches real-time weather data from the OpenWeather API.
* Stores weather data in a SQLite database.
* Provides endpoints for performing CRUD (Create, Read, Update, Delete) operations on weather data.
* User-friendly web interface to view, add, update, and delete weather records.
* Responsive design for a seamless experience on both desktop and mobile devices.

Technologies Used:

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript

Installation: 

Clone the repository:
* git clone https://github.com/your-username/weather-app.git

Change into the project directory:
* cd weather-app

Create a virtual environment (recommended):
* python -m venv myenv

Activate the virtual environment:
On Windows:
* myenv\Scripts\activate

Install the required packages:
* pip install -r requirements.txt

Start the application:
* python app.py

Open your browser and navigate to http://localhost:5000 to access the Weather App.

Usage:
* On the homepage, you can view the existing weather records for different cities.
* To add a new weather record, fill in the city, state (optional), and country fields in the form and click "Add Weather".
* To update an existing weather record, click the "Update" button next to the respective record and enter the updated values in the prompt.
* To delete a weather record, click the "Delete" button next to the respective record.
The weather records will be dynamically updated on the page without requiring a refresh.
