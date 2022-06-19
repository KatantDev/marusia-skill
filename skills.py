import json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

categories = {
    'web': 'Разработка сайтов',
    'design': 'Дизайн',
    'gamedev': 'Разработка игр',
    'data_science': 'Анализ данных',
    'ml': 'Машинное обучение',
    'mobile': 'Мобильная разработка'
}


@app.route('/webhook', methods=['OPTIONS'])
def _():
    response = Response()
    response.status_code = 200
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
    response.headers['Access-Control-Allow-Origin'] = 'https://skill-debugger.marusia.mail.ru'
    return response


@app.route('/webhook', methods=['POST'])
def hello_world():
    request_data = request.get_json()
    response_json = {
        'session': request_data['session'],
        'version': request_data['version'],
    }

    command = request_data['request']['command'].lower()
    session = request_data['state']['session']
    if 'двфу' in command and 'лучший вуз' in command and ('вездекод' in command or 'вездеход' in command):
        response_json['response'] = {
            'tts': 'Привет вездек`одерам! Сейчас я задам тебе несколько вопросов, отвечай да или нет.\n'
                   'Ты ^умеешь^ программировать? <speaker audio=marusia-sounds/things-bell-1>',
            'text': 'Привет вездекодерам! Сейчас я задам тебе несколько вопросов, отвечай да или нет.\n'
                    'Ты умеешь программировать?',
            'end_session': False
        }
        response_json['session_state'] = {
            'question': 1,
            'design': 0,
            'gamedev': 0,
            'data_science': 0,
            'ml': 0,
            'web': 0,
            'mobile': 0
        }
    elif session.get('question') == 1:
        session['question'] += 1
        if command == 'да':
            session['design'] += 1

        response_json['response'] = {
            'tts': 'Ты ^любишь^ компьютерные игры?',
            'text': 'Ты любишь компьютерные игры?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 2:
        session['question'] += 1
        if command == 'да':
            session['gamedev'] += 1

        response_json['response'] = {
            'tts': 'Много ли времени ты проводишь в телефоне?',
            'text': 'Много ли времени ты проводишь в телефоне?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 3:
        session['question'] += 1
        if command == 'да':
            session['mobile'] += 1

        response_json['response'] = {
            'tts': 'Ты ^любишь^ математику?',
            'text': 'Ты любишь математику?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 4:
        session['question'] += 1
        if command == 'да':
            session['ml'] += 1
            session['data_science'] += 1

        response_json['response'] = {
            'tts': 'Ты ^любишь^ узнавать всё первым?',
            'text': 'Ты любишь узнавать всё первым?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 5:
        session['question'] += 1
        if command == 'да':
            session['data_science'] += 1

        response_json['response'] = {
            'tts': 'Тебе ^нравится^ листать веб-сайты?',
            'text': 'Тебе нравится листать веб-сайты?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 6:
        session['question'] += 1
        if command == 'да':
            session['web'] += 1

        response_json['response'] = {
            'tts': 'Тебе ^нравится^ рисовать?',
            'text': 'Тебе нравится рисовать?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 7:
        session['question'] += 1
        if command == 'да':
            session['design'] += 1
            session['web'] += 1

        response_json['response'] = {
            'tts': 'Ты ^любишь^ придумывать истории?',
            'text': 'Ты любишь придумывать истории?',
            'end_session': False
        }
        response_json['session_state'] = session
    elif session.get('question') == 8:
        session.pop('question')
        if command == 'да':
            session['gamedev'] += 1

        category = max(session, key=session.get)
        response_json['response'] = {
            'tts': f'Я думаю тебе стоит попробовать себя в категории: {categories[category]}'
                   f'<speaker audio=marusia-sounds/game-win-1>\nХочешь ли научиться чему-то новому?',
            'text': f'Я думаю тебе стоит попробовать себя в категории: {categories[category]}\n'
                    f'Хочешь ли научиться чему-то новому?',
            'end_session': False
        }
        response_json['session_state'] = {'vk_lessons': 1}
    elif session.get('vk_lessons') == 1:
        response_json['response'] = {
            'tts': 'Присоединяйся к VK Lessons и изучай много нового в сфере IT.',
            'text': 'Присоединяйся к VK Lessons и изучай много нового в сфере IT.',
            'card': {
                    'type': 'MiniApp',
                    'url': 'https://vk.com/app7923597'
            },
            'end_session': False
        }
    else:
        response_json['response'] = {
            'tts': 'Не понял тебя',
            'text': 'Не понял тебя :(',
            'end_session': False
        }

    response = Response(
        response=json.dumps(response_json),
        status=200,
        mimetype='application/json',
    )
    response.headers['Access-Control-Allow-Origin'] = 'https://skill-debugger.marusia.mail.ru'
    return response


app.run(port=8000)
