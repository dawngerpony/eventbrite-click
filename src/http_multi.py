import grequests
import socket


def exception_handler(request, exception):
    print "Request failed"


def get_multi(urls):
    rs = (grequests.get(u) for u in urls)
    try:
        return grequests.map(rs, size=25, exception_handler=exception_handler)
    except socket.error, e:
        print "Socket error!"
