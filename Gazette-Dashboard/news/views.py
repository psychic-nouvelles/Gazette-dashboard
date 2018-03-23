from django.shortcuts import render
import urllib.request
from urllib.error import URLError, HTTPError
import urllib.parse


def manageNews(request):

    return render(request, 'news/manageNews.html')

def addNews(request):
    nextPage = ""
    return render(request, 'news/addNews.html', {'nextPage': nextPage})


from newspaper import Article
import nltk
import datetime, dateutil.parser

def getNews(request):

    url = request.POST.get('articleURL')
    if url is None:
        url = request.GET.get('url')
    print(url)
    article = Article(url)
    article.download()
    articleHTML = article.article_html
    article.parse()
    authors = article.authors
    publishDate = article.publish_date
    articleText = article.text
    articleTitle = article.title
    articleImage = article.top_image
    OGData = article.meta_data['og']
    article.nlp()
    articleKeywords = article.keywords
    articleSummary = article.summary
    date = OGData.get('updated_time')
    parsedDate = ""
    if date is not None:
        d = dateutil.parser.parse(date)
        parsedDate = d.strftime('%d/%m/%Y %I:%M:%S')
        print(date, parsedDate, "<-- TIME")

    print(authors, publishDate, articleText, articleImage, articleKeywords, articleSummary, "<-- DATA", articleTitle, OGData)

    return render(request, 'news/addNews.html', {'authors': authors, 'publishDate': publishDate,
                                                    'articleText': articleText, 'articleImage': articleImage,
                                                    'articleKeywords': articleKeywords,
                                                    'articleSummary': articleSummary.strip(),
                                                    'articleTitle': articleTitle.strip(), 'OGData': OGData,
                                                    'articleHTML': articleHTML, 'parsedDate': parsedDate,
                                                    'requestURL': url})

import feedparser
import urllib.parse as urlparse
def newsSearch(request):
    newsSource = request.POST.get('newsSource')
    print(newsSource)
    if newsSource == 'googleNews':
        print('News')
        searchQuery = request.POST.get('searchQuery')
        searchString = searchQuery.replace(' ', '%20')
        print(searchString, "Search Query")
        rssURL = 'https://news.google.com/news/rss/search/section/q/' + searchString + '/' + searchString + '?hl=en-IN&gl=IN&ned=in'
        xmlResponse = feedparser.parse(rssURL)
        responseEntries = xmlResponse['entries']
        print(searchQuery, rssURL)
        responseDict = []
        for key in responseEntries:
            updated = ''
            author = ''
            responseDict.append({'id': key.link, 'title': key.title, 'link': key.link, 'published': key.published_parsed,
                                 'updated': updated, 'content': key.description, 'author': author,
                                 'category': key.category})


        return render(request, 'news/manageNews.html', {'searchQuery': searchQuery, 'xmlResponse': xmlResponse,
                                                        'responseEntries': responseEntries,
                                                        'responseDict': responseDict, 'news': True})
    else:
        print('Alerts')
        searchQuery = request.POST.get('searchQuery')
        rssURL = 'https://www.google.co.in/alerts/feeds/13344073460838789859/1399775576898670551'
        xmlResponse = feedparser.parse(rssURL)
        responseEntries = xmlResponse['entries']
        # print(rssURL, xmlResponse)
        responseDict = []
        for key in responseEntries:
            link = key.link
            parsed = urlparse.urlparse(link)
            parsedLink = urlparse.parse_qs(parsed.query)['url']
            parsedLinkString = parsedLink[0]
            contentValue = key.content[0]['value']
            print(parsedLinkString, contentValue)

            responseDict.append({'id': key.id, 'title': key.title, 'link': parsedLinkString, 'published': key.published,
                                 'updated': key.updated, 'content': contentValue, 'author': key.author})  # content = key.content

        # print(responseDict)

        return render(request, 'news/manageNews.html', {'xmlResponse': xmlResponse, 'searchQuery': searchQuery,
                                                        'responseEntries': responseEntries,
                                                        'responseDict': responseDict, 'news': False})