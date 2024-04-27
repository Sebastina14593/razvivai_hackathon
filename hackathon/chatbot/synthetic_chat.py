import time
def synthetic_chat_generation(message):
    time.sleep(5)
    if "расскажи про первый" in message:
        return """На текущей должности Светлана использует следующие навыки: управление командой, анализ финансовых данных, анализ рисков, коммуникационные навыки, организация рабочих процессов, управление проектом. В вашей команде есть три сотрудника, которые потенциально могут выполнять эти обязанности в рамках освобожденной должности:
                  <br><br>1. Сергей Петров (<a href = 'http://127.0.0.1:8000/resumes/5'>профиль</a>): 90 баллов; Сергей обладает навыками: анализ финансовых данных, анализ рисков, коммуникационные навыки, управление проектом, стратегическое мышление, креативность, умение работать в режиме многозадачности. Необходимо улучшить навык: управление командой.
                  <br><br>2. Лидия Яковлева (<a href = 'http://127.0.0.1:8000/resumes/5'>профиль</a>): 88 баллов; Лидия обладает навыками: анализ финансовых данных, коммуникационные навыки, организация рабочих процессов, управление проектом, стрессоустойчивость. Необходимо улучшить навык: управление командой, анализ рисков.
                  <br><br>3. Олег Дубов (<a href = 'http://127.0.0.1:8000/resumes/5'>профиль</a>): 86 баллов; Олег обладает навыками: анализ финансовых данных, анализ рисков, коммуникационные навыки, стрессоустойчивость. Необходимо улучшить навыки: управление командой, управление проектом.
                  <br><br>Я могу построить траектории по освоению оставшихся навыков. Рассказать ли подробнее о каком-то из кандидатов?
                """
    elif "расскажи о сергее" in message.lower():
        return """Как руководитель проекта в банке, Сергей проявляет высокую компетенцию в организации рабочих процессов, анализе финансовых данных и управлении командой. Его опыт в области проектного управления позволяет ему успешно достигать целей и решать сложные задачи в срок. Предлагаю следующую траекторию для подготовки Сергея к замене Светланы:

                <br><br>1. Адаптация к новым обязанностям: Проведение индивидуальных сессий с Светланой для погружения в специфику её работы и методики, которые она применяет.

                <br><br>2. Развитие недостающих навыков: Организация тренингов и курсов, направленных на усовершенствование навыков, в которых Сергей ещё не достаточно компетентен, чтобы полностью занять позицию Светланы. Это может включать в себя обучение методам анализа рисков, коммуникационным навыкам или стратегическому планированию.

                <br><br>3. Практическое применение полученных знаний: Предложение проектов или задач, которые позволят Сергею применить новые навыки на практике под руководством Светланы. Например, возможностей для участия в совместных проектах, где он сможет наблюдать и учиться от неё.

                <br><br>4. Обратная связь и мониторинг: Регулярные сессии обратной связи и оценки прогресса, чтобы убедиться, что Сергей эффективно осваивает новые навыки и готов к переходу на новую должность.

                <br>Вы хотите оставить Сергея или предложить анализ по другим кандидатам?
                """
    elif "только по сергею" in message.lower():
        return """Хорошо, оставляю рекомендации только по Сергею. Есть ли еще что-то, что вы хотели бы уточнить или изменить?"""
    elif "нам поручили" in message.lower():
        time.sleep(2)
        return """Для успешного внедрения GigaChat необходимо обладать следующими навыками:

                <br><br>1. Знание языка программирования Python: GigaChat написана на Python, поэтому важно иметь базовые знания этого языка.

                <br><br>2. Опыт работы с нейросетями: GigaChat использует нейросети для обработки естественного языка (NLP) и генерации текста. Понимание принципов работы нейросетей и опыт работы с ними будут полезны при внедрении GigaChat.

                <br><br>3. Умение работать с API: GigaChat предоставляет RESTful API, который позволяет интегрировать ее в различные приложения и веб-сайты. Навыки работы с API помогут вам эффективно использовать возможности GigaChat.

                <br><br>4. Аналитические способности: GigaChat может обрабатывать большие объемы данных и предоставлять аналитику. Важно уметь анализировать данные и интерпретировать результаты, чтобы принимать обоснованные решения на основе полученной информации.

                <br><br>5. Коммуникативные навыки: GigaChat является инструментом коммуникации, поэтому умение ясно и четко выражать свои мысли и идеи будет полезным при работе с ней.

                <br><br>6. Готовность к обучению: GigaChat постоянно развивается и улучшается, поэтому важно быть готовым к изучению новых функций и возможностей.

                <br><br>Я нашел 3 кандидатов, которые могут подходить под эти требования.<br><br>Интересно ли вам это?
"""
    elif "да" in message.lower():
        return """В вашей команде есть 3 кандидата, которым вы можете поручить проект по внедрению GigaChat:
                <br><br>1. Иван Загородный (<a href = 'http://127.0.0.1:8000/resumes/5'>ссылка</a>): совпадение 90% навыков;
                <br><br>2. Павел Иванов (<a href = 'http://127.0.0.1:8000/resumes/5'>ссылка</a>): совпадение 80% навыков;
                <br><br>3. Николай Пирогов (<a href = 'http://127.0.0.1:8000/resumes/5'>ссылка</a>): совпадение 75% навыков.
                <br><br>Рассказать ли подробнее о каком-то из кандидатов?
                """

    else:
        return "Наконец то"

def synthetic_chat_generation2(message):
    time.sleep(5)
    if "создай мне" in message.lower():
        return """
               Ушедший аналитик данных: Павел Иванов. Вам составить описание вакансии на основе его опыта и навыков или вы хотите завести новую вакансию?
               """
    elif "составь описание" in message.lower():
        return """
               Я составил описание вакансии аналитика данных по ушедшему аналитику:
               <br><br>Навыки: Python, SQL, PostgreSQL, Qlik Sense, Grafana
               <br><br>Обязанности: Анализ источников данных.
               <br><br>Написание и оптимизация SQL запросов. Автоматизация дэшбордов в QlikSense.
               <br<br>Проведение A/B тестов
               <br><br>Создать новую вакансию на должности аналитика данных?
               """
    elif "да" == message.lower():
        return """
                       Я создал новую вакансию на должность аналитик данных.
                       Также нашел внутренних кандидатов, подходящих под описание:
                       Кандидат: Демин Тимофей Михайлович (<a href="/resumes/18" target="_blank">резюме</a>)
                       <br>1) Оценка: 90 баллов.
                       <br>2) Преимущества кандидата: Имеет опыт работы в должности главного аналитика, что соответствует требованиям вакансии. Также обладает навыками PostgreSQL, Python, Grafana, Linux, что делает его квалифицированным для выполнения обязанностей аналитика данных.
                       <br>3) Недостатки кандидата: Не указаны конкретные достижения. Отсутствует опыт работы с Qlik Sense.

                       <br><br>Кандидат: Соболев Ярослав Романович (<a href="/resumes/18" target="_blank">резюме</a>)
                       <br>1) Оценка: 90 баллов.
                       <br>2) Преимущества кандидата: Владеет знаниями в области статистического анализа данных, имеет опыт работы с базами данных и SQL.
                       <br>3) Недостатки кандидата: Отсутствие достижений в резюме. Отсутствие опыта работы с инструментами визуализации данных, такими как Grafana или Qlik Sense.

                       <br><br>Кандидат: Капустин Артём Дмитриевич (<a href="/resumes/18" target="_blank">резюме</a>)
                       <br>1) Оценка: 80 баллов.
                       <br>2) Преимущества кандидата: Имеет опыт работы с Python, СУБД Oracle, Linux, и Agile methodologies. Обладает навыками, необходимыми для должности аналитика.
                       <br>3) Недостатки кандидата: Отсутствие достижений в резюме. Отсутствует опыт работы с СУБД PostgreSQL. Отсутствие опыта работы с инструментами визуализации данных, такими как Grafana или Qlik Sense.
                       Заинтересовал ли вас кто-то? 

                       """

    elif "да, я хочу" in message.lower():
        return """Прекрасно, отправить ему предложение рассмотреть вакансию?"""

    elif "отправь" in message.lower():
        return """Я направил ему коммуникацию и сразу же сообщу о любых новостях. Есть ли у вас еще вопросы?"""

    else:
        return "человеческое существо"