#from webbot import Browser
import csv
import requests
import re

def main():

    #with open('urls.csv') as csv_file:
    with open('urls.csv') as csv_file:
        urls_file = csv.reader(csv_file, delimiter=',')
        with open('result.csv', mode='w') as result_file:
            result_writer = csv.writer(
                result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in urls_file:
                #print(f'URL is {row[0]}')
                site_status = 0
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                try:
                    r = requests.head(f'{row[0]}', headers=headers)
                    site_status = r.status_code
                except requests.ConnectionError:
                    result_writer.writerow([f'{row[0]}', 'failed to connect'])
                if site_status is 200:
                    s = r'(?<=</span>&nbsp;<span>)(.*GMT.)+(?=<\/span>)'
                    r = requests.get(f'{row[0]}', headers=headers)
                    result = re.search(s, r.text)
                    print (result.group(1))
                    #web = Browser(showWindow=False)
                    #web.go_to(f'{row[0]}')
                    #result = web.find_elements(id='google-cache-hdr', classname='', number=1, css_selector='', xpath='', loose_match=True)
                    #print(web.get_page_source())
                    #web.driver.quit()
                    result_writer.writerow([f'{row[0]}', result.group(1)])
                else:
                    result_writer.writerow([f'{row[0]}', site_status])


if __name__ == '__main__':
    main()
