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
    for record in resp:
        sys.stdout.write('\t'.join(record) + '\n')
    sys.stdout.flush()


class QueryHandler(object):
    def __init__(self):
        self.qtable = {
            'HELO': self.handle_helo,
            'Q': self.handle_q,
        }
        self.srv_fqdn = socket.getfqdn()
        self.soa = ' '.join([self.srv_fqdn,
                             'vladislav.vm-0.com',
                             '1',
                             '3600',
                             '3600',
                             '604800',
                             '60'])


    def make_fail(self, _):
        return [['FAIL']]


    def handle_badcmd(self, _):
        return [['LOG', 'Malformed query'],
                ['FAIL']]


    def handle_helo(self, q):
        try:
            ver = int(q[1])
            if ver == 1:
                return [['OK', 'reflect.py is ready']]
            else:
                return self.make_fail(q)
        except:
            return self.make_fail(q)


    def make_a_resp(self, q):
        return [['DATA', q[1], 'IN', 'A', '0', '1', q[5]],
                ['END']]


    def make_aaaa_resp(self, q):
        return [['DATA', q[1], 'IN', 'AAAA', '0', '1', q[5]],
                ['END']]


    def make_soa_resp(self, q):
        return [['DATA', q[1], 'IN', 'SOA', '0', '1', self.soa],
                ['END']]


    def handle_q(self, q):
        try:
            _, domain, qclass, qtype, ID, remote_ip = q
            if qclass != 'IN':
                return [['LOG', 'Only IN addresses are supported'],
                        ['FAIL']]

            if qtype == 'SOA':
                return self.make_soa_resp(q)

            af = detect_af(remote_ip)
            if af == socket.AF_INET and qtype in ('A', 'ANY'):
                return self.make_a_resp(q)
            elif af == socket.AF_INET6 and qtype in ('AAAA', 'ANY'):
                return self.make_aaaa_resp(q)
            else:
                return [['LOG', 'Bad address family %d of address %s' % (af, repr(remote_ip))],
                        ['FAIL']]

        except Exception as e:
            return [['LOG', 'Exception: %s' % str(e)],
                    ['FAIL']]


    def handle(self, q):
        return self.qtable.get(q[0], self.handle_badcmd)(q)


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
    except KeyboardInterrupt:
        sys.stdout.flush()


if __name__ == '__main__':
    main()
