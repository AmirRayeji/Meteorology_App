from bs4 import BeautifulSoup as bs
import PySimpleGUI as sg
import requests


sg.theme('Black')

image_sec=sg.Column([[sg.Image('', key='-IMAGE-', visible=False)]])
info_sec=sg.Column([
    [sg.Text('', key='-LOCATION-', visible=False)],
    [sg.Text('', key='-TIME-', visible=False)],
    [sg.Text('', key='-TEMP-', visible=False)]
])


laye=[
    [sg.Input(key='-INPUT-', expand_x=True), sg.Button('برو', key='-GO-')],
    [image_sec, info_sec]
]


def get_weather(loc):
    url=f"https://www.google.com/search?q=weather+{loc.replace(' ','')}"
    session=requests.Session()
    session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    html=session.get(url)
    soup=bs(html.text, 'html.parser')
    name=soup.find('div', attrs={'id':'wob_loc'}).text
    time=soup.find('div', attrs={'id':'wob_dts'}).text
    weather=soup.find('span', attrs={'id':'wob_dc'}).text
    temp=soup.find('span', attrs={'id':'wob_tm'}).text

    return name, time, weather, temp


win=sg.Window('آب و هوا', layout=laye)

while True:
    events , Values = win.read()
    if events == sg.WINDOW_CLOSED:
        break
    
    if events == '-GO-':
        name, time, weather, temp=get_weather(Values['-INPUT-'])
        win['-LOCATION-'].update(name,visible=True)
        win['-TIME-'].update(time,visible=True)
        win['-TEMP-'].update(f'{temp}\u2103 {weather}',visible=True)

        if weather in ('Sun', 'Sunny', 'Clear', 'Clear with periodic clouds'):
            win['-IMAGE-'].update('Image/sun.png',visible=True)
        elif weather in ('Partly Sunny', 'Mostly Sunny', 'Partly cloudy', 'Mostly cloudy', 'Cloudy', 'Overcast'):
            win['-IMAGE-'].update('Image/part-sun.png',visible=True)
        elif weather in ('Rain', 'Chance of Rain', 'Light Rain', 'Showers', 'Scattered Showers', 'Rain and Snow', 'Hail'):
            win['-IMAGE-'].update('Image/rain.png',visible=True)
        elif weather in ('Scattered Thunderstorms', 'Chance of Storm', 'Storm', 'Thunderstorm', 'Chance of TStorm'):
            win['-IMAGE-'].update('Image/thunder.png',visible=True)
        elif weather in ('Mist','Dust','Fog','Smoke','Haze','Flurries'):
            win['-IMAGE-'].update('Image/foggy.png',visible=True)
        elif weather in ('Freezing Drizzle', 'Chance of Snow', 'Sleet', 'Snow', 'Icy','Snow Showers'):
            win['-IMAGE-'].update('Image/snow.png',visible=True)
        else:
            win['-IMAGE-'].update('Image/idle.png',visible=True)

win.close()
