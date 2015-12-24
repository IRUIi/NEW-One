#coding:utf-8
import urllib

def getHtml(url):
    # 获取网页内容
    page = urllib.urlopen(url)
    html = page.read()
    return html
def content(html): 
    str = '<article class="article-content">'# 我们想要得到的内容是在这个目录标签下的
    content = html.partition(str)[2]# partition() 方法用来根据指定的分隔符将字符串进行分割。这里，区三段中的最后一段
    str1= '<div class="article-social">'# 功能行为
    content = content.partition(str1)[0]# 在content目录中取第一段，赋值;就是取得是str后面的加上str1前面的内容
    return content
def title(content,beg=0):
    # 完成title的抓取，利用str.index()函数和序列的切片方法。
    try:
        title_list=[]
        while True:
            num1 = content.index('】',beg)+3 # 开头
            num2 = content.index('</p>',num1) # 结尾
            title_list.append(content[num1:num2])# 取以num1开头，num2结尾的一段信息
            beg = num2# 新的开头，即上一段的结尾
    except ValueError:
            return title_list
def get_img(content,beg=0):
    # 匹配图片的url,还是运用str.index()和序列切片
    try:
        img_list=[]
        while True:
            scr1 = content.index('http',beg) # 开头
            scr2 = content.index('/></p>',scr1) # 结尾
            img_list.append(content[scr1:scr2])
            beg = scr2
    except ValueError:
            return img_list
        
def many_img(data,beg = 0):
    # 用于匹配多图的url
    try:
        many_img_str = ''
        while True:
            scr1 = data.index('http',beg)
            scr2 = data.index('/><br /> <img scr=',scr1)
            many_img_str += data[scr1:scr2]+'|'  # 图片之间用符号隔开
            beg = scr2
    except ValueError:
        return many_img_str  
def data_out(title, img):
    # 写入文本
    with open(r"C:\Users\Administrator\Desktop\aab.txt", "a+") as fo:# a+模式，不存在建立，有的话追加末尾
        fo.write('\n')
        for size in range(0, len(title)):
            # 判断img[size]中存在的是不是一个url，即判断是不是有很多图
            if len(img[size]) > 70: 
                img[size] = many_img(img[size])# 多图，调用many_img()方法
            fo.write(title[size]+'$'+img[size]+'\n')# 将标题和图的
        
def main_content(html):
# 首页内容分割的标签,用来分割首页
    str = '<div class="content">'
    content = html.partition(str)[2]
    str1 = '</div>'
    content = content.partition(str1)[0]
    return content # 得到网页的内容   

def page_url(content, order = 20, beg = 0):# 新增一个参数order，默认为20
    try:
        url = []
        i = 0
        while i < order:
            url1 = content.index('<h2><a href="',beg)+13
            url2 = content.index('" ',url1)
            url.append(content[url1:url2])
            beg = url2
            i = i + 1
        return url
    except ValueError:
        return url   
def get_order(num):
# num代表获取的条目数量
    url_list = []
    page = num / 20 # 每一页有20条
    order = num % 20 # 超出一整页的条目
    if num < 20:  # 如果获取的条目数量少于20（一页20个），直接爬取第一页的num条
        url = 'http://bohaishibei.com/post/category/main'
        main_html = getHtml(url)
        clean_content = main_content(main_html)         
        url_list = url_list + page_url(clean_content, num)  
    for i in range(1, page+1): # 需这里需要尾巴
        url = 'http://bohaishibei.com/post/category/main/page/%d' % i # 爬取整页的条目
        main_html = getHtml(url)
        clean_content = main_content(main_html)
        url_list = url_list + page_url(clean_content) #获取整夜
      
        if (i == page)&(order > 0):  # 爬到最后一页，如果有超出一页的条目则继续爬order条
            url = 'http://bohaishibei.com/post/category/main/page/%d' % (i+1) 
            main_html = getHtml(url)
            clean_content = main_content(main_html)         
            url_list = url_list + page_url(clean_content, order)            
            #print len(page_url(clean_content, order))
    return url_list
order = get_order(30) # get_order方法接受参数，抓取多少期的数据
for i in order:  # 遍历列表的方法
    html = getHtml(i)            
    content_data = content(html)
    title_data = title(content_data)
    img_data = get_img(content_data)
    data_out(title_data, img_data)                      
