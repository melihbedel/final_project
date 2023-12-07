from data.database import read_query
from data.professional_model import CompanyAds


def view_all_company_ads():
    data = read_query('''SELECT * from company_ads WHERE status = "active"''')

    return (CompanyAds.from_query_result(*row) for row in data)


def view_by_location(location):
    data = read_query('''SELECT * from company_ads WHERE location = ? AND status = "active"''',
                      (location,))

    return (CompanyAds.from_query_result(*row) for row in data)


