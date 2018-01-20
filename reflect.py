#!/usr/bin/env python

import sys
import socket


def detect_af(addr):
    return socket.getaddrinfo(addr,
                              None,
                              socket.AF_UNSPEC,
                              0,
                              0,
							  socket.AI_NUMERICHOST)[0][0]


def write_response(resp):
    for record in response:
        sys.stdout.write('\t'.join(record) + '\n')
    sys.stdout.flush()


class QueryHandler(object):
    def __init__(self):
        pass


    def handle_badcmd(self, _):
        return [['FAIL']]


    def handle_helo(self, q):
        try:
            ver = int(q[1])
            if ver == 1:
                return ['OK', 'reflect.py is ready']
            else:
                return handle_badcmd(q)
        except
            return handle_badcmd(q)


    def handle_q(self, q):
        try:
            _, domain, qclass, qtype, ID, remote_ip = q
            if qclass != 'IN':
                return [['LOG', 'Only IN addresses are supported'],
                        ['FAIL']]
            if qtype in 

        except:
            return handle_badcmd(q)


    qtable = {
        'HELO': handle_hello,
        'Q': handle_q,
    }


    def handle(self, q):
        return qtable.get(q[0], handle_badcmd)(self, q)


def main():
    handler = QueryHandler()
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            query = line.rstrip('\n').split('\t')
            resp = handler.handle(query)
            write_response(resp)
    except KeyboadInterrupt:
        sys.stdout.flush()


if __name__ == '__main__':
    main()
