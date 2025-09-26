# Query the web

import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

class WebQuery:
    def __init__(self):
        self.key = os.getenv("BOCHA_API_KEY")
        self.use_web = os.getenv("USE_WEB", "false").lower() == "true"

    def query(self, query: str, key: str = None) -> str:
        if key is None:
            key = self.key
        if not self.use_web:
            return []
        print(f'Search for query in web: {query}')
        url = "https://api.bochaai.com/v1/web-search"

        payload = json.dumps({
        "query": query,
        "count": 10,
        "summary": True,
        })

        headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        web_pages = response.json().get('data', {}).get('webPages', {}).get('value', [])

        top_results = []
        for page in web_pages:

            result = {
                'title': page.get('name'),
                'source': page.get('url'),
                'date': page.get('dateLastCrawled'),
                'siteName': page.get('siteName'),
                'logo': page.get('siteIcon'),
                'summary': page.get('summary'),
                'snippet': page.get('snippet')
            }
            top_results.append(result)
            
        web_articles = [
            {
                'text': web.get('summary', ''),
                'metadata': {
                'title': web.get('title', '无标题'),
                'date': web.get('date', '未知日期'),
                'source': web.get('source', ''),
                'siteName': web.get('siteName', ''),
                }
            }
            for web in top_results
        ]
        return web_articles
    

if __name__ == "__main__":
    web_query = WebQuery()
    query = "查理·芒格"
    results = web_query.query(query)
    print(len(results), 'articles')
    print(results)