# PokerAnalytics

Небольшой Python-проект для анализа покерных раздач: оценка комбинаций,
equity/outs и решение о выгодности колла по pot odds и EV.

## Установка

Требуется Python 3.10+.

```bash
cd "/Users/amanatkorgan/Desktop/my projects/PokerAnalytics"
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

Карты записываются двумя символами: ранг `2`–`9`, `T`, `J`, `Q`, `K`, `A` и
масть `s` (пики), `h` (черви), `d` (бубны), `c` (трефы), например `As`.

## Основной API

- `poker.evaluator.evaluate_hand(cards)` — возвращает оценку комбинации;
  поддерживаются `HIGH_CARD`, `ONE_PAIR`, `TWO_PAIR`, `THREE_OF_A_KIND`,
  `STRAIGHT`, `FLUSH`, `FULL_HOUSE`, `FOUR_OF_A_KIND`, `STRAIGHT_FLUSH` и
  `ROYAL_FLUSH`.
- `poker.equity.calculate_equity(hero_cards, board, villain_cards=None)` —
  вероятность победы героя; неизвестные карты перебираются или моделируются
  реализацией модуля.
- `poker.equity.calculate_outs(hero_cards, board, villain_cards=None)` — карты,
  улучшающие руку на следующей улице.
- `poker.odds.pot_odds(pot_size, call_amount)` — требуемая equity:
  `call_amount / (pot_size + call_amount)`.
- `poker.odds.expected_value(pot_size, call_amount, equity)` — EV колла:
  `equity * (pot_size + call_amount) - call_amount`.

Размеры банка и ставки должны быть неотрицательными, а `equity` — числом от
`0` до `1`.

## Study и Live режимы

**Study** предназначен для разбора сохранённых раздач и обучения. Можно
использовать полную информацию о картах, повторяемые расчёты и перебор
вариантов. Результат не следует считать подсказкой во время игры.

**Live** предназначен для расчёта в реальном времени. Он должен получать только
доступные игроку данные, учитывать задержку и лимит вычислений, а неизвестные
карты — моделировать. Перед использованием проверьте правила площадки:
автоматизированные подсказки, чтение экрана и внешние трекеры могут быть
запрещены. Этот проект не гарантирует точность Live-оценок и не заменяет
решение игрока.

## Тесты

Запустить весь набор:

```bash
python -m pytest
```

С покрытием:

```bash
python -m pytest --cov=poker --cov-report=term-missing
```

Отдельные области:

```bash
python -m pytest tests/test_evaluator.py
python -m pytest tests/test_equity.py
python -m pytest tests/test_odds.py
```

Тесты покрывают все категории комбинаций, ace-low straight, сравнение кикеров,
дубликаты карт, базовые equity и outs, pot odds, break-even EV и валидацию
входных значений.
