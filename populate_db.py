import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3


class PopulateDB():
    # connection to the sqlite database
    def __init__(self):
        self.con = sqlite3.connect('db.sqlite3')
        self.cur = self.con.cursor()

    # parse year ordered data and return pandas dataframe
    def parse_data(self):
        page = requests.get("https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-and-regional-series")
        soup = BeautifulSoup(page.content, 'html.parser')
        txt_file_links = soup.find_all(attrs={"rel": "noopener", "title": re.compile("Date")}) # tags whose rel = "noopener" and title contains "Date"
        # params_list = []
        # regions_list = []
        # units_list = []
        links = []
        units = {
            "Tmin": "Celsius", 
            "Tmean": "Celsius", 
            "Tmax":"Celsius",
            "Sunshine": "Days", 
            "Rainfall": "mm", 
            "Raindays1mm": "Days", 
            "AirFrost": "Days"
            }
        for link in txt_file_links:
            links.append(link)
            l = link['href']
            temp = l.split("/")
            file_name = temp[-1].replace('.txt', '')
            statistics_type = temp[-3]
            unit = units[statistics_type]
            # params_list.append(statistics_type)
            # units_list.append(unit)
            # regions_list.append(file_name)
            self.insert_instrument(statistics_type, file_name, unit)
            response = requests.get("https://www.metoffice.gov.uk"+l)
            content = response.content.decode()
            raw_data = content.split('\n')[5:]
            a = [re.split("\s+", x) for x in raw_data]
            data = pd.DataFrame(a[1:], columns=a[0])
            data['region'] = file_name
            data['params'] = statistics_type
            data['unit'] = unit
            self.insert_data(data)
            self.insert_seasonal_data(data)
        
    # insert data in instrument table
    def insert_instrument(self, param, region, unit):
        self.cur.execute("Insert into api_instrument (parameters, region, unit) values (?, ?, ?)", (param, region, unit))
        self.con.commit()

    # insert data in data table
    def insert_data(self, data):
        new_data = data.iloc[:, 0:13]
        table_data = []
        for key, value in new_data.iterrows():
            year = value[0]
            count = 0
            if year:
                for e in value:
                    if count > 0:
                        table_data.append([year, count, e])
                    count+=1
        id = self.cur.execute("Select id from api_instrument where parameters = ? and region = ? and unit = ?",
        (data['params'][0], data['region'][0], data['unit'][0])).fetchone()
        if id :
            id = id[0]
            for row in table_data:
                try:
                    row[2] = float(row[2])
                except:
                    row[2] = None
                self.cur.execute("Insert into api_data (year, month, data, instrument_id) values(?, ?, ?, ?)",
                (row[0], row[1], row[2], id))
            self.con.commit()
    
    # insert data in seasonal data table
    def insert_seasonal_data(self, data):
        new_data = data.iloc[:, [0,13,14,15,16,17]]
        table_data = []
        seasons = {
            1: "win",
            2: "spr",
            3: "sum",
            4: "aut",
            5: "ann",
        }
        for key, value in new_data.iterrows():
            year = value[0]
            count = 0
            if year:
                for e in value:
                    if count > 0:
                        table_data.append([year, seasons[count], e])
                    count+=1
        id_instrument = self.cur.execute("Select id from api_instrument where parameters = ? and region = ? and unit = ?",
        (data['params'][0], data['region'][0], data['unit'][0])).fetchone()
        if id_instrument :
            id_instrument = id_instrument[0]
            for row in table_data:
                id_seasons = self.cur.execute("Select id from api_seasons where name = ?",(row[1],)).fetchone()
                id_seasons = id_seasons[0]
                try:
                    row[2] = float(row[2])
                except:
                    row[2] = None
                self.cur.execute("Insert into api_seasonaldata (year, season_id, data, instrument_id) values(?, ?, ?, ?)",
                (row[0], id_seasons, row[2], id_instrument))
            self.con.commit()

    # insert data in seasons table
    def insert_seasons(self):
        seasons = [
            ["win", "Winter"],
            ["spr", "Spring"],
            ["sum", "Summer"],
            ["aut", "Autumn"],
            ["ann", "Annual"]
        ]

        for season in seasons:
            self.cur.execute("Insert into api_seasons (name, verbose) values(?, ?)",
            (season[0], season[1]))
        self.con.commit()



db = PopulateDB()
db.insert_seasons()
db.parse_data()

