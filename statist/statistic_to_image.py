from PIL import Image, ImageDraw, ImageFont



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


# font = ImageFont.truetype("Montserrat-VariableFont_wght.ttf" ,22, )
font = ImageFont.truetype(font="Inter_font/static/Inter-Regular.ttf", size= 22)
font_headers = ImageFont.truetype(font="Inter_font/static/Inter-Bold.ttf", size= 30)


font.size = 100
print(font.getbbox('h'))
for player, halfs in td.items():
    y = 10
    x = 10
    image = Image.new(size=(1000,1500), mode='RGB', color='white')
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text=f'{player}', fill='black', font=font, anchor='lt')
    x_half = image.size[0] / 4
    act = False
    x_value = 210

    for half, actions in halfs.items():
        y = 10
        x = 10

        # x_half = x_half_start + image.size[0] / 2
        draw.text((x_half, y), text=f'{half} Тайм', fill='black', font=font,anchor='mt')
        x_half =  image.size[0] - x_half

        for action, value in actions.items():
            y += 100

            if not act:
                draw.text((x, y), text=f'{action}', fill='black', font=font_headers)

            draw.text((x_value, y), text=f'{value}', fill='black', font=font)
        act = True
        x_value += 500

    # x += 200

image.show()



