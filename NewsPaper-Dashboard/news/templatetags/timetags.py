from django import template
import datetime, time, dateutil.parser
register = template.Library()

def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    # return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(ts / 1000.))
    return time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime(ts/1000.))


register.filter(print_timestamp)

def googlePubDate(pubDate):
    parsedDate = time.strftime('%d/%m/%Y %I:%M:%S %p', pubDate)
    return parsedDate


register.filter(googlePubDate)


def iso8601(isoDate):
    parsedDate = dateutil.parser.parse(isoDate)
    return parsedDate.strftime('%d/%m/%Y %I:%M:%S %p')

register.filter(iso8601)