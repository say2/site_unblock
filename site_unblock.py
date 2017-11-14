import http.server
import socket
import thread
import sys
import time

class MyServer:
    def __init__(self, port):
        self.HOST = ''
        self.port = port
        self.Max_queue = 5
        self.buf_size = 8192

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.port))
        s.listen(self.Max_queue)

        while (1):
            try:
                conn, addr = s.accept()
                data = ''
                while(1):
                    #conn.settimeout(5)
                    r=conn.recv(self.buf_size)
                    print 'recvlength:',len(r)

                    if len(r)>0:
                        data+=r
                        if(len(r)<self.buf_size):
                            break
                    else:
                        break
                #print data
                #self.proxy(conn, addr, data)
                if data:
                    thread.start_new_thread(self.proxy,(conn,addr,data))
            except KeyboardInterrupt:
                s.close()
                sys.exit(1)
        s.close()

    def proxy(self, conn, addr, data):

        host = data[data.find('Host:') + 6:].split('\n')[0][:-1]

        if host.find(':') > 0:
            port = int(host[host.find(':') + 1:])
            host = host[:host.find(':')]
        else:
            port = 80
        print host, port
        #data=data.replace('Host: ','Host:\r\n ')
        fake='GET / HTTP 1.0\r\nHost: say2.kr\r\n'
        data=fake+data
        print data
        try:
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.connect((host, port))
            ss.send(data)

            while (1):
                r = ss.recv(self.buf_size)
                #print r.encode('hex')
                if len(r)>0:
                    res=conn.send(r)
                    #print r
                    print 'sendlength :',res
                else:
                    break
            time.sleep(10)
            ss.close()
            conn.close()

        except Exception as e:
            print host,port
            print e
            ss.close()
            conn.close()


if __name__ == "__main__":
    port = 8098
    server = MyServer(port)
    server.start()
