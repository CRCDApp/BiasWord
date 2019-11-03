import datetime

import requests
from lxml import html
from newspaper import Article

""" Class Description:
    This class is for crawling articles from TheGuardians newspaper website 
"""


def crawl_articles(url, visited_urls):
    """Crawling Articles from article, avoiding to crawl already visited articles

    Parameters:
    url: URL of a page containing articles
    visited_urls: List of already visited urls

    Returns:
    article_texts: List of article text
    visited_urls: updated list of visited_urls
   """
    article_texts = []
    page = requests.get(url)
    webpage = html.fromstring(page.content)
    # Searching for all links within current page
    valuable_articles = webpage.xpath('//a/@href')

    for new_url in valuable_articles:
        # Checking if url is valid and is not already visited
        if (new_url.find(url[:len(url) - 4]) < 0) or (new_url in visited_urls):
            continue

        # getting the new article
        article = Article(new_url)
        try:
            article.download()
            article.parse()
        except:
            continue
        # Addin article text to our texts and also adding url to visited urls
        article_texts.append(article.text)
        visited_urls.append(new_url)

    return article_texts, visited_urls


def save_articles(articles, urls, category='category', path='.'):
    """saving articles and urls into file, using datetime as postfix in the file name

    Parameters:
    articles: list of article texts
    url: list of urls of the respective article
    category: part of the name of the file to find easier

    Returns:
    string: path to the articles file
   """
    time = datetime.datetime.now()
    with open('%s/Guardians-%s_%s_Articles_%s_%s_%s.txt' % (
            path, category, str(len(articles)), str(time.date()), str(time.hour), str(time.minute)), 'w') as f:
        for item in articles:
            f.write("%s\n" % item)

    with open('%s/Links_Guardians-%s_%s_Articles_%s_%s_%s.txt' % (
            path, category, str(len(articles)), str(time.date()), str(time.hour), str(time.minute)), 'w') as f:
        for item in urls:
            f.write("%s\n" % item)

    return '%s/Guardians-%s_%s_Articles_%s_%s_%s.txt' % (
        path, category, str(len(articles)), str(time.date()), str(time.hour), str(time.minute))


def generate_links():
    """Generate links of articles of Guardians website from 2017 to 2019

    Returns:
    List of URLs
   """
    day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
           '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    month = ['dec', 'nov', 'oct', 'sep', 'aug', 'jul', 'jun', 'may', 'apr', 'mar', 'feb', 'jan']
    year = ['2019', '2018', '2017']
    category = ['world', 'commentisfree', 'environment', 'artanddesign', 'lifeandstyle', 'sport']
    return ["https://www.theguardian.com/%s/%s/%s/%s/all" % (c, y, m, x) for c in category for y in year for m in month
            for x in day]


def create_guardians_dataset(articleCount=200, path='./', category='world'):
    """ Creating a dataset of Articles from Guardians website

    Parameters:
    articleCount: Number of articles needs to be crawled
    path: path to save output dataset
    category: part of the name of the output dataset file to find easier

    Returns:
    string: path to the articles file
   """
    articles = []
    urls = []
    links = generate_links()
    for link in links:
        # checking if the number of articles is enough
        if (len(urls) > articleCount):
            break
        new_response, urls = crawl_articles(link, urls)
        articles = articles + new_response
    return save_articles(articles, urls, category, path)
