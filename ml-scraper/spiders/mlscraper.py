import random
import scrapy
import pymysql
from pymysql.err import OperationalError, ProgrammingError


USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 Edg/113.0.1774.35",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:113.0) Gecko/20100101 Firefox/113.0 Edg/113.0.1774.35",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36 OPR/90.0.4480.84",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0 OPR/77.0.4054.172",
        "Mozilla/5.0 (Linux; Android 11; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:113.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:113.0) Gecko/20100101 Firefox/113.0"
    ]

class MlScraperSpider(scrapy.Spider):
    name = 'mlscraper'

    # Database Parameters
    db_params = {
        'user': 'myuser',
        'password': 'mypassword',
        'host': 'localhost',
        'port': 3306,
        'database': 'mydatabase'
    }
    
    def create_DDL_statement(self):
        return f'''
        CREATE TABLE IF NOT EXISTS {self.s.replace('-', '_')} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            price VARCHAR(50),
            link TEXT
        );
        '''

    # Initialize database connection and cursor
    def create_table(self):
        table_statement = self.create_DDL_statement()
        try:
            self.conn = pymysql.connect(**self.db_params)
            self.cur = self.conn.cursor()
            self.cur.execute(table_statement)
            self.conn.commit()
            print(f"Table '{self.s.replace('-', '_')}' is ready.")
        except OperationalError as e:
            print(f"Operational error occurred: {e}")
        except ProgrammingError as e:
            print(f"Programming error occurred: {e}")

    def start_requests(self):
        self.create_table()
        url = f'https://lista.mercadolivre.com.br/{self.s}'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        for i in response.xpath('/html/body/main/div/div[3]/section/ol'):
            titles = i.xpath('.//h2[contains(@class, "ui-search-item__title")]/text()').getall()
        
            # Extract the price
            prices = i.xpath('.//div[contains(@class, "ui-search-result__content")]'
                            '//div[contains(@class, "ui-search-item__group ui-search-item__group--price")]'
                            '//div[contains(@class, "ui-search-item__group__element")]'
                            '//div[contains(@class, "ui-search-price ui-search-price--size-medium")]'
                            '//div[contains(@class, "ui-search-price__second-line")]'
                            '//span[contains(@class, "andes-money-amount__fraction")]/text()').getall()            
            # Extract the link
            links = i.xpath('.//a[contains(@class, "ui-search-item__group__element")]/@href').getall()
        
            print(prices, len(prices), 'THE PRICES')
            print(len(titles))
            print(len(links))


            for title, price, link in zip(titles, prices, links):
                self.insert_data(title, f'R$ {price}', link)

        next_page1 = response.xpath('//a[contains(@title,"Próxima")]/@href').get()
        next_page2 = response.xpath("//a[contains(@title, 'Seguinte')]/@href").get()
        
        if next_page1:
            yield self.make_request(next_page1)
        elif next_page2:
            yield self.make_request(next_page2)
            

    def make_request(self, url):
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        return scrapy.Request(url, callback=self.parse, headers=headers)


    def insert_data(self, title, price, link):
        insert_query = f'''
        INSERT INTO {self.s.replace('-', '_')} (title, price, link)
        VALUES (%s, %s, %s)
        '''
        try:
            self.cur.execute(insert_query, (title, price, link))
            self.conn.commit()
        except OperationalError as e:
            print(f"Operational error occurred during insert: {e}")
        except ProgrammingError as e:
            print(f"Programming error occurred during insert: {e}")