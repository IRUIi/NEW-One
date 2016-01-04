#coding:utf-8
import urllib
import MySQLdb

def getHtml(url):
    # ��ȡ��ҳ����
    page = urllib.urlopen(url)
    html = page.read()
    return html
def content(html): 
    str = '<article class="article-content">'# ������Ҫ�õ��������������Ŀ¼��ǩ�µ�
    content = html.partition(str)[2]# partition() �����������ָ���ķָ����ַ���зָ���ȡ����е����һ��
    str1= '<div class="article-social">'
    content = content.partition(str1)[0]# ��contentĿ¼��ȡ��һ�Σ���ֵ;����ȡ����str����ļ���str1ǰ�������
    return content
def title(content,beg=0):
    # ���title��ץȡ������str.index()��������е���Ƭ������
    try:
        title_list=[]
        while True:
            num1 = content.index('��',beg)+3 # ��ͷ
            num2 = content.index('</p>',num1) # ��β
            title_list.append(content[num1:num2])# ȡ��num1��ͷ��num2��β��һ����Ϣ
            beg = num2# �µĿ�ͷ������һ�εĽ�β
    except ValueError:
            return title_list
def get_img(content,beg=0):
    # ƥ��ͼƬ��url,��������str.index()��������Ƭ
    try:
        img_list=[]
        while True:
            scr1 = content.index('http',beg) # ��ͷ
            scr2 = content.index('/></p>',scr1) # ��β
            img_list.append(content[scr1:scr2])
            beg = scr2
    except ValueError:
            return img_list
        
def many_img(data,beg = 0):
    # ����ƥ���ͼ��url
    try:
        many_img_str = ''
        while True:
            scr1 = data.index('http',beg)
            scr2 = data.index('/><br /> <img scr=',scr1)
            many_img_str += data[scr1:scr2]+'|'  # ͼƬ֮���÷�Ÿ���
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
def data_out1(title,img):
    for size in range(0, len(title)):  
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306)
            cur=conn.cursor()
            cur.execute('insert into qwe(title,img) values(%s,%s)', (title[size],img[size]))
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
          
     # conn = MySQLdb.connect(host='127.0.0.1', user='root',
      #              passwd='123456', db='mysql', port = 3306, charset = 'utf8')
      #      cur = conn.cursor()
       #     cur.execute('insert into qwe(title,img) values(%s,%s)', (title[size],img[size]))
           
      #      cur.close()
      #      conn.close()   
def main_content(html):#�µķ�����������ȡ�뿴����������
# ��ҳ���ݷָ�ı�ǩ,�����ָ���ҳ
    str = '<div class="content">'
    content = html.partition(str)[2]
    str1 = '</div>'
    content = content.partition(str1)[0]
    return content # �õ���ҳ������   

def page_url(content, order = 20, beg = 0):# ����һ������order��Ĭ��Ϊ20����Ϊÿҳ20�ڡ���ҳ��
    try:
        url = []
        i = 0
        while i < order:# һҳ���ڣ�ֱ����ȡ����������һҳ
            url1 = content.index('<h2><a href="',beg)+13
            url2 = content.index('" ',url1)#��u11��ͷ�ģ�����β��
            url.append(content[url1:url2])
            beg = url2
            i = i + 1
        return url
    except ValueError:
        return url   
def get_order(num):
# num����ȡ����Ŀ���������Ըı䣬�����뿴���ڣ�һ�ھ���һ��
    url_list = []
    page = num / 20 # ÿһҳ��20��
    order = num % 20 # ����һ��ҳ����Ŀ
    if num < 20:  # ����ȡ����Ŀ��������20��һҳ20������ֱ����ȡ��һҳ��num��
        url = 'http://bohaishibei.com/post/category/main'
        main_html = getHtml(url)
        clean_content = main_content(main_html)  # ����ҳ���õ���ҳ��Ϣ        
        url_list = url_list + page_url(clean_content, num)  #���뵽url_list�У���Ϊ����20�ڣ�����order��Ҫ�仯��������Ҫ������
    for i in range(1, page+1): 
        url = 'http://bohaishibei.com/post/category/main/page/%d' % i # ��ȡ��ҳ����Ŀ��%i��%d��ֵһֱ�������һҳ��
        main_html = getHtml(url)
        clean_content = main_content(main_html)
        url_list = url_list + page_url(clean_content) #��ȡ��ҳ�����뵽url_list��
      
        if (i == page)&(order > 0):  # �������һҳ������г���һҳ����Ŀ�������order��
            url = 'http://bohaishibei.com/post/category/main/page/%d' % (i+1) #ʣ�µ���һҳ����
            main_html = getHtml(url)
            clean_content = main_content(main_html)         
            url_list = url_list + page_url(clean_content, order)            
    return url_list
order = get_order(30) # get_order�������ܲ���ץȡ�����ڵ���ݣ�return��url_list
for i in order:  # �����б�ķ���
    html = getHtml(i)   #getHtml(url_list)         
    content_data = content(html)
    title_data = title(content_data)
    img_data = get_img(content_data)
    data_out(title_data, img_data) 
    data_out1(title_data, img_data)    