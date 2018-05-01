from __future__ import print_function

from router import Router

import argparse
import Queue
import random
import sys

def update_map_map(k1, k2, v, m):
    if k1 not in m:
        m[k1] = { }
    m[k1][k2] = v

class Network:
    def __init__(self, routers, links, delay_range=5, debug=False):
        self.debug = debug
        self.link_map     = { }
        self.neighbor_map = { }
        self.message_queue = Queue.Queue()
        for (r1, r2, w) in links:
            # N.B. assumes bidirectional (undirected) networks
            self.link_map[(r1, r2)] = w
            self.link_map[(r2, r1)] = w
            update_map_map(r1, r2, w, self.neighbor_map)
            update_map_map(r2, r1, w, self.neighbor_map)
        self.routers = { r : Router(r, routers, self.neighbor_map[r], self, self.debug) for r in routers }

    def send(self, msg):
        self.message_queue.put(msg)

    def debug_print(self, msg):
        if self.debug:
            print(msg)

    def run(self, n):
        if self.debug:
            print('=== Initialization ===')
            for r in self.routers: print(self.routers[r])
            for (r1, r2), weight in self.link_map.iteritems(): print('({}, {}): {}'.format(r1, r2, weight))
            print('====================== ')
        for step in xrange(1, n+1):
            self.debug_print('Step {}'.format(step))
            if not self.message_queue.empty():
                msg = self.message_queue.get()
                self.routers[msg.dst].receive_update(msg)
        print('=== Final State ===')
        for r in self.routers: print(self.routers[r])
        print('===================')

def parse_topology_file(filename):
    with open(filename, 'rU') as f:
        routers = f.readline().strip().split(' ')
        link_lines = [l.strip().split(' ') for l in f.readlines()]
        links   = [ (l[0], l[1], float(l[2])) for l in link_lines ]
        return (routers, links)

def main():
    parser = argparse.ArgumentParser(description='Simulates the Distance Vector pathfinding algorithm')
    parser.add_argument('steps', type=int, help='number of steps to run the simulation')
    parser.add_argument('topfile', help='file that defines the topology of the network')
    parser.add_argument('--debug', dest='debug', action='store_true', help='enables debug information')
    args = parser.parse_args()
    routers, links = parse_topology_file(args.topfile)
    network = Network(routers, links, debug=args.debug)
    network.run(args.steps)

if __name__ == '__main__':
    main()
