import json
import requests

from .giga_chat_adhoc import get_chat_adhoc
from resumes.models import UserResume, UserResume2

from .chatbot_functions.resumes_db import get_data_by_fio
from .chatbot_functions.text_correction import *

def get_chat_completion(auth_token, user_message, conversation_history):

    # Не надо начинать диалог с привествия, поскольку на странице уже будут предложены готовые варианты
    welcome_word = " Обойдись без приветствий."
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Задаем роль ИИ-помощнику
    conversation_history = [{"role": "system", "content": '''Ты бот, помогающий руководителю проектов внутри банка. Ты занимаешься анализом ситуации в команде. И предлагаешь три функции:
                                                               1. Отслеживаешь перспективы повышения сотрудников и предлогаешь кандидатов из команды для подготовки преемников в случае потенциального ухода сотрудника из команды.
                                                                  Ты также строишь траекторию подготовкидля потенциального сотрудника-преемника.
                                                               2. Анализируешь, сколько ПШЕ (производственная штатная единица) было выделено на команду и рекоммендуешь на их место внутренних кандидатов из всего банка.
                                                               3. Отслеживаешь, кто уволился из команды и создаешь заявку на вакансию и рекомендуешь внутренних кандидатов всего банка на освободившуюся позицию.
                                                           ''' + (welcome_word if len(conversation_history) == 0 else "")}
                            ] + conversation_history
    print(len(conversation_history))
    # Если это первый ответ пользователя (т.е. длина списка истории равна 2, то в этом случае):
    if len(conversation_history) == 1:
        user_input = '''Ответ от руководителя на результат твоего анализа команды на предмет того,
                        кто был уволен на этой неделе '3. На этой неделе у вас уволился аналитик данных.
                        Я могу создать заявку на вакансию и порекомендовать внутренних кандидатов.': 
                     '''
        # Уволенный сотрудник:
        fired_emp = 'Казакова Александра Романовна'
        # Вопрос пользователю:
        chat_comment = f"""Ушедший аналитик данных: {fired_emp}.
                           Вам составить описание вакансии на основе его опыта и навыков или Вы хотите завести новую вакансию?
                        """
        user_input = user_input + (f". Спроси следующий вопрос: '{chat_comment}'")

    elif len(conversation_history) == 3:
        # Уволенный сотрудник
        fired_emp = 'Казакова Александра Романовна'
        # Информация по уволенному сотруднику:
        fired_emp_info = get_data_by_fio(fired_emp)
        fired_emp_skills = fired_emp_info["skills"]
        fired_emp_responsibilities = number_correction(fired_emp_info["responsibilities"])

        chat_comment = f'''Навыки: {fired_emp_skills};
                           <br><br>Обязанности на текущем месте работы: {fired_emp_responsibilities};
                           <br><br>Создать новую вакансию на должность аналитика данных?
                        '''
        user_input = f'''Во всех ответах сохраняй тег "<br>". Напиши следующее: "{chat_comment}"'''

    elif len(conversation_history) == 5:
        # Уволенный сотрудник
        fired_emp = 'Казакова Александра Романовна'
        # Вакансия по навыкам и обязанностям уволенного сотрудника
        vacancy = f'''Позиция: аналитик данных
                      Навыки: {get_data_by_fio(fired_emp)["skills"]}
                      Обязанности: {get_data_by_fio(fired_emp)["responsibilities"]}
                   '''
        perfect_candidates = perfect_candidates_search(fired_emp, get_data_by_fio(fired_emp)["skills"].split(", "))
        # Далее проходимся по отобранным кандидатам
        # И с помощью вложенного гигачата опредяем оценки данных кандидатов

        chat_comment2 = ""
        for perfect_candidate in perfect_candidates:

            perfect_candidate_ = get_chat_adhoc(auth_token,f'''
                                <вакансия>
                                {vacancy}
                                </вакансия>
                                <резюме>
                                Должность на текущем месте работы: {perfect_candidate['position']}.
                                Обязанности на текущем месте работы: {perfect_candidate['responsibilities']}
                                Навыки кандидата: {perfect_candidate['skills']}
                                Достижения кандидата: {perfect_candidate['achievements']}
                                Профтеги кадидата: {perfect_candidate['prof_tags']}
                                </резюме>
                                Тебе нужно оценить <резюме> кандидата по 100 балльной шкале. Оценивать кандидатов нужно строго по критериям оценки. У каждого критерия есть максимальный балл.
                                Общий максимальный балл, который может получить кандидат: 100 баллов.
                                <Критерии для оценки>:
                                    1) Соответствие должности кандидата (максимальный балл - 15)
                                    2) Соответствие выполняемых обязанностей кандидата на работе (максимальный балл - 35). 
                                    3) Соответствие навыков кандидата (максимальный балл - 25).
                                    4) Наличие достижений у кандидата (максимальный балл - 15).
                                    5) Соответствие профтегов кандидата требуемой позиции (максимальный балл - 10)
                                </Критерии для оценки>.
                    
                                Сформулируй ответ, в котором нужно указать оценку кандидата [кол-во баллов], [преимущества кандидата] и [недостатки кандидата].
                                Ответ представь по <шаблону>: 1) Оценка: [кол-во баллов]. 2) Преимущества кандидата: [преимущества кандидата]. 3) Недостатки кандидата: [недостатки кандидата]
                                ''').json()['choices'][0]['message']['content']
            perfect_candidate_ = f"Кандидат: {perfect_candidate['fio']} (<a href='/resumes/{perfect_candidate['id']}' target='_blank'>резюме</a>)<br>" + \
                                 perfect_candidate_.replace("1)", "<br>1)").replace("2)", "<br>2)").replace("3)", "<br>3)")

            chat_comment2 += perfect_candidate_ + "<br><br>"
            print(chat_comment2)

        chat_comment1 = '''Я создал новую вакансию на должность аналитик данных. Также нашел внутренних кандидатов, подходящих под описание:<br>'''
        chat_comment3 = '''Заинтересовал ли Вас кто-то?'''

        chat_comment = chat_comment1 + chat_comment2 + chat_comment3

        user_input = f'''Во всех ответах сохраняй теги "<br>" и сохраняй теги "<a>". Напиши следующее: "{chat_comment}"'''

    elif len(conversation_history) == 7:
        user_input = 'Спроси следующее: "Прекрасно, отправить кандидату предложение рассмотреть вакансию?"'

    elif len(conversation_history) == 9:
        user_input = "Напиши следующее: 'Я направил кандидату коммуникацию и сразу же сообщу о любых новостях. Есть ли у вас еще вопросы?'"
    # Далее работает как обычный чат
    else:
        user_input = user_message

    if len(conversation_history) != 1000:
        conversation_history.append({
            "role": "user", # Роль отправителя
            "content": user_input # Содержание сообщения
        })
    else:
        conversation_history = [{
            "role": "user",  # Роль отправителя
            "content": user_input  # Содержание сообщения
        }]

    print(conversation_history)
    # print(conversation_history, UserResume)

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": conversation_history,
        "temperature": 1,
        # Генерация температуры (насколько случайным будет ответ при генерации ответа. Если 0, то будет выбираться самый надежный результат (всегда один и тот же ответ))
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов (также за разнообразие)
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,
        # Потоквая ли передача ответов (отправляется ли каждый токен в ответ пользователю или сразу весь ответ)
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения (можно ставить побольше, чтобы не повторялись в больших текстах)
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1

def perfect_candidates_search(emp, required_skills_list):
    print(required_skills_list)
    candidates_fio = [x["fio"] for x in UserResume2.objects.values('fio')]
    candidates_skills = [x["skills"] for x in UserResume2.objects.values('skills')]

    candidates_ranks_list = [0] * len(candidates_fio)

    for required_skill in required_skills_list:
        for i in range(len(candidates_fio)):
            if candidates_fio[i] == emp:
                candidates_ranks_list[i] = 0
            else:
                if required_skill.lower() in candidates_skills[i].lower():
                    candidates_ranks_list[i] += 1

    # Далее определяем наиболее подходящих сотрудников по рангу
    your_idel_candidate = []
    max_rank = max(candidates_ranks_list)
    print(candidates_ranks_list)
    if candidates_ranks_list.count(max_rank) < 3:
        left_el = candidates_ranks_list.index(max_rank - 1)
        right_el = len(candidates_ranks_list) - candidates_ranks_list[::-1].index(max_rank - 1) - 1
        candidates_ranks_list[left_el] += 1
        candidates_ranks_list[right_el] += 1

    for i in range(len(candidates_ranks_list)):
        if candidates_ranks_list[i] == max_rank:
            your_idel_candidate.append(get_data_by_fio(candidates_fio[i]))

    return your_idel_candidate