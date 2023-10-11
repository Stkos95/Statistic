from PIL import Image, ImageDraw, ImageFont, ImageOps

# test_dict = {'546': {'peredacha': {'value': '2', 'russian_name': 'Передача'}, 'fol': {'value': '0', 'russian_name': 'Фол'}}, 'ываыва': {'peredacha': {'value': '0', 'russian_name': 'Передача'}, 'fol': {'value': '3', 'russian_name': 'Фол'}}}
td = {'Женя': {'1': {'Обводка': '0 / 0 / 0',
                     'Отбор': '0 / 0 / 0',
                     'Передача вперед БЕЗ сопр': '0 / 0 / 0',
                     'Передача вперед с сопр.': '0 / 0 / 0',
                     'Передача назад БЕЗ сопр': '0 / 0 / 0',
                     'Передача назад с сопр': '0 / 0 / 0',
                     'Перехват': '0 / 0 / 0',
                     'Прием мяча': '0 / 0 / 0',
                     'ТТД': 0,
                     'Удар из штрафной': '0 / 0 / 0',
                     'Удар из-за штрафной': '0 / 0 / 0'},
               '2': {'Обводка': '0 / 0 / 0',
                     'Отбор': '0 / 0 / 0',
                     'Передача вперед БЕЗ сопр': '0 / 0 / 0',
                     'Передача вперед с сопр.': '0 / 0 / 0',
                     'Передача назад БЕЗ сопр': '0 / 0 / 0',
                     'Передача назад с сопр': '0 / 0 / 0',
                     'Перехват': '0 / 0 / 0',
                     'Прием мяча': '0 / 0 / 0',
                     'ТТД': 0,
                     'Удар из штрафной': '0 / 0 / 0',
                     'Удар из-за штрафной': '0 / 0 / 0'}},
      'Илья': {'1': {'Обводка': '0 / 0 / 0',
                     'Отбор': '0 / 0 / 0',
                     'Передача вперед БЕЗ сопр': '0 / 0 / 0',
                     'Передача вперед с сопр.': '0 / 0 / 0',
                     'Передача назад БЕЗ сопр': '0 / 0 / 0',
                     'Передача назад с сопр': '0 / 0 / 0',
                     'Перехват': '0 / 0 / 0',
                     'Прием мяча': '0 / 0 / 0',
                     'ТТД': 0,
                     'Удар из штрафной': '0 / 0 / 0',
                     'Удар из-за штрафной': '0 / 0 / 0'},
               '2': {'Обводка': '2 / 1 / 50',
                     'Отбор': '0 / 0 / 0',
                     'Передача вперед БЕЗ сопр': '0 / 0 / 0',
                     'Передача вперед с сопр.': '0 / 0 / 0',
                     'Передача назад БЕЗ сопр': '0 / 0 / 0',
                     'Передача назад с сопр': '0 / 0 / 0',
                     'Перехват': '0 / 0 / 0',
                     'Прием мяча': '0 / 0 / 0',
                     'ТТД': 2,
                     'Удар из штрафной': '0 / 0 / 0',
                     'Удар из-за штрафной': '0 / 0 / 0'}},
      'Костя': {'1': {'Обводка': '1 / 0 / 0',
                      'Отбор': '1 / 1 / 100',
                      'Передача вперед БЕЗ сопр': '0 / 0 / 0',
                      'Передача вперед с сопр.': '0 / 0 / 0',
                      'Передача назад БЕЗ сопр': '0 / 0 / 0',
                      'Передача назад с сопр': '0 / 0 / 0',
                      'Перехват': '0 / 0 / 0',
                      'Прием мяча': '0 / 0 / 0',
                      'ТТД': 2,
                      'Удар из штрафной': '0 / 0 / 0',
                      'Удар из-за штрафной': '0 / 0 / 0'},
                '2': {'Обводка': '0 / 0 / 0',
                      'Отбор': '0 / 0 / 0',
                      'Передача вперед БЕЗ сопр': '0 / 0 / 0',
                      'Передача вперед с сопр.': '0 / 0 / 0',
                      'Передача назад БЕЗ сопр': '0 / 0 / 0',
                      'Передача назад с сопр': '0 / 0 / 0',
                      'Перехват': '0 / 0 / 0',
                      'Прием мяча': '0 / 0 / 0',
                      'ТТД': 2,
                      'Удар из штрафной': '2 / 0 / 0',
                      'Удар из-за штрафной': '0 / 0 / 0'}}}

# d = Image.new(mode="RGB", size=(500, 500), color='white')
# draw = ImageDraw.Draw(d)

#
# class ImageProcessing:
#
#     def __init__(self,
#                  mode: str = 'RGB',
#                  size: tuple = (500, 500),
#                  color: str = 'white'):
#
#         self.image = Image.new(mode=mode, size=size, color=color)
#         self.draw = ImageDraw.Draw(self.image)
#
#     def draw_text(self, coords: tuple, text: str):
#         draw.text(coords, text=text, fill='black', font=font)


y = 10
x = 10


class TeamStatisticImage:
    def __init__(self, image_path: str | None = None):
        if image_path:
            self.image = Image.open(image_path)
        else:
            self.image = Image.new(size=(1000, 1500), mode='RGB', color='white')
        self.draw = ImageDraw.Draw(self.image)

    def _get_font(self, path: str, size: int):
        return ImageFont.truetype(path, size)

    def put_text(self,
                 coords: tuple,
                 data: str,
                 fill: str,
                 path: str,
                 size: int,
                 **kwargs) -> tuple:
        font = self._get_font(path=path, size=size)
        self.draw.text(coords, data, fill=fill, font=font, **kwargs)
        return font.getbbox(data)


class OurTeamImage(TeamStatisticImage):
    def __init__(self, player_name, match_date, match_name):
        self.x = self.y = 10
        self.photo = Image.open('../players/photo_1_2023-10-09_15-21-35.jpg').resize((200, 200))
        self.player_name = player_name
        self.match_name = match_name
        self.match_date = match_date
        super().__init__()

    @staticmethod
    def _make_logo_circular(team_logo):
        mask = Image.new('L', team_logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + team_logo.size, fill=255)
        # mask = mask.resize(mask.size, Image.ANTIALIAS)
        out = ImageOps.fit(team_logo, mask.size, centering=(0.5, 0.5))
        out.putalpha(mask)
        return out

    def add_player_photo(self):
        photo = self._make_logo_circular(self.photo)
        self.image.paste(photo, mask=photo)

    # def put_fio(self, coords, data):
    #     font = self.put_text(coords=coords,
    #                   data=data,
    #                   fill='black',
    #                   path="Inter_font/static/Inter-Bold.ttf",
    #                   size=40
    #                   )
    # #
    #     return font.getbbox(data)
    #
    # def put_date(self, coords, data):
    #     font = self.put_text(coords=coords,
    #                   data=data,
    #                   fill='black',
    #                   path="Inter_font/static/Inter-Bold.ttf",
    #                   size=30
    #                   )
    #
    #     return font.getbbox(data)
    #
    # def put_match_name(self, coords, data):
    #     font = self.put_text(coords=coords,
    #                   data=data,
    #                   fill='black',
    #                   path="Inter_font/static/Inter-Bold.ttf",
    #                   size=30
    #                   )
    #
    #     return font.getbbox(data)

    def make_header(self):
        self.add_player_photo()
        self.x += self.photo.size[0]
        fio_box_size = self.put_text(coords=(self.x, self.y + 40),
                                     data=self.player_name,
                                     fill='black',
                                     path="Inter_font/static/Inter-Bold.ttf",
                                     size=40,
                                     anchor='lb'
                                     )
        # self.y += fio_box_size[3] + 10
        self.y += 66

        date_box_size = self.put_text(coords=(self.x, self.y),
                                      data=self.match_date,
                                      fill='black',
                                      path="Inter_font/static/Inter-Bold.ttf",
                                      size=30
                                      )
        # self.y += date_box_size[3] + 10
        self.y += 66

        match_name_box_size = self.put_text(coords=(self.x, self.y),
                                      data=self.match_name,
                                      fill='black',
                                      path="Inter_font/static/Inter-Bold.ttf",
                                      size=30
                                      )
        self.image.show()


    def put_first_half(self):


    def put_statistic(self):
        pass



d = OurTeamImage(player_name='Ступенко Константин', match_date='10.10.2003', match_name='МФК "Луч" - МФК "Партизан"')
d.make_header()






# d.add_player_photo()
# d.put_fio()

# font = ImageFont.truetype(font="Inter_font/static/Inter-Regular.ttf", size=22)
# font_headers = ImageFont.truetype(font="Inter_font/static/Inter-Bold.ttf", size=30)
#
# font.size = 100
# print(font.getbbox('h'))
# for player, halfs in td.items():
#     y = 10
#     x = 10
#     image = Image.new(size=(1000, 1500), mode='RGB', color='white')
#     draw = ImageDraw.Draw(image)
#     draw.text((x, y), text=f'{player}', fill='black', font=font, anchor='lt')
#     x_half = image.size[0] / 4
#     act = False
#     x_value = 210
#
#     for half, actions in halfs.items():
#         y = 10
#         x = 10
#
#         # x_half = x_half_start + image.size[0] / 2
#         draw.text((x_half, y), text=f'{half} Тайм', fill='black', font=font, anchor='mt')
#         x_half = image.size[0] - x_half
#
#         for action, value in actions.items():
#             y += 100
#
#             if not act:
#                 draw.text((x, y), text=f'{action}', fill='black', font=font_headers)
#
#             draw.text((x_value, y), text=f'{value}', fill='black', font=font)
#         act = True
#         x_value += 500
#
#     # x += 200
#
# image.show()
