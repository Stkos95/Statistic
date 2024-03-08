
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

