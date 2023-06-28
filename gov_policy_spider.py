# coding utf-8
"""
作者：Hester
日期：2023/6/28
"""
import requests
from requests.exceptions import RequestException
import json
from lxml import etree
from fake_useragent import UserAgent
import datetime


def get_onepage(url,headers):
    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            print('网页获取成功')
            return response.json()
        else:
            print('网页获取失败')

    except RequestException:
        return 'requests出现异常错误'


#根据json文件结构提取信息
def parse_page(json,headers,start_time,end_time):
    if json:
        policy_list = json.get('articles')
        results=[]
        for policy in policy_list:
            # 获取发布日期并进行比较
            date = policy['created_at']
            date= datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            if start_time<=date<=end_time:
                #获取索引号，发布机构，政策标题
                index = policy['identifier_f']
                agency = policy['publisher']
                title = policy['title']
                date=policy['created_at']
                # 访问政策详情页
                policy_url = policy['url']
                policy_response = requests.get(policy_url,headers=headers)
                policy_html_content = policy_response.content
                # 创建lxml解析器对象
                parser = etree.HTMLParser()
                # 使用lxml解析器解析政策详情页内容
                policy_tree = etree.fromstring(policy_html_content, parser=parser)
                # 获取政策正文文本和附件链接
                article_content = policy_tree.xpath('//div[@class="article-content"]')[0]
                content = article_content.xpath('.//text()')
                content = [c.strip() for c in content if c.strip()]
                attachment_link = policy_tree.xpath('//div[@class="article-content"]/p/a/@href')

                # 将政策信息添加到结果列表中
                result = {
                    '索引号': index,
                    '发布机构': agency,
                    '发布日期': date,
                    '政策标题': title,
                    '政策正文文本': content,
                    '政策正文附件链接': attachment_link
                }
                results.append(result)
        return results

def write_txt(results):
     # 遍历结果列表
     for result in results:
         # 获取政策标题作为文件名
         filename = result['政策标题'] + ".txt"
         # 打开一个txt文件，使用写模式
         with open(filename, 'w', encoding='utf-8') as file:
             # 写入索引号
             file.write("索引号: " + result['索引号'] + '\n')
             # 写入发布机构
             file.write("发布机构: " + result['发布机构'] + '\n')
             # 写入发布日期
             file.write("发布日期: " + result['发布日期'] + '\n')
             # 写入政策标题
             file.write("政策标题: " + result['政策标题'] + '\n')
             # 写入政策正文文本
             file.write("政策正文文本: \n")
             for line in result['政策正文文本']:
                 file.write(line + '\n')
             # 写入政策正文附件链接
             file.write("政策正文附件链接: " + str(result['政策正文附件链接']) + '\n')



if __name__ =='__main__':
    # 输入
    date_range = input("请输入日期范围（格式：YYYYMMDD-YYYYMMDD）：")
    start_date_str, end_date_str = date_range.split('-')
    start_date = datetime.datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y%m%d")
    for i in range(1,50):
        headers = {
            'User-Agent': UserAgent().random,
            'cookie': 'Path=/; _trs_uv=li9vxzk2_122_biit; Path=/; gkmlfront_session=eyJpdiI6IjBYUTY2dVwvbTlhT3pGQ01SN1pEWnpnPT0iLCJ2YWx1ZSI6Im8zS2lsV2hyRDYzUnRNaEIyb2p5VGxLZlRiNCtYUlUyUXRCQ2VmeVVzU0Q0VVFnMWJ0SjE5bGxDaVJFTkJmcHAiLCJtYWMiOiJkZGMxMGViY2NkOGYyM2JmMGE2M2MzNjZlODEwMDkxY2VkMDFjMTA0N2U2ZTU3NWZiYzFjNjhhNzcwM2RlMDUwIn0%3D; front_uc_session=eyJpdiI6Ikpud1wveDBNTTY5VHZHdFc4NzdGdkl3PT0iLCJ2YWx1ZSI6IkI3dndVZW5MWGxyaFhOdzdibDdTYjdwMUc2Um9FRENsWndvdVBzZ0xwakxzRGhWQVpOUkFuRmh3MXRFOXpBUUYiLCJtYWMiOiIwN2IwMDRmZDM3NDRhOWNjMmJhYWQzM2Y3YWQxNGFjNTRiNGJkM2VlMDQ5ZDEyOGUxZWE1OTk1NjU2ZDEyMjgzIn0%3D',
            'X-Requested-With': 'XMLHttpRequest'
        }
        base_url = f'https://www.gd.gov.cn/gkmlpt/api/all/5?page={i}&sid=2'
        p_json = get_onepage(base_url, headers)
        if not p_json:
            break
        results = parse_page(p_json, headers, start_date, end_date)
        if not results:
            break
        write_txt(results)


