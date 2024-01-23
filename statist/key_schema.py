


class KeySchema:
    def hash_match_player_half(self, match_id, player_id, half_id) -> str:
        """
        :return [match_id]:[player_id]:[half_id]
        """
        return f'{match_id}:{player_id}:{half_id}'
