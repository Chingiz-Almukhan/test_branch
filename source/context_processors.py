import datetime


def get_current_date(request):
    return {'current_date': datetime.datetime.today()}
