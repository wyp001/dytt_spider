import requests
from lxml import etree

# 需求：爬取电影天堂2019新片精品，网址：https://www.dytt8.net/

BASE_DOMAIN = "https://dytt8.net"
HEADERS = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
url = "https://dytt8.net/html/gndy/dyzz/list_23_1.html"

# 获取详情页面的url
def get_detail_urls(url):
    response = requests.get(url,HEADERS)
    # response.text
    # response.content
    # requests库，默认会使用自己猜测的编码方式将爬取下来的网页进行解码，然后存储到text属性上去
    # 在电影天堂的网页中，因为编码方式，requests库猜错了，所以使用requests.text会产生乱码问题
    # 此时就需要使用requests.content方法手动指定解码方式,此处，电影天堂使用的是gbk编码方式，所以要使用gbk解码
    # print(response.encoding) # 打印requests库的默认编码方式
    # print(response.content.decode("gbk"))

    # 由于后面爬取时response.content.decode("gbk")各边页面有问题，因此可以使用text先解码，提取出需要的内容后再进行相应编码格式的解码
    text = response.text
    html = etree.HTML(text)
    detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
    # lambda url:BASE_URL+url,detail_urls 将detail_urls列表中的每一项前面都拼接上BASE_URL等价于下面的代码：
    # def abc(url):
    #     return BASE_URL + url
    # index = 0
    # for detail_url in detail_urls:
    #     detail_url = abc(detail_url)
    #     detail_urls[index] = detail_url
    #     index += 1
    detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return detail_urls

# 解析详情页面
def parse_detail_page(url):
    movie = {} # 定义一个电影的字典
    response = requests.get(url,headers=HEADERS)
    text = response.content.decode("gbk")
    html = etree.HTML(text)
    title = html.xpath('//div[@class="title_all"]//font[@color="#07519a"]/text()')[0]
    movie['title'] = title # 将title的属性放到movie的字典中

    zoomE = html.xpath('//div[@id="Zoom"]')[0]
    images = zoomE.xpath('.//img/@src')
    cover = images[0]   # 电影封面
    screenshort = images[1] # 电影截屏
    movie['cover'] = cover
    movie['screenshort'] = screenshort

    infos = zoomE.xpath('.//text()')
    for index,info in enumerate(infos):
        # startswith("") 以xxx开始
        if info.startswith("◎年　　代"):
            # strip()  去除前面的空格
            info = info.replace("◎年　　代","").strip()
            movie["time"] = info
        elif info.startswith("◎产　　地"):
            info = info.replace("◎产　　地","").strip()
            movie["country"] = info
        elif info.startswith("◎豆瓣评分"):
            info = info.replace("◎豆瓣评分","").strip()
            movie["rating"] = info
        elif info.startswith("◎类　　别"):
            info = info.replace("◎类　　别","").strip()
            movie["type"] = info
        elif info.startswith("◎片　　长"):
            info = info.replace("◎片　　长","").strip()
            movie["duration"] = info
        elif info.startswith("◎主　　演"):
            info = info.replace("◎主　　演","").strip()
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎标　　签"):
                    break
                actors.append(actor)
            movie["actors"] = actors
        elif info.startswith("◎简　　介"):
            info = info.replace("◎简　　介","").strip()
            for x in range(index+1,len(infos)):
                profile = infos[x].strip()
                if profile.startswith("【下载地址】"):
                    break
                movie["profile"] = profile
    return movie

def spider():
    # 原本的url为：https://dytt8.net/html/gndy/dyzz/list_23_1.html
    # 次数的{}先占为，后面替换
    base_url = "https://dytt8.net/html/gndy/dyzz/list_23_{}.html"
    movies = []
    # 获取1-7页的内容
    for x in range(1,8): # 第一个for循环控制总共要获取7页电影列表
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:  # 第二个for循环是用来获取每一页中所有电影的详情url
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)


if __name__ == '__main__':
    spider()


