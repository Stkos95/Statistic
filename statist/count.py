from pprint import pprint

td = {'Женя': {'1': {'Обводка': {'fail': '0', 'success': '0'},
                     'Отбор': {'fail': '0', 'success': '0'},
                     'Передача вперед БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача вперед с сопр.': {'fail': '0', 'success': '0'},
                     'Передача назад БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача назад с сопр': {'fail': '0', 'success': '0'},
                     'Перехват': {'fail': '0', 'success': '0'},
                     'Прием мяча': {'fail': '0', 'success': '0'},
                     'Удар из штрафной': {'fail': '0', 'success': '0'},
                     'Удар из-за штрафной': {'fail': '0', 'success': '0'}},
               '2': {'Обводка': {'fail': '0', 'success': '0'},
                     'Отбор': {'fail': '0', 'success': '0'},
                     'Передача вперед БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача вперед с сопр.': {'fail': '0', 'success': '0'},
                     'Передача назад БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача назад с сопр': {'fail': '0', 'success': '0'},
                     'Перехват': {'fail': '0', 'success': '0'},
                     'Прием мяча': {'fail': '0', 'success': '0'},
                     'Удар из штрафной': {'fail': '0', 'success': '0'},
                     'Удар из-за штрафной': {'fail': '0', 'success': '0'}}},
      'Илья': {'1': {'Обводка': {'fail': '0', 'success': '0'},
                     'Отбор': {'fail': '0', 'success': '0'},
                     'Передача вперед БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача вперед с сопр.': {'fail': '0', 'success': '0'},
                     'Передача назад БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача назад с сопр': {'fail': '0', 'success': '0'},
                     'Перехват': {'fail': '0', 'success': '0'},
                     'Прием мяча': {'fail': '0', 'success': '0'},
                     'Удар из штрафной': {'fail': '0', 'success': '0'},
                     'Удар из-за штрафной': {'fail': '0', 'success': '0'}},
               '2': {'Обводка': {'fail': '1', 'success': '1'},
                     'Отбор': {'fail': '0', 'success': '0'},
                     'Передача вперед БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача вперед с сопр.': {'fail': '0', 'success': '0'},
                     'Передача назад БЕЗ сопр': {'fail': '0', 'success': '0'},
                     'Передача назад с сопр': {'fail': '0', 'success': '0'},
                     'Перехват': {'fail': '0', 'success': '0'},
                     'Прием мяча': {'fail': '0', 'success': '0'},
                     'Удар из штрафной': {'fail': '0', 'success': '0'},
                     'Удар из-за штрафной': {'fail': '0', 'success': '0'}}},
      'Костя': {'1': {'Обводка': {'fail': '1', 'success': '0'},
                      'Отбор': {'fail': '0', 'success': '1'},
                      'Передача вперед БЕЗ сопр': {'fail': '0', 'success': '0'},
                      'Передача вперед с сопр.': {'fail': '0', 'success': '0'},
                      'Передача назад БЕЗ сопр': {'fail': '0', 'success': '0'},
                      'Передача назад с сопр': {'fail': '0', 'success': '0'},
                      'Перехват': {'fail': '0', 'success': '0'},
                      'Прием мяча': {'fail': '0', 'success': '0'},
                      'Удар из штрафной': {'fail': '0', 'success': '0'},
                      'Удар из-за штрафной': {'fail': '0', 'success': '0'}},
                '2': {'Обводка': {'fail': '0', 'success': '0'},
                      'Отбор': {'fail': '0', 'success': '0'},
                      'Передача вперед БЕЗ сопр': {'fail': '0', 'success': '0'},
                      'Передача вперед с сопр.': {'fail': '0', 'success': '0'},
                      'Передача назад БЕЗ сопр': {'fail': '0', 'success': '0'},
                      'Передача назад с сопр': {'fail': '0', 'success': '0'},
                      'Перехват': {'fail': '0', 'success': '0'},
                      'Прием мяча': {'fail': '0', 'success': '0'},
                      'Удар из штрафной': {'fail': '2', 'success': '0'},
                      'Удар из-за штрафной': {'fail': '0', 'success': '0'}}}}


result_TTD = {}


def accumulate_statistic(player_actions ):
    result_actions = {}
    for half, actions in player_actions.items():
        ttd = 0
        result_actions.setdefault(half, {})
        for action, status in actions.items():
            success = int(status['success'])
            fail = int(status['fail'])
            total = success + fail
            try:
                percent_success = int(success / total * 100)
            except ZeroDivisionError:
                percent_success = 0
            value = f'{total} / {success} / {percent_success} %'
            result_actions[half][action] = value
            ttd += success + fail
        # result_actions[player][half]['ТТД'] = ttd

    return result_actions

