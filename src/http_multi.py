import grequests


def exception_handler(request, exception):
    print "Request failed"


def get_multi(urls):
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs, size=10, exception_handler=exception_handler)
