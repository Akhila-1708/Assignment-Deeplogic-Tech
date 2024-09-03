import http.server
import socketserver
import requests


def fetch_html():
    url = "https://time.com"
    response = requests.get(url)
    return response.text

def extract_stories(html):
   
    stories = []
    start_tag = '<h3 class="latest-stories__item-headline">'
    link_tag = '<a href="'
    for _ in range(6):  
        start_idx = html.find(start_tag)
        if start_idx == -1:
            break
        html = html[start_idx + len(start_tag):]
        title_start = html.find('>') + 1
        title_end = html.find('</a>')
        title = html[title_start:title_end].strip()

        link_start = html.find(link_tag) + len(link_tag)
        link_end = html.find('"', link_start)
        link = "https://time.com" + html[link_start:link_end]

        stories.append({"title": title, "link": link})
    
    return stories

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            html = fetch_html()
            stories = extract_stories(html)
            response = {
                "stories": stories
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(response), "utf-8"))


port = 8080
Handler = MyHttpRequestHandler
httpd = socketserver.TCPServer(("", port), Handler)
print("Serving at port", port)
httpd.serve_forever()
