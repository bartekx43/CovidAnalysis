import csv
import matplotlib.pyplot as plt
from datetime import datetime
import locale
import matplotlib.patches as mpatches


def get_country(name, start_str, end_str):
    with open('cases.csv') as file:
        reader = csv.reader(file)
        cases = []
        header = next(reader)[4:]
        for row in reader:
            if row[1] == name:
                cases = row[4:]
    with open('deaths.csv') as file:
        reader = csv.reader(file)
        deaths = []
        for row in reader:
            if row[1] == name:
                deaths = row[4:]
    with open('vaccines.csv') as file:
        reader = csv.reader(file)
        vaccines = []
        for row in reader:
            if row[0] == name and row[11]:
                vaccines.append([datetime.strptime(row[2], "%Y-%m-%d").date(), float(row[11])])

    x_axis = header
    x_axis = [datetime.strptime(el, "%m/%d/%y").date() for el in x_axis]
    start = [i for i, date in enumerate(x_axis) if date == datetime.strptime(start_str, "%d-%m-%Y").date()][0]
    end = [i for i, date in enumerate(x_axis) if date == datetime.strptime(end_str, "%d-%m-%Y").date()][0]
    x_axis = x_axis[start:end]
    new_cases = cases[start:end]
    new_deaths = deaths[start:end]
    new_cases = list(map(int, new_cases))
    new_deaths = list(map(int, new_deaths))
    for i in range(len(new_cases) - 2, -1, -1):
        new_cases[i + 1] -= new_cases[i]
        new_deaths[i + 1] -= new_deaths[i]
    new_deaths = new_deaths[1:]
    new_cases = new_cases[1:]

    return new_cases, new_deaths, vaccines, x_axis[:-23]


def update():
    u_cases = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    u_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    u_vaccines = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'

    def download(t_url, filename):
        import requests
        data_c = requests.get(u_cases)
        with open("cases.csv", "w") as f:
            f.write(data_c.text)
        data_c = requests.get(u_deaths)
        with open("deaths.csv", "w") as f:
            f.write(data_c.text)
        data_c = requests.get(u_vaccines)
        with open("vaccines.csv", "w") as f:
            f.write(data_c.text)

    download(u_cases, "cases")
    download(u_deaths, "deaths")
    download(u_vaccines, "vaccines")


if __name__ == '__main__':
    # update() #uncomment this line to update data before running program

    names = ["Portugal", "Ireland", "Italy", "Hungary", "Poland", "Bulgaria"]
    start_str = "01-07-2020"
    end_str = "01-01-2022"

    locale.setlocale(locale.LC_ALL, "en_GB.utf8")
    fig = plt.figure(figsize=(3, 2))

    for num, name in enumerate(names):
        new_cases, new_deaths, vaccines, x_axis = get_country(name, start_str, end_str)
        day50 = datetime.today().date()
        day60 = datetime.today().date()
        day70 = datetime.today().date()
        for pair in vaccines:
            if pair[1] > 50.0:
                day50 = pair[0]
                break
        for pair in vaccines:
            if pair[1] > 60.0:
                day60 = pair[0]
                break
        for pair in vaccines:
            if pair[1] > 70.0:
                day70 = pair[0]
                break

        cases_avg = [sum(new_cases[i:i + 7]) / 7 if sum(new_cases[i:i + 7]) / 7 > 0 else 0 for i in
                     range(0, len(new_cases) - 22)]
        deaths_avg = [sum(new_deaths[i + 14:i + 14 + 7]) / 7 if sum(new_deaths[i + 14:i + 14 + 7]) / 7 > 0 else 0 for i
                      in range(0, len(new_deaths) - 22)]
        days = [day50, day60, day70]

        ax_left = fig.add_subplot(320 + num + 1)
        ax_right = ax_left.twinx()
        p1 = ax_left.plot(x_axis, cases_avg, color="blue", label="cases")
        p2 = ax_right.plot(x_axis, deaths_avg, color="red", label="deaths")
        p3 = plt.plot([], [], ' ', label="Fully vaccinated:")
        green1 = mpatches.Patch(color='green', alpha=0.15, label='50%')
        green2 = mpatches.Patch(color='green', alpha=0.3, label='60%')
        green3 = mpatches.Patch(color='green', alpha=0.45, label='70%')

        lines = p1 + p2 + p3
        lines.extend([green1, green2, green3])
        labs = [l.get_label() for l in lines]

        ax_left.tick_params(axis='y', colors='blue')
        ax_right.tick_params(axis='y', colors='red')
        ax_left.tick_params(axis='x', rotation=0)
        plt.title(name)
        for day in days:
            if day != datetime.today().date():
                ax_left.axvspan(day, x_axis[-1], facecolor='green', alpha=0.15)

        import matplotlib.dates as mdates

        myFmt = mdates.DateFormatter('%b')
        ax_left.xaxis.set_major_formatter(myFmt)

    fig.suptitle("Covid cases and deaths reported*", size=15)
    fig.legend(lines, labs, framealpha=0.5, loc='upper left')
    fig.text(0.125, 0.03,
             '* 7-day average of cases reported from ' + start_str + ' to ' + end_str + ' with average number of deaths reported 14 days later',
             size=8)
    plt.subplots_adjust(wspace=0.33, hspace=0.4)
    plt.show()
