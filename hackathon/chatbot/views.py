from django.shortcuts import render, redirect
from django.http import JsonResponse

from .words_comparison import filter_list, process_skills
from .giga_chat_adhoc import get_chat_adhoc
from .true_chat import get_chat_completion
# from .true_chat_2 import get_chat_completion

from .synthetic_chat import synthetic_chat_generation, synthetic_chat_generation2
# from django.contrib import auth
# from django.contrib.auth.models import User

# Для поиска наиболее похожих между собой слов
from difflib import SequenceMatcher

# Для сохранения чатов в БД
from .models import Chat
from resumes.models import UserResume, UserResume2
from django.utils import timezone

# Для работы с гигачатом
import requests
import json
import uuid

client_id = 'bcf40466-3e35-4583-a25b-a73219d9f796'
secret = '35709e53-1531-40f5-8fe2-bfb739a190e8'
# Даня:
# auth_giga = 'YmNmNDA0NjYtM2UzNS00NTgzLWEyNWItYTczMjE5ZDlmNzk2OjM1NzA5ZTUzLTE1MzEtNDBmNS04ZmUyLWJmYjczOWExOTBlOA=='
auth_giga = 'ZTRiNzRjNzgtYzIwNC00YzdlLWFmZTUtMDY2M2I5MWYxNTlmOmY3YmU5MDhiLTczNGYtNDkxYS1hN2M0LTU5MmQ4NGJhN2Y2ZA=='
# Здесь хранитсся список всех возможных навыков:
filter_words = ['SQL', 'PostgreSQL', 'Oracle', 'MS SQL', "Администрирование базы данных",
                "Архитектура базы данных", "Управление базами данных", 'Excel', 'MS PowerPoint', 'Python',
                'Pandas', 'Numpy',
                "Оптимизация SQL запросов", "Проектирование реляционных баз данных", "Аналитические навыки",
                "Решение проблем", "Критическое мышление", "Мат. статистика", "Hadoop", "Spark", 'Greenplum',
                'ETL', 'Ответственность', 'Коммуникабельность', 'Управление проектами', 'Grafana',
                'Qlik Sense']

def get_token(auth_token, scope = 'GIGACHAT_API_PERS'):
    """
    Выполняет POST-запрос к эндпоинту, который выдает токен.

    Параметры:
    - auth_token (str): токен авторизации, необходимый для запроса.
    - область (str): область действия запроса API. По умолчанию - "GIGACHAT_API_PERS" (физическое лицо, иначе юридическое).

    Возвращает:
    - ответ API, где токен и срок его "годности".
    """

    # создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
      'RqUID': rq_uid,
      'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {"scope": scope}

    try:
        # делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отлюкчать проверку не надо)
        response = requests.post(url, headers = headers, data = payload, verify = False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

response_token = get_token(auth_giga)
if response_token != -1:
    try:
        giga_token = response_token.json()["access_token"]
    except:
        giga_token = ""

# def get_chat_completion(auth_token, user_message, conversation_history):
#     """
#     Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.
#
#     Параметры:
#     - auth_token (str): Токен для авторизации в API
#     - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.
#     - conversation_history: История диалога пользователя и GigaChat
#
#     Возвращает:
#     - str: Ответ от API в виде текстовой строки.
#
#     """
#     welcome_word = " Обойдись без приветствий."
#     # URL API, к которому мы обращаемся
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#
#
#     # Задаем роль ИИ-помощнику ()
#     if len(conversation_history) <= 11:
#         conversation_history = [{"role": "system", "content": """Ты бот занимающийся подбором кандидатов. К тебе приходит руководитель и у него есть потребность в сотруднике.
#                                                                  В процессе диалога ты должен получить с него основную информацию о желаемом кандидате. Твоя задача лишь внимательно слушать пользовательские инструкции, и делать то, что тебя попросят.
#                                                               """ + (welcome_word if len(conversation_history) == 0 else "")}] + conversation_history
#
#     # Если это первый ответ пользователя (т.е. длина списка истории равна 2, то в этом случае):
#     if len(conversation_history) == 1:
#         user_input = ("Ответ пользователя на первый вопрос 'На какую [должность] ты ищешь сотрудника': ") + user_message + (". Спроси следующий вопрос: 'Какими навыками должен обладать твой идеальный кандидат?'")
#
#     # Если это второй ответ пользователя (т.е. он ввел необходимые пользователю навыки)
#     elif len(conversation_history) == 3:
#         user_input = ("Необходимые <навыки>: ") + user_message + (""".
#                       Суммаризируй указанные <навыки> и представь их в виде <ключевых слов>. Для вывода используй следующую <инструкцию>: 1) ключевые слова должны быть записаны через запятую. 2) Ответ должен содержать только ключевые слова </инструкция>.""")
#
#         # Здесь хранится список с требуемыми навыками от пользователя:
#         input_words = get_chat_completion(auth_token, user_input, conversation_history=[""] * 1000).json()['choices'][0]['message']['content'].split(", ")
#
#         # Здесь же хранятся обработанные навыки (на случай если, пользователь допустил например грамматическую ошибку и т.д.):
#         processed_skills = process_skills(input_words, filter_words)
#
#         # Дополним контекст переписки также списком навыков, отправленных пользователем
#         conversation_history.append({
#             "role": "user",  # Роль отправителя
#             "content": ', '.join(processed_skills)
#         })
#
#         # Здесь же хранится список рекомендуемых навыков
#         # Если навыки, которые ввел пользователь (предобработанные) содержатся
#         # в списке с глоабльными наывками, то в этом случае навык потворно предлагаться не будет.
#         recommended_list = filter_list(processed_skills, filter_words)
#
#         # if len(filtered_list) > 0:
#         user_input = (f"Скажи пользователю, что его идеальный набор навыков выглядит следующим образом <идеальные навыки>: {", ".join(processed_skills)}") + \
#                      (". Предложи пользователю также <другие навыки>: " + ", ".join(recommended_list) + f". Для вывода используй следующую <шаблон>") + \
#                      (": Твой идеальный кандидат должен обладать следующими навыками: <идеальные навыки>. Также тебе могут быть интересны и другие навыки: <другие навыки>.") + \
#                      ("Нужно ли дополнить исходный список?</инструкция>")
#         # else:
#         #     user_input = "Скажи пользователю следующее: Перечень навыков по данной професси получился исчерпывающим."
#
#     elif len(conversation_history) == 5:
#         print(conversation_history[4])
#         # Положительные ответы:
#         if len(user_message) >= 4:
#             if user_message[:3].lower() == "нет" or user_message[:2].lower() == "не":
#                 user_input = f"Ответ пользователя о необходимости дополнительных навыков: {user_message}. Скажи, что понял его " + \
#                              "и спроси, 'Какой опыт работы должен быть у кандидата?'" + \
#                              " Все это делай по инструкции: <инструкция>Понял тебя. Какой опыт работы должен быть у твоего идеального кандидата?<\инструкция>"
#             elif "нужн" in user_message[:4].lower() or "надо" in user_message[:4].lower() or "нужн" in user_message.lower() or u"добавь" in user_message.lower() or "добавить" in user_message.lower() or "облад" in user_message.lower() or "владе" in user_message.lower() or user_message.lower()[:2] == "да":
#                 add_skills = get_chat_adhoc(auth_token, "Необходимые <навыки>: " + user_message + """.
#                               Суммаризируй указанные <навыки> и представь их в виде <ключевых слов>.
#                               Для вывода используй следующую <инструкцию>: 1) ключевые слова должны быть записаны через запятую.
#                               2) Ответ должен содержать только ключевые слова </инструкция>.""").json()['choices'][0]['message']['content']
#                 if add_skills != -1:
#                     user_preferences = conversation_history[4]["content"].split("обладать следующими навыками ")[1]
#                     user_preferences = user_preferences[:user_preferences.index(". Также")].replace(", ", ",").split(",")
#
#                     add_skills = add_skills.replace(", ", ",").split(",")
#                     user_input = f"Выведи ответ по инструкции <инструкция>" + \
#                                  f" 'Итоговый список требуемых навыков от идеального сотрудника: {", ".join(user_preferences + add_skills)}'.<\инструкция>" + \
#                                  " Затем спроси у пользователя 'Какой опыт работы должен быть у кандидата?'"
#                 else:
#                     user_input = f"Ответ пользователя о необходимости дополнительных навыков: {user_message}. Скажи, что понял его " + \
#                                  "и спроси, 'Какой опыт работы должен быть у кандидата?'" + \
#                                  " Все это делай по инструкции: <инструкция>Понял тебя. Какой опыт работы должен быть у твоего идеального кандидата?<\инструкция>"
#             else:
#                 user_input = f"Ответ пользователя о необходимости дополнительных навыков: {user_message}. Скажи, что понял его " + \
#                               "и спроси, 'Какой опыт работы должен быть у кандидата?'" + \
#                               " Все это делай по инструкции: <инструкция>Понял тебя. Какой опыт работы должен быть у твоего идеального кандидата?<\инструкция>"
#         # Предполагаем далее отрицательные ответы
#         else:
#             user_input = f"Ответ пользователя о необходимости дополнительных навыков: {user_message}. Скажи, что понял его " + \
#                           "и спроси, 'Какой опыт работы должен быть у кандидата?'" + \
#                           " Все это делай по инструкции: <инструкция>Понял тебя. Какой опыт работы должен быть у твоего идеального кандидата?<\инструкция>"
#
#
#     elif len(conversation_history) == 7:
#         # user_input = ("Требуемый опыт работы сотрудника : ") + user_message + (""". Ответь пользователю, используя следующую <инструкцию>: 1) Преобразуй опыт работы в количество лет в числах. 2) Не пиши ничего лишнего. </инструкция>. """) \
#         #             + ("Затем спроси у пользователя, чем предстоит заниматься его будущему кандидату.")
#         user_input = ("Требуемый опыт работы сотрудника : ") + user_message + ("Спроси пользователя, используя следующую <инструкцию>: 'Чем предстоит заниматься твоему будущему сотруднику?' </инструкция>")
#
#     elif len(conversation_history) == 9:
#
#         sberposition, skills, responsibilities, work_experience = resume_compilation(conversation_history, user_message, auth_token)
#
#         user_input = (f"""Без указания ничего лишнего, выведи ответ по следующей <инструкции>:
#                          'Итак, ты ищешь {sberposition} с опытом работы {work_experience}.
#                           Обязанности: {responsibilities}.
#                           Навыки: {skills}. Все ли верно?'
#                         </инструкция>. Не нужно указывать ничего лишнего.
#                       """
#
#                       )
#     elif len(conversation_history) == 11:
#         # user_input = user_message
#         # user_preferences = conversation_history[10]["content"].split("Навыки: ")[1]
#         # user_preferences = user_preferences[:user_preferences.index(". Все")]
#
#         user_preferences, skills, responsibilities, work_experience = resume_compilation(conversation_history, user_message,
#                                                                                      auth_token)
#
#         print(user_preferences)
#         user_perfect_candidate = perfect_candidate(user_preferences)
#         user_perfect_candidates = []
#
#         perfect_user_rank_max = 0
#         for perfect_user in user_perfect_candidate:
#
#             # perfect_user_ = get_chat_adhoc(auth_token, f"Есть <описание вакансии>: {conversation_history[10]["content"]}, которое тебе необходимо суммаризировать. А также имеется описание <резюме пользователя>," + \
#             #                                           f": {perfect_user}, которое также необходимо суммаризировать." + \
#             #                               f"""Сопоставь суммаризированное <описание вакансии> и суммаризированное <резюме пользователя> и выдели основные <плюсы и минусы> в <резюме пользователя>. Дай [оценку] по шкале
#             #                               от 0 до 100, которая объясняет, на сколько <резюме пользователя> соответствует <описанию вакансии>
#             #                               Для вывода используй следующую <инструкцию>: 'Сотрудник [{perfect_user['ФИО']}] получил [оценку] соответствия вакансии и резюме.
#             #                              Вот основные его <плюсы и минусы>.</инструкция>""").json()['choices'][0]['message']['content']
#
#             perfect_user_ = f"""
#             <Вакансия>:
#             Должность: {user_preferences}
#             Навыки: {skills}
#             Обязанности: {responsibilities}
#             Стаж: {work_experience}
#             </Вакансия>
#             <Резюме>
#             ФИО: {perfect_user["ФИО"]}
#             Должность: {perfect_user["Должность"]}
#             Навыки: {perfect_user["Навыки"]}
#             Обязанности: {perfect_user["Обязанности"]}
#             Стаж: {perfect_user["Стаж"]}
#             Достижения: {perfect_user["Достижения"]}
#             Профессиональные теги: {perfect_user["Проф. теги"]}
#             </Резюме>
#             Тебе нужно оценить <резюме> кандидата по 100 балльной шкале. Оценивать кандидатов нужно строго по критериям оценки. У каждого критерия есть максимальный балл. Общий максимальный балл, который может получить кандидат: 100 баллов. <Критерии для оценки>: 1) Соответствие должности кандидата (максимальный балл - 10) 2) Соответствие стажа работы кандидата (максимальный балл - 20). 3) Соответствие выполняемых обязанностей кандидата на работе (максимальный балл - 30).
#             4) Соответствие навыков кандидата (максимальный балл - 20). 5) Наличие достижений у кандидата (максимальный балл - 10). 6) Соответствие профтегов кандидата требуемой позиции (максимальный балл - 10) </Критерии для оценки>.
#             Сформулируй ответ, в котором нужно указать оценку кандидата [кол-во], преимущества кандидата и недостатки кандидата.
#             Ответ представь ТОЧНО по <шаблону>:Отлично, по твоему обращению создана заявка. Скоро с вами свяжется рекрутер. Ниже представлен список рекомендуемых кандидатов: Кандидат: [ФИО]: 1) Оценка GigaChat: [кол-во баллов] баллов. 2) Преимущества кандидата: [преимущества кандидата]. 3) Недостатки кандидата: [недостатки кандидата].
#             Есть ли у тебя предпочтения по кандидатам?
#             """
#             print(perfect_user_)
#             perfect_user_ = get_chat_adhoc(auth_token, perfect_user_)
#             perfect_user_rank_max_ = perfect_user_.json()['choices'][0]['message']['content']
#             print(perfect_user_rank_max_)
#             mark = ""
#             for symbol in perfect_user_rank_max_[perfect_user_rank_max_.index("GigaChat") + 10:perfect_user_rank_max_.index(" баллов")]:
#                 if symbol in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
#                     mark += symbol
#             if mark == "":
#                 perfect_user_rank_max_ = 0
#             else:
#                 perfect_user_rank_max_ = int(mark)
#
#             # perfect_user_rank_max_ = int(perfect_user_rank_max[:perfect_user_rank_max_.index(".")])
#
#             if perfect_user_rank_max_ > perfect_user_rank_max:
#                 perfect_user_rank_max = perfect_user_rank_max_
#                 user_perfect_candidates.append(perfect_user_.json()['choices'][0]['message']['content'])
#
#         print(user_perfect_candidates, type(user_perfect_candidates))
#         user_perfect_candidates = ", ".join(user_perfect_candidates)
#
#         # user_resume = get_chat_completion(auth_token, ("Найди в этом приложение название вакансии [должность]: '") + conversation_history[1] + ("'. Формализуй ответ в виде: [должность]"), conversation_history=[""] * 1000).json()['choices'][0]['message']['content']
#         # print(user_resume)
#         print(user_perfect_candidates)
#         user_input = (f"Выведи следующий текст без лишних слов: {user_perfect_candidates}")# + user_message
#
#         # user_input = ("Если пользователь ответил да в предыдущем ответе, скажи 'ОК',") + \
#         #              ("иначе скажи 'УГУ'")
#         perfect_candidates_search = []
#     # #
#     # # elif len(conversation_history) == 7:
#     # #     user_input = "Требуемый опыт работы сотрудника : " + user_message + """. Ответь пользователю, используя следующую <инструкцию>: 1) Преобразуй опыт работы в количество месяцев. 2) Не пиши ничего лишнего. </инструкция>. """
#     # elif len(conversation_history) == 13:
#     #     if user_message.lower() == "да":
#     #         user_input = user_message
#
#     else:
#         user_input = user_message
#
#     print(user_input, conversation_history)
#     if len(conversation_history) != 1000:
#         conversation_history.append({
#             "role": "user", # Роль отправителя
#             "content": user_input # Содержание сообщения
#         })
#     else:
#         conversation_history = [{
#             "role": "user",  # Роль отправителя
#             "content": user_input  # Содержание сообщения
#         }]
#
#     print(conversation_history)
#     # print(conversation_history, UserResume)
#
#     # Подготовка данных запроса в формате JSON
#     payload = json.dumps({
#         "model": "GigaChat",  # Используемая модель
#         "messages": conversation_history,
#         "temperature": 1,
#         # Генерация температуры (насколько случайным будет ответ при генерации ответа. Если 0, то будет выбираться самый надежный результат (всегда один и тот же ответ))
#         "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов (также за разнообразие)
#         "n": 1,  # Количество возвращаемых ответов
#         "stream": False,
#         # Потоквая ли передача ответов (отправляется ли каждый токен в ответ пользователю или сразу весь ответ)
#         "max_tokens": 512,  # Максимальное количество токенов в ответе
#         "repetition_penalty": 1,  # Штраф за повторения (можно ставить побольше, чтобы не повторялись в больших текстах)
#         "update_interval": 0  # Интервал обновления (для потоковой передачи)
#     })
#
#     # Заголовки запроса
#     headers = {
#         'Content-Type': 'application/json',  # Тип содержимого - JSON
#         'Accept': 'application/json',  # Принимаем ответ в формате JSON
#         'Authorization': f'Bearer {auth_token}'  # Токен авторизации
#     }
#
#     try:
#         response = requests.post(url, headers=headers, data=payload, verify=False)
#         return response
#     except requests.RequestException as e:
#         # Обработка исключения в случае ошибки запроса
#         print(f"Произошла ошибка: {str(e)}")
#         return -1

def ask_giga_chat(message, current_user, giga_token=giga_token):
    chats_history = []
    if len(Chat.objects.filter(user=current_user)) == 0:
        pass
    else:
        users_messages = Chat.objects.filter(user=current_user).values('message')
        chatbots_messages = Chat.objects.filter(user=current_user).values('response')
        for i in range(len(users_messages)):
            user_message = users_messages[i]
            user_message = user_message["message"]

            chatbot_message = chatbots_messages[i]
            chatbot_message = chatbot_message["response"]

            chats_history.append({"role": "user", "content": user_message})
            chats_history.append({"role": "assistant", "content": chatbot_message})

    print(get_chat_completion(giga_token, message, chats_history))
    answer = get_chat_completion(giga_token, message, chats_history).json()['choices'][0]['message']['content']
    return answer
# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get("message")
        response = ask_giga_chat(message, current_user = request.user)
        # response = synthetic_chat_generation(message)
        # response = synthetic_chat_generation2(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, "response": response})
    return render(request, 'chatbot/chatbot.html', {'chats': chats})

def perfect_candidate(required_skills_string):
    print(required_skills_string)
    required_skills_list = required_skills_string.replace(", ", ",").split(",")
    candidates_sex = [x["sex"] for x in UserResume2.objects.values('sex')]
    candidates_fio = [x["fio"] for x in UserResume2.objects.values('fio')]
    candidates_skills = [x["skills"] for x in UserResume2.objects.values('skills')]
    candidates_work_exprience = [x["work_exprience"] for x in UserResume2.objects.values('work_exprience')]
    candidates_responsibilities = [x["responsibilities"] for x in UserResume2.objects.values('responsibilities')]
    candidates_prof_area = [x["prof_area"] for x in UserResume2.objects.values('prof_area')]
    candidates_position = [x["position"] for x in UserResume2.objects.values('position')]
    candidates_achievements = [x["achievements"] for x in UserResume2.objects.values('achievements')]
    candidates_position = [x["position"] for x in UserResume2.objects.values('position')]
    candidates_total_work_exprience = [x["total_work_exprience"] for x in UserResume2.objects.values('total_work_exprience')]
    candidates_prof_tags = [x["prof_tags"] for x in UserResume2.objects.values('prof_tags')]
    candidates_hobbies = [x["hobbies"] for x in UserResume2.objects.values('hobbies')]
    candidates_key_achievements = [x["key_achievements"] for x in UserResume2.objects.values('key_achievements')]
    candidates_career_status = [x["career_status"] for x in UserResume2.objects.values('career_status')]
    candidates_managment_experience = [x["managment_experience"] for x in UserResume2.objects.values('managment_experience')]
    candidates_score = [x["score"] for x in UserResume2.objects.values('score')]
    candidates_language_skills = [x["language_skills"] for x in UserResume2.objects.values('language_skills')]
    candidates_degree = [x["degree"] for x in UserResume2.objects.values('degree')]
    candidates_psychotype = [x["psychotype"] for x in UserResume2.objects.values('psychotype')]
    candidates_motivations = [x["motivations"] for x in UserResume2.objects.values('motivations')]

    candidates_ranks_list = [0] * len(candidates_fio)

    for required_skill in required_skills_list:
        for i in range(len(candidates_fio)):
            print("ТРЕБУЕМЫЙ НАВЫК: " + required_skill, "НАВЫКИ ПОЛЬЗОВАТЕЛЯ: " + candidates_skills[i])
            if required_skill.lower() in candidates_skills[i].lower():
                candidates_ranks_list[i] += 1

    # Далее определяем наиболее подходящих сотрудников по рангу
    your_idel_candidate = []
    max_rank = max(candidates_ranks_list)
    print(candidates_ranks_list)

    for i in range(len(candidates_ranks_list)):
        if candidates_ranks_list[i] == max_rank:
            your_idel_candidate.append({"ФИО": candidates_fio[i],
                                        "Должность": candidates_position[i],
                                        "Навыки": candidates_skills[i],
                                        "Обязанности": candidates_responsibilities[i],
                                        "Стаж": candidates_work_exprience[i],
                                        "Достижения": candidates_achievements[i],
                                        "Проф. теги": candidates_prof_tags[i]
                                        })

    return your_idel_candidate

def resume_compilation(conversation_history, user_message, auth_token):
    print(conversation_history)
    print(user_message)
    print("Здесь располагаются идеальные навыки 6: " + conversation_history[6]["content"])
    print("Здесь располагаются идеальные навыки 5: " + conversation_history[5]["content"])
    if "итоговый список" in conversation_history[6]["content"].lower():
        skills = get_chat_adhoc(auth_token, "Необходимые <навыки>: " + conversation_history[6]["content"] + """. 
                          Суммаризируй указанные <навыки> и представь их в виде <ключевых слов>.
                          Для вывода используй следующую <инструкцию>: 1) ключевые слова должны быть записаны через запятую.
                          2) Ответ должен содержать только ключевые слова </инструкция>.""").json()['choices'][0][
            'message']['content']
    else:
        skills = conversation_history[4]["content"].split("обладать следующими навыками: ")[1]
        skills = skills[:skills.index(". Также")].replace(", ", ",")

    print(conversation_history[4])

    print(skills)
    sberposition = get_chat_adhoc(auth_token,
                                  f"""О какой вакансии идет речь в следу  ющем предложении: {conversation_history[1]["content"]}?.
                                                  Без указания ничего лищнего, выведи ответ по следующей 
                                                             <инструкции>:
                                                             1) В ответе должно быть только название вакансиии
                                                             2) Не пиши ничего лишнего. </инструкция>. """).json()[
        'choices'][0]['message']['content']
    print(sberposition)

    work_experience = get_chat_adhoc(auth_token, f"""Требуемый опыт работы: {conversation_history[6]["content"]}.
                                                     Ответь пользователю, используя следующую <инструкцию>:
                                                     1) Преобразуй опыт работы в количество лет.
                                                     2) Не пиши ничего лишнего. </инструкция>. """).json()['choices'][
        0]['message']['content']
    print(work_experience)

    responsibilities = get_chat_adhoc(auth_token, "Необходимые <требования>: " + user_message + """. 
                          Суммаризируй указанные <требования> и представь их в виде <ключевых слов>.
                          Для вывода используй следующую <инструкцию>: 1) ключевые слова должны быть записаны через запятую.
                          2) Ответ должен содержать только ключевые слова </инструкция>.""").json()['choices'][0][
        'message']['content']
    print(responsibilities)
    print("РЕЗУЛЬТАТ РАБОТЫ ФУНКЦИИ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: ", skills, sberposition, work_experience, responsibilities)
    return skills, sberposition, responsibilities, work_experience

def giga_chat_response_corrected(giga_chat_response):
    if ". Кандидат:" in giga_chat_response:
        giga_chat_response = giga_chat_response.replace(". Кандидат:", ".<br>Кандидат:")
    elif " 1) " in giga_chat_response:
        giga_chat_response = giga_chat_response.replace(" 1) ", "<br>1) ")
    elif " 2) " in giga_chat_response:
        giga_chat_response = giga_chat_response.replace(" 2) ", "<br>1) ")
    elif " 3) " in giga_chat_response:
        giga_chat_response = giga_chat_response.replace(" 3) ", "<br>1) ")
    elif ". Обязанности: " in giga_chat_response:
        giga_chat_response = giga_chat_response.replace(". Обязанности: ", ".<br>Обязанности: ")
    elif ". Навыки: " in giga_chat_response:
        giga_chat_response = giga_chat_response.replace(". Навыки: ", ".<br>Навыки: ")
    else:
        pass
    return giga_chat_response

# Ниже располагаются функции для поиска наиболее похожих межжду собой слов (первый шаг проверки кандидата)