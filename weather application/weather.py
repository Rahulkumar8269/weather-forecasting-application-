import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
                font-size: 14px;
            }
            QLabel, QPushButton {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: "Segoe UI Emoji";
            }
            QLabel#description_label {
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "339e99a7bbc34f967f985e19032d6277"
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name.")
            return
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get('message', 'An error occurred.'))
        except requests.RequestException as e:
            self.display_error(f"Network error: {str(e)}")

    def display_error(self, message):
        self.temperature_label.setText("")
        self.emoji_label.setText("❌")
        self.description_label.setText(message)

    def display_weather(self, data):
        temp = data['main']['temp']
        description = data['weather'][0]['description'].capitalize()
        
        # Set temperature
        self.temperature_label.setText(f"{temp:.1f}°C")
        
        # Set description
        self.description_label.setText(description)
        
        # Set emoji based on weather
        emoji = self.get_weather_emoji(description.lower())
        self.emoji_label.setText(emoji)

    def get_weather_emoji(self, description):
        if 'clear' in description:
            return "☀️"
        elif 'cloud' in description:
            return "☁️"
        elif 'rain' in description:
            return "🌧️"
        elif 'snow' in description:
            return "❄️"
        elif 'thunder' in description:
            return "⛈️"
        elif 'mist' in description or 'fog' in description:
            return "🌫️"
        else:
            return "🌤️"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())