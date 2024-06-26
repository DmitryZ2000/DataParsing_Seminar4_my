import scrapy
from scrapy.http import HtmlResponse
from items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://volgograd.hh.ru/search/vacancy?ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&text=Python&enable_snippets=false&L_save_area=true"]

    def parse(self, response: HtmlResponse):
# Проверка наличия перехода на следующую страницу            
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//span/a[@target='_blank']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@data-qa='vacancy-title']/text()").get()
        url = response.url
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        yield JobparserItem(name=name, salary=salary, url=url)


        