import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_GPT = os.getenv('API_KEY_GPT')
AUTHORIZATION = os.getenv('AUTHORIZATION')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
STATUS_OPEN = [1, 2, 5, 6]

'''
    parâmetro controller:
    adress = endereço
    neighborhood = bairro
    city = municipio
    site_name = nome do site
    recused_reason = motivo da recusa
    opening_reason = motivo de abertura
    triage = triagem
    rov=rov
    id_activity = id da atividade pai na btime
    children_id = id da atividade filha na btime
    checklist = questionario
    system = sistema
    validate_status_father = status da atividade pai na btime
    validate_status_children = status da atividade filha na btime
'''