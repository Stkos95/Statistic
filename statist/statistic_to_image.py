from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import os
class TeamStatisticImage:
    def __init__(self, image_path: str | None = None):
        if image_path:
            self.image = Image.open(image_path)
        else:
            self.image = Image.new(size=(1000, 1500), mode='RGB', color='white')
        self.draw = ImageDraw.Draw(self.image)

    def show(self):
        self.image.show()

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
    def __init__(self):
        self.photo = None

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

    def add_player_photo(self, player_photo=None):
        if not player_photo:
            player_photo = './statist/static/img/no_image.png'
        self.photo = Image.open(player_photo).resize((200, 200))

        circular_photo = self._make_logo_circular(self.photo).convert('RGBA')
        self.image.paste(circular_photo, mask=circular_photo)

    def make_header(self, match_name, match_date, player_name, player_photo=None):
        print(os.getcwd())
        font = f"./statist/Inter_font/static/Inter-Bold.ttf"

        self.add_player_photo(player_photo)

        x = self.photo.size[0]
        y = 40
        fio_box_size = self.put_text(coords=(x, y),
                                     data=player_name,
                                     fill='black',
                                     path=f"statist/static/fonts/Inter_font/Inter-Bold.ttf",
                                     size=40,
                                     anchor='lb'
                                     )
        # self.y += fio_box_size[3] + 10
        y += 66

        date_box_size = self.put_text(coords=(x, y),
                                      data=str(match_date),
                                      fill='black',
                                      path=f"./statist/static/fonts/Inter_font/Inter-Bold.ttf",
                                      size=30
                                      )
        # self.y += date_box_size[3] + 10
        y += 66

        match_name_box_size = self.put_text(coords=(x, y),
                                            data=match_name,
                                            fill='black',
                                            path=f"./statist/static/fonts/Inter_font/Inter-Bold.ttf",
                                            size=30
                                            )
        y = 250
        x = self.image.width / 2
        self.put_text(coords=(x, y),
                      data="1 Тайм",
                      fill='black',
                      path=f"./statist/static/fonts/Inter_font/Inter-Bold.ttf",
                      size=30
                      )
        x = self.image.width / 2 + self.image.width / 4
        self.put_text(coords=(x, y),
                      data="2 Тайм",
                      fill='black',
                      path=f"./statist/static/fonts/Inter_font/Inter-Bold.ttf",
                      size=30
                      )

    def put_statistic(self, data: dict):

        y = 330
        for action, halfs in data.items():
            x = 10
            self.put_text(coords=(x, y),
                          data=action,
                          fill='black',
                          path=f"./statist/static/fonts/Inter_font/Inter-Black.ttf",
                          size=30
                          )

            x = self.image.width / 2

            self.put_text(coords=(x, y),
                          data=f'{halfs["1"]}',
                          fill='black',
                          path=f"./statist/static/fonts/Inter_font/Inter-Medium.ttf",
                          size=30
                          )
            x = self.image.width / 2 + self.image.width / 4

            self.put_text(coords=(x, y),
                          data=f'{halfs["2"]}',
                          fill='black',
                          path=f"./statist/static/fonts/Inter_font/Inter-Regular.ttf",
                          size=30
                          )
            y += 100

    def save_to_bytes(self):
        byte = BytesIO()
        self.image.save(byte, format='JPEG')
        return byte

