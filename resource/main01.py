import requests
from lxml import etree

# 需求：爬取电影天堂2019新片精品，网址：https://www.dytt8.net/


BASE_URL = "https://dytt8.net"
url = "https://dytt8.net/html/gndy/dyzz/list_23_1.html"
headers = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
response = requests.get(url,headers)
# response.text
# response.content
# requests库，默认会使用自己猜测的编码方式将爬取下来的网页进行解码，然后存储到text属性上去
# 在电影天堂的网页中，因为编码方式，requests库猜错了，所以使用requests.text会产生乱码问题
# 此时就需要使用requests.content方法手动指定解码方式,此处，电影天堂使用的是gbk编码方式，所以要使用gbk解码
# print(response.content.decode("gbk"))
text = response.content.decode("gbk")
html = etree.HTML(text)
detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
for detail_url in detail_urls:
    print(BASE_URL+detail_url)


