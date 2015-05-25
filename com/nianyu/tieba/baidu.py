# -*- coding: utf-8 -*-

import urllib2
import urllib
import sys
import json
import re
import cookielib

# name = "840311035@qq.com"
name="小仙吧"
password = "909295"

### preparing for the post data
def get_url_response(url, post_dict={}, header_dict={}, timeout=0, useGzip=False):
    url = str(url)

    # 添加post数据
    if (post_dict):
        post_data = urllib.urlencode(post_dict)
        request = urllib2.Request(url, post_data)
        request.add_header('Conntent-Type', 'application/x-www-form-urlencode')
    else:
        request = urllib2.Request(url)

    #添加头信息
    if (header_dict):
        for key in header_dict:
            request.add_header(key, header_dict[key])

    default_header_dict = {
        'User-Agent'    : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Cache-Control' : 'no-cache',
        'Accept'        : '*/*',
        'Connection'    : 'keep-Alive'
        }
    for key in default_header_dict:
        request.add_header(key, default_header_dict[key])

    # 设置编码
    if (useGzip):
        request.add_header('Accept-Encoding', 'gzip, deflate')

    # 设置时间间隔
    if timeout > 0:
        response = urllib2.urlopen(request, timeout = timeout)
    else:
        response = urllib2.urlopen(request)

    return response
###################################################################

def get_cookie():

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    cookie_url = 'http://www.baidu.com/'
    cookie = get_url_response(cookie_url)

    for index, cookie in enumerate(cj):
        print '[%d]'%index, cookie
    return cj

###################################################################


def get_token():

    token_url = 'https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true'
    token = get_url_response(token_url)
    token_html = token.read()


    token_position = re.search("bdPass\.api\.params\.login_token='(?P<tokenval>\w+)';", token_html)
    if (token_position):
        token_value = token_position.group('tokenval')
        print 'token: ', token_value
        return token_value
    else:
        print 'Failed to get token.'
        sys.exit()

#####################################################################
def login_baidu(cj,token):

    login_url = 'https://passport.baidu.com/v2/api/?login'
    staticpage = "http://www.baidu.com/cache/user/html/jump.html"
    postdict = {
        'charset'   : 'utf-8',
        'token'     : token,
        'isPhone'   : False,
        'username'  : name,
        'password'  : password,
        'tpl'       : 'mn',
        'callback'  : "parent.bdPass.api.login._postCallback",
        'loginType' : "1",
        'index'     : "0",
        "staticpage":"http://tieba.baidu.com/tb/v2Jump.html"
        }
    login = get_url_response(login_url, postdict)
    cj_cookie = []
    n = 0
    for cookie in cj:
        cj_cookie.append(cookie.name)
        print cookie.name
    cookie_check = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
    for i in range(len(cookie_check)):
        if cookie_check[i] in cj_cookie:
            n += 1
    if n==4:
        print "Welcome! sign in baidu successfully!"
    else:
        print "Sorry! Failed to sign in."
        sys.exit()
#################################################################

def get_tbs():
    tbs_url='http://tieba.baidu.com/dc/common/tbs'
    tbs_resp=urllib2.urlopen(tbs_url).read()
    print tbs_resp
    tbs=re.search('"tbs":"(?P<tbs>.*?)"',tbs_resp).group('tbs')
    print 'tbs:',tbs
    return tbs

def get_tieba_list():
    url = 'http://tieba.baidu.com/f/like/mylike?pn='
    page = 1
    a=r'title="(.+?)">\1</a></td>'
    a=re.compile(a)
    result = []
    while(1):
        sign_url = url + str(page)
        html = urllib2.urlopen(sign_url).read().decode('GBK')

        result += re.findall(a,html)
        if(html.find(u'下一页') == -1):
            break
        page += 1
    return result

def sign_tieba(bars):
    sign_url='http://tieba.baidu.com/sign/add'
    tbs = get_tbs()
    for bar in bars:
        name = bar.encode("utf-8")
        print "%s吧 正在尝试签到..." % name
        sign_request={'ie':'utf-8','kw':name,'tbs':tbs}
        sign_request=urllib.urlencode(sign_request)
        sign_request=urllib2.Request(sign_url,sign_request)
        sign_resp=urllib2.urlopen(sign_request)
        sign_resp=json.load(sign_resp)

        if sign_resp['error']=='' :
            user_sign_rank = int(sign_resp['data']['uinfo']['user_sign_rank']) #第几个签到
            cont_sign_num = int(sign_resp['data']['uinfo']['cont_sign_num'])   #连续签到
            cout_total_sing_num = int(sign_resp['data']['uinfo']['cout_total_sing_num'])#累计签到
            print "签到成功,第%d个签到,连续签到%d天,累计签到%d天" %(user_sign_rank, cont_sign_num, cout_total_sing_num)
        else :#签到失败处理
            if not sign_resp['error']==u'亲，你之前已经签过了':
                print "签到失败，原因未知"
            else:
                print '亲，%s 你之前已经签过了' % name

cj = get_cookie()
token = get_token()

login_baidu(cj, token)
bars=get_tieba_list()
if not bars is None:
    sign_tieba(bars)




