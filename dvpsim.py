from __future__ import print_function

from router import Router

import argparse
from collections import deque
import random
import sys

def update_map_map(k1, k2, v, m):
    if k1 not in m:
        m[k1] = { }
    m[k1][k2] = v

class Network:
    def __init__(self, routers, links, events, delay_range=5, debug=False, poison=False):
        self.debug = debug
        self.link_map     = { }
        self.neighbor_map = { }
        self.message_queue = deque()
        for (r1, r2, w) in links:
            # N.B. assumes bidirectional (undirected) networks
            self.link_map[(r1, r2)] = w
            self.link_map[(r2, r1)] = w
            update_map_map(r1, r2, w, self.neighbor_map)
            update_map_map(r2, r1, w, self.neighbor_map)
        self.routers = { r : Router(r, routers, self.neighbor_map[r], self, poison, self.debug) for r in routers }
        self.events = events

    def send(self, msg):
        self.message_queue.append(msg)

    def compute_best_route(self, src, dst):
        route = []
        cur = src
        while cur != dst:
            if cur in route:
                route.append(cur)
                route.append('<loop>')
                return route
            else:
                route.append(cur)
                cur = self.routers[cur].get_next_hop(dst)

        route.append(cur)   # NOTE: cur = dst
        return route

    def compute_all_best_routes(self):
        ret = []
        for r1 in self.routers:
            for r2 in self.routers:
                if r1 != r2: ret.append(self.compute_best_route(r1, r2))
        return ret

    def execute_events(self, cur):
        for (step, ev) in self.events:
            if cur == step:
                if self.debug: print(ev)
                r1, r2 = ev['link']
                weight = ev['weight']
                self.routers[r1].detect_link_change(r2, weight)
                self.routers[r2].detect_link_change(r1, weight)

    def run(self, n):
        if self.debug:
            print('=== Initialization ===')
            for r in self.routers: print(self.routers[r])
            for (r1, r2), weight in self.link_map.iteritems(): print('({}, {}): {}'.format(r1, r2, weight))
            print('====================== ')
        for step in xrange(1, n+1):
            if self.debug: print('Step {} (queue size={})'.format(step, len(self.message_queue)))
            # Process a message from the queue
            if len(self.message_queue) > 0:
                msg = self.message_queue.popleft()
                self.routers[msg.dst].receive_update(msg)
            # Execute every event that should fire on this step
            self.execute_events(step)
        if self.debug:
            print('=== Final State ===')
            for r in self.routers: print(self.routers[r])
            print('===================')
        for route in self.compute_all_best_routes():
            print(route)

def parse_event_file(filename):
    with open(filename, 'rU') as f:
        event_lines = [l.strip().split(' ') for l in f.readlines()]
        events      = [ (int(l[0]), { 'link' : (l[1], l[2]), 'weight' : (int(l[3])) }) for l in event_lines ]
        return events

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
    parser.add_argument('eventfile', help='file that defines the events that will run during the simulation')
    parser.add_argument('--debug', dest='debug', action='store_true', help='enables debug information')
    parser.add_argument('--poison', dest='poison', action='store_true', help='enables poison reversal (mastery)')
    args = parser.parse_args()
    routers, links = parse_topology_file(args.topfile)
    events = parse_event_file(args.eventfile)
    network = Network(routers, links, events, debug=args.debug, poison=args.poison)
    network.run(args.steps)

if __name__ == '__main__':
    main()
