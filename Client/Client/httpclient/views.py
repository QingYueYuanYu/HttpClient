import socket
import ssl
from urllib.parse import urlparse, urlencode
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.contrib import messages  # 导入消息模块

# Helper function to create HTTP request headers
def create_http_request(method, host, path, headers=None, body=None):
    request = f"{method} {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    if headers:
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
    if body:
        request += f"Content-Length: {len(body)}\r\n"
    request += "Connection: close\r\n\r\n"
    if body:
        request += body
    return request

def send_http_request(host, port, request, use_ssl=False):
    response = ""
    if use_ssl:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.sendall(request.encode())
                while True:
                    data = ssock.recv(4096)
                    if not data:
                        break
                    response += data.decode(errors='replace')
    else:
        with socket.create_connection((host, port)) as sock:
            sock.sendall(request.encode())
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data.decode(errors='replace')
    return response

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    images = soup.find_all('img', src=True)
    links = soup.find_all('a', href=True)

    text_content = [p.get_text() for p in paragraphs]
    image_sources = [img['src'] for img in images if img['src'].endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    hyperlinks = [(link['href'], link.get_text()) for link in links]

    return text_content, image_sources, hyperlinks

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('url')
        method = request.POST.get('method')
        post_data = request.POST.get('post_data')

        if not user_input.startswith("http://") and not user_input.startswith("https://"):
            user_input = "http://" + user_input

        parsed_url = urlparse(user_input)
        host = parsed_url.hostname
        path = parsed_url.path or "/"
        port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)
        use_ssl = parsed_url.scheme == "https"

        headers = {"User-Agent": "PythonHTTPClient/1.0"}
        body = None

        if method == "POST":
            body = urlencode(dict(pair.split('=') for pair in post_data.split('&')))
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        # request_str = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n"
        # for key, value in headers.items():
        #     request_str += f"{key}: {value}\r\n"
        # if body:
        #     request_str += f"Content-Length: {len(body)}\r\n"
        # request_str += "Connection: keep-alive\r\n\r\n"
        # if body:
        #     request_str += body
        # print("Init Request")
        # print(request_str)
        request_str = create_http_request(method, host, path, headers, body)
        # print("Opt Request")
        # print(request_str)

        # 发送请求并获得响应
        response = send_http_request(host, port, request_str, use_ssl)
        response_headers, response_body = response.split("\r\n\r\n", 1)

        # 解析 HTML 内容
        text_content, image_sources, hyperlinks = parse_html(response_body)

        # print("Response Headers:")
        # print(response_headers)
        # print("Response Body:")
        # print(response_body)
        messages.success(request, "发送成功")  # 成功消息

        return render(request, 'httpclient/index.html', {
            'response_headers': response_headers,
            'text_content': text_content,
            'image_sources': image_sources,
            'hyperlinks': hyperlinks,
        })

    return render(request, 'httpclient/index.html')