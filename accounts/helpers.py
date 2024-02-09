from datetime import timedelta, datetime


def formatDate(sdate=None):
    if sdate == None:
        return sdate

    return datetime.strptime(sdate, "%d-%m-%Y").date()

