from fastapi import HTTPException
from services.database_service import read_query, insert_query, update_query
from models.match_request import MatchRequest, Status
from models import job_ad
from models import company_ad
from models import professional
from models.account import Type
from services.companies import job_ads_service
from services.professionals import company_ads_service


def get_match_request(company_ad_id: int, job_ad_id: int, sender_type: Type):

    match_request = read_query('SELECT company_ad_id, job_ad_id, sender_type, status FROM match_requests WHERE company_ad_id = ? AND job_ad_id = ? AND sender_type = ?', 
                               (company_ad_id, job_ad_id, sender_type))[0]
    sender_name = get_sender_name(company_ad_id, job_ad_id, sender_type)
    if match_request[2] == 'professional':
        return MatchRequest.from_database(sender_name, match_request[0], match_request[3], match_request[2])
    if match_request[2] == 'company':
        return MatchRequest.from_database(sender_name, match_request[1], match_request[3], match_request[2])
    

def get_all_matches_for_ad_id(id: int):

    sent_match_request_list = []
    received_match_request_list =[]
    ad_type = ''
    account_type = ''


    if job_ads_service.is_job_ad(id):
        ad_type = 'job_ad_id' 
        account_type = 'company'
    elif company_ads_service.is_company_ad(id):
        ad_type = 'company_ad_id'
        account_type = 'professional'
    else:
        return [[],[]]


    for match_info_tuple in read_query(f'SELECT company_ad_id, job_ad_id, sender_type, status FROM match_requests WHERE {ad_type} = ?', (id,)):
        if match_info_tuple[2] == account_type:
            sent_match_request_list.append(get_match_request(match_info_tuple[0], match_info_tuple[1], match_info_tuple[2]))
        else:
            received_match_request_list.append(get_match_request(match_info_tuple[0], match_info_tuple[1], match_info_tuple[2]))

    match_request_list = [sent_match_request_list, received_match_request_list]

    return match_request_list


def get_all_matches_for_id(id: int):
    table = ''
    id_type = ''
    ad_type = ''
    account_type = ''
    if id in [id_tupel[0] for id_tupel in read_query('SELECT professional_id FROM company_ads')]:
        table = 'company_ads'
        id_type = 'professional_id'
        ad_type = 'company_ad_id'
        account_type = 'professional'
    elif id in [id_tupel[0] for id_tupel in read_query('SELECT company_id FROM job_ads')]:
        table = 'job_ads'
        id_type = 'company_id'
        ad_type = 'job_ad_id'
        account_type = 'company'
    else:
        return [[],[]]

    sent_match_request_list = []
    received_match_request_list =[]

    for ad_id_tuple in read_query(f'SELECT id FROM {table} WHERE {id_type} = ?', (id,)):
        for match_request in read_query(f'SELECT company_ad_id, job_ad_id, sender_type FROM match_requests WHERE {ad_type} = ?', (ad_id_tuple[0],)):
            if match_request[2] == account_type:
                sent_match_request_list.append(get_match_request(match_request[0], match_request[1], match_request[2]))
            else:
                received_match_request_list.append(get_match_request(match_request[0], match_request[1], match_request[2]))

    match_request_list = [sent_match_request_list, received_match_request_list]
    #This is disgusting but it works

    return match_request_list


def create_match_request(company_ad_id: int, job_ad_id: int, sender_type: Type):
    if len(read_query('SELECT * FROM match_requests WHERE company_ad_id = ? AND job_ad_id = ?', (company_ad_id, job_ad_id))) > 0: return get_match_request(company_ad_id, job_ad_id, sender_type)

    insert_query('INSERT INTO match_requests(company_ad_id, job_ad_id, sender_type, status) VALUES(?,?,?,?)', (company_ad_id, job_ad_id, sender_type, Status.PENDING))
    
    return get_match_request(company_ad_id, job_ad_id, sender_type)


def get_sender_name(company_ad_id: int, job_ad_id: int, sender_type: Type):
    if sender_type == 'professional':
        return [f'{name_tuple[0]} {name_tuple[1]}' for professional_id_tuple in read_query('SELECT professional_id FROM company_ads WHERE id = ?', (company_ad_id,)) 
                for name_tuple in read_query('SELECT first_name, last_name FROM professionals WHERE id = ?', (professional_id_tuple[0],))][0]
    if sender_type == 'company':
        return [f'{name_tuple[0]}' for company_id_tuple in read_query('SELECT company_id FROM job_ads WHERE id = ?', (job_ad_id,)) 
                for name_tuple in read_query('SELECT name FROM companies WHERE id = ?', (company_id_tuple[0],))][0]

                
def match_response(company_ad_id: int, job_ad_id: int, response):

    if not match_request_exists(company_ad_id, job_ad_id):
        raise HTTPException(status_code=400, detail=f'No match request between Company Ad {company_ad_id} and Job Ad {job_ad_id}')

    if response == 'accept':
        update_query('UPDATE match_requests SET status = ? WHERE company_ad_id = ? AND job_ad_id = ?', (Status.ACCEPTED, company_ad_id, job_ad_id))
        update_query('UPDATE company_ads SET status = ? WHERE id = ?', (company_ad.Status.MATCHED, company_ad_id))
        update_query('UPDATE job_ads SET status = ? WHERE id = ?', (job_ad.Status.ARCHIVED, job_ad_id))
        update_query('UPDATE professionals SET status = ? WHERE id = ?', (professional.Status.BUSY, company_ads_service.get_company_ad_owner(company_ad_id)))
    if response == 'reject':
        update_query('UPDATE match_requests SET status = ? WHERE company_ad_id = ? AND job_ad_id = ?', (Status.REJECTED, company_ad_id, job_ad_id))


def match_request_exists(company_ad_id, job_ad_id):
    if [match_request for match_request in read_query('SELECT status FROM match_requests WHERE company_ad_id = ? AND job_ad_id = ?', (company_ad_id, job_ad_id))]:
        return True
    return False