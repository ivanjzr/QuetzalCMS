import urllib2
import ast



def loadJSONResults(url_page):
    try:
        url = url_page
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        page_result = response.read()
        r = ast.literal_eval(page_result)
        return page_result


    except Exception as e:
        return dict(r=str(e))