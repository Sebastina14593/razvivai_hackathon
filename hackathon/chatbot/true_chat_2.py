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
                                                           ''' + (
        welcome_word if len(conversation_history) == 0 else "")}
                            ] + conversation_history
    print(len(conversation_history))
    # Если это первый ответ пользователя (т.е. длина списка истории равна 2, то в этом случае):
    if len(conversation_history) == 1:
        user_input = '''Ответ от руководителя на результат твоего анализа команды на предмет того,
                        кто был уволен на этой неделе '1. Кузьмин Матвей Владимирович имеет перспективы повышения.
                        Я могу предложить кандидатов из вашей команды для подготовки преемника и построить
                        траекторию его подготовки к новой должности.': 
                     '''
        # Сотрудник на повышение:
        promotion_emp = 'Кузьмин Матвей Владимирович'
        # Потенциальные преемники:
        skills_list = get_data_by_fio(promotion_emp)["skills"].split(", ")
        perfect_candidates = perfect_candidates_search(promotion_emp, skills_list)
        # Вопрос пользователю:
        chat_comment1 = f"""На текущей должности {promotion_emp} использует следующие навыки: {get_data_by_fio(promotion_emp)["skills"]}.
                            В вашей команде есть {len(perfect_candidates)} сотрудника, которые потенциально могут выполнять эти обязанности в рамках освобожденной должности:
                         """

        chat_comment2 = ""
        for perfect_candidate in perfect_candidates:
            perfect_candidate_ = get_chat_adhoc(auth_token, f'''
                                   Оцени по 100 бальной шкале [кол-во баллов] соответствие {perfect_candidate['skills']} и {skills_list}.
                                   Старайся оценивать числом, меньшим чем 100.
                                   И составить список навыков, которые надо улучшить сотруднику [навыки улучшить].

                                   Сформулируй ответ, в котором нужно указать оценку кандидата, его имеющиеся и навыки, которые нужно улучшить [навыки улучшить]. Передай [авыки улучшить] в виде списка через запятую без квадратных скобок.
                                   Ответ представь по <шаблону>: 1) [кол-во баллов]; 2) {perfect_candidate['fio']} обладает навыками: {perfect_candidate['skills']}. Необходимо улучшить навыки: [навыки улучшить].
                                   ''').json()['choices'][0]['message']['content']

            perfect_candidate_ = f"{perfect_candidate['fio']} (<a href='/resumes/{perfect_candidate['id']}' target='_blank'>профиль</a>):" + perfect_candidate_ + "<br>"

            chat_comment2 += perfect_candidate_ + "<br><br>"

        chat_comment3 = '<br>Я могу построить траектории по освоению оставшихся навыков. Рассказать ли подробнее о каком-то из кандидатов?'
        chat_comment = chat_comment1 + "<br><br><br>" + chat_comment2 + chat_comment3
        user_input = user_input + (f'. Во всех ответах сохраняй теги "<br>" и сохраняй теги "<a>". Напиши следующее: "{chat_comment}"')

    elif len(conversation_history) == 4:
        emp = conversation_history[3]["content"]
        print(emp)
        emp_info = conversation_history[2]["content"]
        print(emp_info)

        user_input = f'''Найди в фразе '{emp}' имя сотрудника. Запомни его <имя>.
                        Найди в предложении '{emp_info}' информацию по имени <имя> сотрудника. Найди список навыков [навыки],
                        которые нужно улучшить. Не задавая лишних вопросов,
                        дай рекоммендации [рекоммендации] по сотруднику <имя> и [навыкам], которые ему нужно улучшить.
                        Вот пример по абстрактному сотруднику Сергею: "Как руководитель проекта в банке, Сергей проявляет высокую компетенцию в организации рабочих процессов, анализе финансовых данных и управлении командой. Его опыт в области проектного управления позволяет ему успешно достигать целей и решать сложные задачи в срок. Предлагаю следующую траекторию для подготовки Сергея к замене Матвея:

                        1. Адаптация к новым обязанностям: Проведение индивидуальных сессий с Матвеем для погружения в специфику его работы и методики, которые он применяет.
                        2. Развитие недостающих навыков: Организация тренингов и курсов, направленных на усовершенствование навыков, в которых Сергей ещё не достаточно компетентен, чтобы полностью занять позицию Светланы. Это может включать в себя обучение методам анализа рисков, коммуникационным навыкам или стратегическому планированию.
                        3. Практическое применение полученных знаний: Предложение проектов или задач, которые позволят Сергею применить новые навыки на практике под руководством Матвея. Например, возможностей для участия в совместных проектах, где он сможет наблюдать и учиться от неё.
                        4. Обратная связь и мониторинг: Регулярные сессии обратной связи и оценки прогресса, чтобы убедиться, что Сергей эффективно осваивает новые навыки и готов к переходу на новую должность.
                        
                        Напиши подробные [рекоммендации] по сотруднику <имя> как в примере, предстлавенном ранее.
                        "
                     
                     '''
        user_input = user_input + " и в конце спроси у пользователя: 'Вы хотите оставить <имя> или предложить анализ по другим кандидатам?'"
    else:
        user_input = user_message

    if len(conversation_history) != 1000:
        conversation_history.append({
            "role": "user",  # Роль отправителя
            "content": user_input  # Содержание сообщения
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
    candidates_fio = [x["fio"] for x in UserResume2.objects.values('fio') if get_data_by_fio(x["fio"])["prof_area"] != get_data_by_fio(emp)["prof_area"]]
    print(candidates_fio)
    candidates_skills = [get_data_by_fio(x)["skills"] for x in candidates_fio]
    print(candidates_skills)

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