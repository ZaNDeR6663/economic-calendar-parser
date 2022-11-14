import urllib
import urllib.request
from urllib.error import HTTPError
import re

from bs4 import BeautifulSoup
import datetime
import arrow


class Investing:
    def __init__(self, uri='http://ru.investing.com/economic-calendar/'):
        self.uri = uri
        self.req = urllib.request.Request(uri)
        self.req.add_header('User-Agent',
                            'Mozilla/5.0 (Macintosh;'
                            ' Intel Mac OS X 10_10_5)'
                            ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
        self.result = []

    def news(self):
        self.result = []
        try:
            response = urllib.request.urlopen(self.req)

            html = response.read()

            soup = BeautifulSoup(html, "html.parser")

            # Find event item fields
            table = soup.find('table', {"id": "ecEventsTable"})
            tbody = table.find('tbody')

            rows = tbody.findAll('tr', {"id": re.compile("eventRowId_")})

            news = {'timestamp': None,
                    'country': None,
                    'impact': None,
                    'name': None,
                    'bold': None,
                    'fore': None,
                    'prev': None
                    }

            for tr in rows:
                # print(tr)
                # print()
                # print (row.attrs['data-event-datetime'])
                _datetime = tr.attrs['event_timestamp']
                # news['timestamp'] = arrow.get(_datetime, "YYYY/MM/DD HH:mm:ss").timestamp
                news['timestamp'] = _datetime

                # извлекаем страну/зону
                cols = tr.find('td', {"class": "flagCur"})
                flag = cols.find('span')
                news['country'] = flag.get('title')

                # извлекаем влияние на волатильность
                impact = tr.find('td', {"class": "sentiment"})
                bull = impact.findAll('i', {"class": "grayFullBullishIcon"})

                news['impact'] = len(bull)  # работает?

                event = tr.find('td', {"class": "left event"})
                news['name'] = event.text.strip()

                bold = tr.find('td', {"class": "bold"})

                if bold.text != '':
                    news['bold'] = bold.text.strip()
                else:
                    news['bold'] = ''

                fore = tr.find('td', {"class": "fore"})
                news['fore'] = fore.text.strip()

                prev = tr.find('td', {"class": "prev"})
                news['prev'] = prev.text.strip()

                self.result.append(news)

                news = {'timestamp': None,
                        'country': None,
                        'impact': None,
                        'name': None,
                        'bold': None,
                        'fore': None,
                        'prev': None
                        }

        except HTTPError as error:
            print("Oops... Get error HTTP {}".format(error.code))

        return self.result

    def today_news(self):
        today = datetime.datetime.now().date()
        res = []
        for today_res in self.result:
            datestamp = datetime.datetime.fromisoformat(today_res['timestamp']).date()
            if datestamp == today:
                # print(today_res)
                # print(datetime.datetime.fromisoformat(today_res['timestamp']).time())
                res.append(today_res)
        return res


if __name__ == "__main__":
    # i = Investing()
    timezone_and_countries = ""
    calType = ""
    timeZone = ""
    lang = ""
    exc_actual = True
    exc_forecast = True
    exc_flags = True

    i = Investing('https://sslecal2.investing.com/?columns=exc_flags,'
                  'exc_currency,exc_importance,exc_actual,exc_forecast,'
                  'exc_previous&features=datepicker,timezone&countries=72,37,5&calType=day&timeZone=18&lang=7')

    i.news()
    for news in i.today_news():
        print(news)
