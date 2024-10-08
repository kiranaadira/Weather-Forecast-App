import datetime
from io import BytesIO

import requests
import json
import matplotlib.pyplot as plt
import numpy as np

from tkinter import *
from PIL import ImageTk, Image

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title('Weather App')
        master.geometry('600x600+450+100')
        master.resizable(0, 0) # Disable window resizing
        master.configure(bg='#A7D3E0')

        # Header label
        self.header_label = Label(
            text="WEATHER FORECAST APP",
            font=('constantia', 25, 'bold', 'underline'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.header_label.place(relx=0.5, rely=0.1, anchor='center')

        # City input label and entry
        self.city_label = Label(
            master,
            text='Enter city name:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        ) 
        self.city_label.place(relx=0.5, rely=0.2, anchor='center')

        self.city_entry = Entry(
            master,
            bg='#FFFFFF',
            fg='#000000',
            highlightthickness=0,
            font=('constantia', 13, 'bold'),
            justify=CENTER
        )
        self.city_entry.place(relx=0.5, rely=0.25, anchor='center')

        # Submit button
        self.submit_button = Button(
            master,
            text='Get Weather',
            command=self.get_weather,
            bg='#A7D3E0',
            fg='#000000',
            highlightthickness=0,
            highlightbackground='#A7D3E0',
            font=('constantia', 13, 'bold')
        )
        self.submit_button.place(relx=0.5, rely=0.3, anchor='center')

        # Label frame to display weather information
        self.label_frame = Frame(master, bg='#A7D3E0')
        self.label_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Labels for weather information
        self.date_label = Label(
            self.label_frame,
            text='Date:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.date_label.pack(pady=5)

        self.weather_label = Label(
            self.label_frame,
            text='Weather:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.weather_label.pack(pady=5)

        self.temperature_label = Label(
            self.label_frame,
            text='Temperature:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.temperature_label.pack(pady=5)

        self.humidity_label = Label(
            self.label_frame,
            text='Humidity:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.humidity_label.pack(pady=5)

        self.wind_label = Label(
            self.label_frame,
            text='Wind Speed:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.wind_label.pack(pady=5)

        self.pressure_label = Label(
            self.label_frame,
            text='Pressure:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.pressure_label.pack(pady=5)

        # Label for weather forecast icon
        self.weather_icon_label = Label(
            master,
            text='Today\'s Weather Forecast:',
            font=('constantia', 13, 'bold'),
            bg='#A7D3E0',
            fg='#333333'
        )
        self.weather_icon_label.place(relx=0.5, rely=0.725, anchor='center')

        # Frame to display weather forecast icons and times
        self.forecast_frame = Frame(master, bg='#A7D3E0')
        self.forecast_frame.place(relx=0.5, rely=0.8, anchor='center')

        # Button to show weekly weather forecast chart
        self.chart_button = Button(
            master,
            text='Weekly Temperature Forecast',
            command=self.show_weather_chart,
            bg='#A7D3E0',
            fg='#000000',
            highlightthickness=0,
            highlightbackground='#A7D3E0',
            font=('constantia', 13, 'bold')
        )
        self.chart_button.place(relx=0.5, rely=0.9, anchor='center')

        # Weather forecast icon labels and time labels
        self.weather_icon_labels = []
        self.weather_time_labels = []

        for i in range(5):
            icon_label = Label(self.forecast_frame, bg='#A7D3E0')
            icon_label.grid(row=0, column=i, padx=5)
            self.weather_icon_labels.append(icon_label)

            time_label = Label(self.forecast_frame, text='', bg='#A7D3E0', font=('constantia', 13, 'bold'))
            time_label.grid(row=1, column=i, padx=5)
            self.weather_time_labels.append(time_label)

    def retrieve_forecast_data(self, city_name):
        try:
            api_key = '57df4a2667df52b68331072c518c20f5'
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric'
            response = requests.get(url)
            forecast_data = json.loads(response.content)
            return forecast_data
        except requests.exceptions.RequestException as e:
            print(f'Error retrieving forecast data: {e}')
            return None
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON response: {e}')
            return None

    def get_weather(self):
        city_name = self.city_entry.get()
        forecast_data = self.retrieve_forecast_data(city_name)

        try:
            if 'list' in forecast_data:
                forecast = forecast_data['list'][:5]

                if len(forecast) >= 5:
                    current_time = datetime.datetime.now()
                    self.date_label.config(text=f'Date: {current_time.strftime("%H:%M %d-%m-%Y")}') # Tanggal
                    self.weather_label.config(text=f'Weather: {forecast[0]["weather"][0]["description"]}') # Keterangan Cuaca
                    self.temperature_label.config(text=f'Temperature: {forecast[0]["main"]["temp"]}°C') # Suhu
                    self.humidity_label.config(text=f'Humidity: {forecast[0]["main"]["humidity"]}%') # Kelembaban
                    self.wind_label.config(text=f'Wind Speed: {forecast[0]["wind"]["speed"]} m/s') # Kecepatan Angin
                    self.pressure_label.config(text=f'Pressure: {forecast[0]["main"]["pressure"]} hPa') # Tekanan Udara

                    icons = [entry['weather'][0]['icon'] for entry in forecast]
                    time = [datetime.datetime.fromisoformat(entry['dt_txt']) for entry in forecast]

                    for i in range(5):
                        current_time = datetime.datetime.now() + datetime.timedelta(hours=i)
                        self.set_weather_icon(icons[i], self.weather_icon_labels[i], 35)
                        self.weather_time_labels[i].config(text=current_time.strftime('%H:%M'))
                else:
                    current_time = datetime.datetime.now()
                    self.date_label.config(text=f'Tanggal: {current_time.strftime("%H:%M %d-%m-%Y")}')
                    self.weather_label.config(text='Insufficient forecast data')
                    self.temperature_label.config(text='')
                    self.humidity_label.config(text='')
                    self.wind_label.config(text='')
                    self.pressure_label.config(text='')

                    for label in self.weather_icon_labels:
                        label.config(image='', bg='#A7D3E0')
                    for label in self.weather_time_labels:
                        label.config(text='')
            else:
                current_time = datetime.datetime.now()
                self.date_label.config(text=f'Tanggal: {current_time.strftime("%H:%M %d-%m-%Y")}')
                self.weather_label.config(text='Unable to retrieve data')
                self.temperature_label.config(text='')
                self.humidity_label.config(text='')
                self.wind_label.config(text='')
                self.pressure_label.config(text='')

                for label in self.weather_icon_labels:
                    label.config(image='', bg='#A7D3E0')
                for label in self.weather_time_labels:
                    label.config(text='')
        except TypeError:
            current_time = datetime.datetime.now()
            self.date_label.config(text=f'Tanggal: {current_time.strftime("%H:%M %d-%m-%Y")}')
            self.weather_label.config(text='An error occurred while processing the forecast data.')
            self.temperature_label.config(text='')
            self.humidity_label.config(text='')
            self.wind_label.config(text='')
            self.pressure_label.config(text='')

            for label in self.weather_icon_labels:
                label.config(image='', bg='#A7D3E0')
            for label in self.weather_time_labels:
                label.config(text='')

    def set_weather_icon(self, icon, label, size):
        response = requests.get(f'http://openweathermap.org/img/w/{icon}.png')
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((size, size)))
        label.config(image=img, bg='#A7D3E0')
        label.image = img

    def show_weather_chart(self):
        city_name = self.city_entry.get()
        forecast_data = self.retrieve_forecast_data(city_name)

        if 'list' in forecast_data:
            forecast = forecast_data['list']

            if len(forecast) >= 40:
                dates = []
                min_temperatures = []
                max_temperatures = []

                for entry in forecast:
                    date = datetime.datetime.fromisoformat(entry['dt_txt']).date() # Extract the date from the forecast entry timestamp
                    min = entry['main']['temp_min']
                    max = entry['main']['temp_max']
                
                    # Check if data for the current date already exists
                    if date in dates:
                        index = dates.index(date) # index is the position of the current date in the dates list
                        # Update minimum and maximum temperatures if necessary
                        if min < min_temperatures[index]: # Update the minimum temperature if the current minimum is lower
                            min_temperatures[index] = min
                        if max > max_temperatures[index]:
                            max_temperatures[index] = max # Update the maximum temperature if the current maximum is higher
                    else:
                        dates.append(date)
                        min_temperatures.append(min)
                        max_temperatures.append(max)

                hasil_max = np.round(max_temperatures, 2)
                hasil_min = np.round(min_temperatures, 2)

                x = np.arange(len(dates))  # Posisi x-axis untuk setiap tanggal
                width = 0.35

                fig, ax = plt.subplots()
                ax.bar(x - width/2, min_temperatures, width, label='Suhu Min', color='blue')
                ax.bar(x + width/2, max_temperatures, width, label='Suhu Max', color='green')

                ax.set_xlabel('Tanggal')
                ax.set_ylabel('Suhu (°C)')
                ax.set_title(f'Weekly Temperature Forecast - {city_name}')
                ax.set_xticks(x)
                ax.set_xticklabels(dates, rotation=45)
                ax.legend()

                # Menampilkan nilai suhu di atas setiap bar
                for i in range(len(dates)):
                    ax.text(x[i] - width/2, min_temperatures[i] + 1, float(hasil_min[i]), ha='center', fontsize=8)
                    ax.text(x[i] + width/2, max_temperatures[i] + 1, float(hasil_max[i]), ha='center', fontsize=8)

                plt.tight_layout()
                plt.show()

root = Tk()
app = WeatherApp(root)
root.mainloop()