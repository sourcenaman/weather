<!-- ABOUT THE PROJECT -->

## About The Project

A weather api which returns rank ordered or year ordered seasonal and monthly data of a region.

### Built With

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [django-rest-framework](https://www.django-rest-framework.org/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- [Python](https://www.python.org/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sourcenaman/weather.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Run Server
   ```sh
   python manage.py runserver
   ```

### API DOCUMENTATION

Parameters
```sh
parameters = ["Tmin", "Tmax", "Sunshine", "Tmean", "Rainfall", "Raindays1mm", "Airfrost"]
region = ["UK", "England", "Wales", "Scotland", "Northern_Ireland", "England_and_Wales", "England_N", "England_S", "Scotland_N", "Scotland_E", "Scotland_W", "England_E_and_NE", "England_NW_and_N_Wales", "Midlands", "East_Anglia", "England_SW_and_S_Wales", "England_SE_and_Central_S"]
season = ["Winter", "Spring", "Summer", "Autumn", "Annual"]
```
1. Endpoint /duration/
```sh
yourdomain.com/duration/
```
Request Body
```sh
{
    "year": [2021, 2020], # List of all the years that needs to be queried. If the list is empty then all the years will be queried (type(int))
    "month": [], # List of all the months that needs to be queried. If the list is empty then all the months will be queried (type(int))
    "parameters": [], # List of all the parameters that needs to be queried. If the list is empty then all the parameters will be queried (type(string)) (case sensitive)
    "region": [], # List of all the regions that needs to be queried. If the list is empty then all the regions will be queried (type(string)) (case sensitive)
    "type": "ranked" #Choice field ["ranked", "date"]
}
```
Response Body
```sh
{
    "year": 2020,
    "month": "January",
    "data": 259.7,
    "instrument": {
        "parameters": "Rainfall",
        "region": "Scotland_N",
        "unit": "mm"
    }
}
```

2. Endpoint /season/
```sh
yourdomain.com/season/
```
Request Body
```sh
{
    "year": [2021, 2020], # List of all the years that needs to be queried. If the list is empty then all the years will be queried (type(int))
    "season": ["Winter"], # List of all the seasons that needs to be queried. If the list is empty then all the seasons will be queried (type(string)) (case sensitive)
    "parameters": [], # List of all the parameters that needs to be queried. If the list is empty then all the parameters will be queried (type(string)) (case sensitive)
    "region": [], # List of all the regions that needs to be queried. If the list is empty then all the regions will be queried (type(string)) (case sensitive)
    "type": "ranked" #Choice field ["ranked", "date"]
}
```
Response Body
```sh
{
    "year": 2020,
    "season": "Winter",
    "data": 377.0,
    "instrument": {
        "parameters": "Rainfall",
        "region": "England_N",
        "unit": "mm"
    }
}
```


<!-- ROADMAP -->

## Roadmap

Make another endpoint for year range and month range.

## Issues

See the [open issues](https://github.com/sourcenaman/weather/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- CONTACT -->

## Contact

Naman Vashishth - namanvashishth12@gmail.com

Project Link: [https://github.com/sourcenaman/weather](https://github.com/sourcenaman/weather)