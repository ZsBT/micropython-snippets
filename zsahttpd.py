#
#	asyncio http server
#

import gc, utime
import uasyncio as asyncio

class Handler:
    ContentType = 'text/html'
    ResponseCode = 200
    Headers = {'Server':'upy', 'Connection':'close'}
    
    def handle(self, req):
        return "override me"
        


def jsonify(writer, dict):
    import ujson
    yield from start_response(writer, "application/json")
    yield from writer.awrite(ujson.dumps(dict))

def start_response(writer, content_type="text/html", status="200", headers=None):
    yield from writer.awrite("HTTP/1.1 %s OK\r\n" % status)
    yield from writer.awrite("Content-Type: ")
    yield from writer.awrite(content_type)
    if not headers:
        yield from writer.awrite("\r\n\r\n")
        return
    yield from writer.awrite("\r\n")
    if isinstance(headers, bytes) or isinstance(headers, str):
        yield from writer.awrite(headers)
    else:
        for k, v in headers.items():
            yield from writer.awrite(k)
            yield from writer.awrite(": ")
            yield from writer.awrite(str(v))
            yield from writer.awrite("\r\n")
    yield from writer.awrite("\r\n")
        

class HTTPRequest:

    def __init__(self):
        pass

    def read_form_data(self):
        size = int(self.headers[b"Content-Length"])
        data = yield from self.reader.read(size)
        form = parse_qs(data.decode())
        self.form = form

    def parse_qs(self):
        form = parse_qs(self.qs)
        self.form = form



class Webserver:
    host = '0.0.0.0'
    port = 80
    
    def __init__(self, handler):
        self.handler = handler
        
    def _handle(self, reader, writer):
        request_line = yield from reader.readline()
        if request_line == b"":
            print("%s: EOF on request start" % reader)
            yield from writer.aclose()
            return
        req = HTTPRequest()
        # TODO: bytes vs str
        request_line = request_line.decode()
        method, path, proto = request_line.split()
        print('%.3f %s %s "%s %s"' % (utime.time(), req, writer, method, path))
        path = path.split("?", 1)
        qs = ""
        if len(path) > 1:
            qs = path[1]
        path = path[0]
        
        req.method = method
        req.path = path
        req.qs = qs
        req.reader = reader

        valasz = self.handler.handle(req)
        self.handler.Headers['Content-Length'] = len(valasz)
        yield from start_response(writer, self.handler.ContentType, self.handler.ResponseCode, self.handler.Headers )
        yield from writer.awrite(valasz)

    def loopify(self,loop):
	gc.collect()
        print("* Running %s on http://%s:%s/" % (self.__qualname__, self.host, self.port))
        loop.create_task(asyncio.start_server(self._handle, self.host, self.port))
    
    def run(self):
        loop = asyncio.get_event_loop()
        self.loopify(loop)
        loop.run_forever()
        loop.close()
