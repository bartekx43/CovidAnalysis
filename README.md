# Covid Analysis
The analysis of a correlation between the percentage of people vaccinated and the number of cases and deaths reported in a given country. For clarity, the number of cases is associated with the number of deaths reported 14 days later (as this was the approximate period between case and death reports if both occured).
The data used for the project comes from the listed sources:
- https://github.com/CSSEGISandData/COVID-19
- https://github.com/owid/covid-19-data
# Use
In order to use the program, run following commands:
```
pip install matplotlib
python3 main.py
```
The set of countries included in the analysis is determined by variable ```names```. Similarly, the period of analysis by variables ```start_str``` and  ```end_str```. 
To collect the newest data from the mentioned sources  ```update()``` function can be called.
# Examples
Sample resuls:
![example2](https://user-images.githubusercontent.com/61387975/161231825-c3b1ae30-7072-45a2-864d-28a5898aaf77.jpg)
