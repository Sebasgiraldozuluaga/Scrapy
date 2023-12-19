import requests
import lxml.html as html
import  os
import datetime

HOME_RUN = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
XPATH_TITLE = '//h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_CUERPO ='//div[@class="html-content"]/p/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code ==200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            #print(notice)
            try:
                title =parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                title = title.replace('?', '')
                title = title.replace('\n', '')
                title = title.replace('\t', '')
                title = title.replace('#', '')
                title = title.replace('|', '')
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_CUERPO)
            except IndexError:
                print("error")
                return
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                print(title)
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_RUN)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                #print(links_to_notices)
                print(link)
                parse_notice(link, today)
        else:
            raise ValueError (f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ =='__main__':
    run()