"""
Fantasy World Motivator — мой первый проект чат‑бота.
Он помогает придумывать идеи для собственного фэнтези‑мира: названия, локации,
особенности народов, конфликты и всё, что помогает начать писать книгу,
комикс или игру. Я сделала его простым и понятным.
Запуск:
1) Открыть терминал
2) Выполнить: python fantasy_motivator_bot.py
3) Следовать меню на экране
Дополнительно:
- если есть TELEGRAM_TOKEN → бот будет работать в Telegram
- если есть OPENAI_API_KEY → ответы станут более творческими
"""
import os
import json
import random
import time
from typing import Dict, Any, Optional
# ---------------------------
# Конфигурация и ресурсы
# ---------------------------
STATE_FILE = 'fantasy_state.json'
SAMPLE_INSPIRATIONS = [
    'Властелин колец (эпическая масштабность, мифология, карты)',
    'Песнь Льда и Огня (политика, интриги, жестокие последствия)',
    'Гарри Поттер (учебная школа, тайны и артефакты)',
    'Колесо Времени (циклы времени, легенды, масштабные пророчества)',
    'Туве Янссон (атмосферность, камерность — применимо к фэнтези для детей/подростков)',
    'Борис Акунин (русская стилистика, детектив в историческом мире — как вдохновение)',
    'Ник Перумов / Мария Семёнова (русские фэнтези-нотки и фольклорные мотивы)'
]
# Примитивная таблица сущностей для генерации
RACES = ['люди', 'эльфы', 'карлики', 'полуэлементы', 'тени', 'кинетические звери']
TRAITS = ['воинственные', 'миролюбивые', 'торгующие', 'кладущие акцент на магию', 'прибежища мудрецов']
LOCALES = ['горные крепости', 'туманные леса', 'песчаные пустоши', 'плавучие острова', 'подземные города']
CONFLICTS = ['борьба за ресурс', 'древний ритуал, пробуждающий чудовище', 'власть и предательство', 'классовое восстание']
# ---------------------------
# Простая сохранялка состояния
# ---------------------------
def load_state() -> Dict[str, Any]:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}
def save_state(state: Dict[str, Any]):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
# ---------------------------
# LLM-интеграция (опционально)
# ---------------------------
def get_llm_response(prompt: str, mode: str = 'simulate') -> str:
    """
    Если в окружении есть OPENAI_API_KEY — используйте реальный вызов OpenAI.
    Иначе — сгенерируйте безопасный локальный ответ.
    mode: 'simulate'|'openai' (openai будет выбран автоматически при наличии ключа)
    """
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        try:
            import openai
            openai.api_key = openai_key
            # Небольшой, аккуратный промпт — модель дополняет и расширяет идеи
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=250,
                temperature=0.8,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"[Ошибка OpenAI: {e}]"
    # Если нет ключа — имитируем ответ
    return simulate_llm(prompt)
def simulate_llm(prompt: str) -> str:
    """Простая имитация — комбинируем шаблоны и случайности для правдоподобных идей."""
    # Попытка угадать что хочет пользователь по ключевым словам
    p = prompt.lower()
    pieces = []
    if 'имя' in p or 'name' in p:
        pieces.append(generate_name())
    if 'лок' in p or 'place' in p or 'лока' in p:
        pieces.append(f"Локация: {random.choice(LOCALES)}")
    if 'рас' in p or 'race' in p:
        pieces.append(f"Население: {random.choice(RACES)} — {random.choice(TRAITS)}")
    if 'конфликт' in p or 'conflict' in p:
        pieces.append(f"Конфликт: {random.choice(CONFLICTS)}")
    if not pieces:
        # общий набор идей
        pieces = [
            f"Идея: {random.choice(SAMPLE_INSPIRATIONS)} как вдохновение.",
            f"Местность: {random.choice(LOCALES)}.",
            f"Главный конфликт: {random.choice(CONFLICTS)}.",
            f"Народ: {random.choice(RACES)} с чертой — {random.choice(TRAITS)}."
        ]
    # Собираем ответ в пару предложений
    return ' '.join(pieces)
# ---------------------------
# Генераторы простых элементов
# ---------------------------
def generate_name() -> str:
    syl1 = ['Ara', 'Vor', 'Ely', 'Mar', 'Gal', 'Zin', 'Kor', 'Thal']
    syl2 = ['dor', 'wen', 'mir', 'th', 'ion', 'ska', 'vyr', 'eon']
    name = random.choice(syl1) + random.choice(syl2)
    # Небольшая вариативность
    if random.random() < 0.3:
        name += '-' + random.choice(['a', 'i', 'o']) + random.choice(['n', 'r'])
    return name
def generate_brief_world(tone: str = 'эпический') -> str:
    # Простейшая логика на основе выбранного тона
    tone = tone.lower()
    if tone not in ['эпический', 'тёмный', 'лёгкий', 'комичный']:
        tone = 'эпический'
    prompts = {
        'эпический': 'широкие описания, древние империи, пророчества и масштабные конфликты',
        'тёмный': 'моральная неоднозначность, утраты, закулисные интриги',
        'лёгкий': 'юмор, уютные поселения, маленькие приключения',
        'комичный': 'абсурд, неожиданные повороты, пародийные элементы'
    }
    insp = random.choice(SAMPLE_INSPIRATIONS)
    world = (
        f"Тон — {tone}. Вдохновение: {insp}. "+
        f"Мир: {random.choice(LOCALES)}, населён {random.choice(RACES)}. "+
        f"Ключевой конфликт: {random.choice(CONFLICTS)}. "
    )
    # небольшая подсказка для автора
    world += f"Совет: попробуйте соединить {prompts[tone]} с локальной легендой или необычным артефактом."
    return world
# ---------------------------
# Логика меню / обработка команд
# ---------------------------
def print_main_menu():
    print('\n=== Мой Фентези Мир — Мотиватор ===')
    print('1. Сгенерировать идею мира')
    print('2. Сгенерировать имя персонажа/места/артефакта')
    print('3. Получить вдохновение (перечень авторов/мотивов)')
    print('4. Сохранить текущую идею')
    print('5. Загрузить последнюю идею')
    print('6. Показать примеры диалогов и подсказки по LLM')
    print('0. Выход')
def console_demo():
    state = load_state()
    current = state.get('current', {})
    while True:
        print_main_menu()
        choice = input('Выберите опцию (0-6): ').strip()
        if choice == '0':
            print('Пока! Сохраняю состояние...')
            state['current'] = current
            save_state(state)
            break
        elif choice == '1':
            tone = input('Какой тон вам нравится? (эпический/тёмный/лёгкий/комичный): ').strip()
            idea = generate_brief_world(tone)
            print('\n' + idea + '\n')
            current['idea'] = idea
        elif choice == '2':
            what = input('Нужно имя для (персонажа/места/артефакта): ').strip().lower()
            prompt = f'Сгенерируй имя для {what} в стиле эпического фэнтези.'
            name = get_llm_response(prompt)
            print('\n' + name + '\n')
            current.setdefault('names', []).append(name)
        elif choice == '3':
            print('\nВдохновляющие авторы/мотивы:')
            for i, s in enumerate(SAMPLE_INSPIRATIONS, 1):
                print(f'{i}. {s}')
            print('\nПопробуйте объединить элементы из нескольких пунктов.')
        elif choice == '4':
            if not current:
                print('Нечего сохранять — сначала сгенерируйте идею.')
            else:
                state['current'] = current
                save_state(state)
                print('Идея сохранена.')
        elif choice == '5':
            state = load_state()
            current = state.get('current', {})
            if not current:
                print('Сохранений не найдено.')
            else:
                print('\nПоследняя сохранённая идея:')
                print(json.dumps(current, ensure_ascii=False, indent=2))
        elif choice == '6':
            print_examples()
        else:
            print('Неверный ввод — введите число от 0 до 6.')
def print_examples():
    ex = '''
Примеры использования LLM-подсказок (рекомендации для интеграции)
:
- "Сделай краткое описание мира в тоне эпик‑фэнтези, 3 предложения, добавь один неожиданный поворот."
- "Придумай 5 вариантов имен для эльфийского города — короткие, запоминающиеся." 
- "Опиши конфликт между магами и ремесленниками: мотивации каждой стороны, три ключевые сцены." 
Если вы используете реальную LLM, храните API-ключ в переменной окружения OPENAI_API_KEY —
не храните его в коде и не публикуйте в репозиториях.
'''
    print(ex)
# ---------------------------
# (Опционально) Telegram-интеграция — простая
# ---------------------------
def run_telegram_bot():
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        print('TELEGRAM_TOKEN не задан — Telegram режим недоступен. Запустите в консоли.')
        return
    try:
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
        updater = Updater(token=token, use_context=True)
        dp = updater.dispatcher
        def start(update, context):
            update.message.reply_text('Привет! Я помогу придумать миры. Используй /idea или /name')
        def idea(update, context):
            tone = 'эпический'
            if context.args:
                tone = context.args[0]
            update.message.reply_text(generate_brief_world(tone))
        def name_cmd(update, context):
            what = 'персонаж'
            if context.args:
                what = ' '.join(context.args)
            prompt = f'Сгенерируй имя для {what} в стиле эпического фэнтези.'
            update.message.reply_text(get_llm_response(prompt))
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CommandHandler('idea', idea))
        dp.add_handler(CommandHandler('name', name_cmd))
        print('Запускаю Telegram бот (polling). Нажмите Ctrl+C для остановки.')
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print('Ошибка при запуске Telegram части:', e)
        print('Убедитесь, что установлена библиотека python-telegram-bot и токен корректен.')
# ---------------------------
# Точка входа
# ---------------------------
if name == 'main':
    print('Запуск файла fantasy_motivator_bot.py')
    # Если задан TELEGRAM_TOKEN — предлагаем Telegram режим, но всё равно не требуем ключа.
    if os.environ.get('TELEGRAM_TOKEN'):
        run_telegram_bot()
    else:
        console_demo()