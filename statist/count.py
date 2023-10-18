from pprint import pprint

xx = {'Обводка': {'1': {'fail': '1', 'success': '0'},
                  '2': {'fail': '0', 'success': '0'}},
      'Отбор': {'1': {'fail': '0', 'success': '1'},
                '2': {'fail': '0', 'success': '0'}},
      'Передача вперед БЕЗ сопр': {'1': {'fail': '0',
                                         'success': '0'},
                                   '2': {'fail': '0',
                                         'success': '0'}},
      'Передача вперед с сопр.': {'1': {'fail': '0',
                                        'success': '0'},
                                  '2': {'fail': '0',
                                        'success': '0'}},
      'Передача назад БЕЗ сопр': {'1': {'fail': '0',
                                        'success': '0'},
                                  '2': {'fail': '0',
                                        'success': '0'}},
      'Передача назад с сопр': {'1': {'fail': '0',
                                      'success': '0'},
                                '2': {'fail': '0',
                                      'success': '0'}},
      'Перехват': {'1': {'fail': '0', 'success': '0'},
                   '2': {'fail': '0', 'success': '0'}},
      'Прием мяча': {'1': {'fail': '0', 'success': '0'},
                     '2': {'fail': '0', 'success': '0'}},
      'Удар из штрафной': {'1': {'fail': '0', 'success': '0'},
                           '2': {'fail': '2', 'success': '0'}},
      'Удар из-за штрафной': {'1': {'fail': '0',
                                    'success': '0'},
                              '2': {'fail': '0',
                                    'success': '0'}}}

result_TTD = {}


def accumulate_statistic(player_actions):
    result_actions = {}
    for action_name, halfs in player_actions.items():
        result_actions.setdefault(action_name, {})
        for half, values in halfs.items():
            result_actions[action_name].setdefault(half, {})
            success = int(values['success'])
            fail = int(values['fail'])
            total = success + fail
            try:
                percent_success = int(success / total * 100)
            except ZeroDivisionError:
                percent_success = 0
            value = f'{total} / {success} / {percent_success} %'
            result_actions[action_name][half] = value
    return result_actions

#
# z = accumulate_statistic(xx)
# print(z)