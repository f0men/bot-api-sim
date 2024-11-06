import logging
import json


def data_add_to_database(data, db):
    for dict_user in data: # проходака по данным и занесение в базу
        logging.info(f'Начало Загрузки данных в базу по пользователю {dict_user.get("lti_user_id")}')
        user_id = dict_user.get('lti_user_id')
        if dict_user.get('passback_params'):
            passback_params = json.loads(dict_user.get('passback_params').replace("'", '"'))
            lis_result_sourcedid = passback_params['lis_result_sourcedid']
            lis_outcome_service_url = passback_params.get('lis_outcome_service_url')
            is_correct = bool(dict_user.get('is_correct'))
            attempt_type = dict_user.get('attempt_type')
            created_at = dict_user.get('created_at')
            s=f"""INSERT INTO database_api_simulative.user_activity(user_id, lis_result_sourcedid, lis_outcome_service_url,is_correct, attempt_type, created_at) VALUES('{user_id}', '{lis_result_sourcedid}', '{lis_outcome_service_url}',{is_correct}, '{attempt_type}', '{created_at}')"""
            db.insert(s)
            logging.info(f'Конец загрузки данных в базу инофрмации по пользователю {user_id}')