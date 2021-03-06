from bs4 import BeautifulSoup
import requests
import pandas as pd


class Melon(object):
    url = 'https://www.melon.com/chart/index.htm?'
    headers = {'User-Agent':'Mozilla/5.0'}  # 벅스와 달리 멜론에서 설정해야 하는 헤더값
    class_name = []
    title_list = []
    artist_list = []
    dict = {}
    df = None

    def set_url(self, detail):
        self.url = requests.get(f'{self.url}{detail}', headers=self.headers).text

    def get_ranking(self):
        soup = BeautifulSoup(self.url, 'lxml')
        t_list = soup.find_all(name='div', attrs={"class":self.class_name[0]})
        for idx, title in enumerate(t_list):
            #print(f'{idx + 1}위 {title.find("a").text}')  # idx는 0 부터 시작함.
            self.title_list.append(title.find("a").text)

        print("=" * 100)
        a_list = soup.find_all(name='div', attrs={"class":self.class_name[1]})
        for artist in a_list:
            # print(f'{artist.find("a").text}')
            self.artist_list.append(artist.find("a").text)

    def make_dict(self):
        for idx, title in enumerate(self.title_list):
            self.dict[title] = self.artist_list[idx]
        print(self.dict)

    def dict_to_dataframe(self):
        dt = self.dict
        self.df = pd.DataFrame.from_dict(dt, orient='index')

    def df_to_csv(self):
        path = './data/melon.csv'
        self.df.to_csv(path, sep=',', na_rep='NaN', encoding='utf-8-sig')

    @staticmethod
    def main():
        melon = Melon()
        melon.set_url('dayTime=2021060515')
        melon.class_name = ["ellipsis rank01", "ellipsis rank02"]
        melon.get_ranking()
        melon.make_dict()
        melon.dict_to_dataframe()
        melon.df_to_csv()


Melon.main()
