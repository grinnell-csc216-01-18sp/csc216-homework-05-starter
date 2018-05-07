from __future__ import print_function

import sys

# NOTE: in Python 3, ints are unbounded, so we would instead use
#       sys.maxsize (the system's maximum word size) as the max
MAX_WEIGHT = sys.maxint

class Message:
    def __init__(self, src, dst, dv):
        """ Creates a new message that contains a router's updated distance vector.

        Note: exposes two fields, src and dst, that contain the names of the
        source and destination of the message respectively.

        Arguments:
        src (str) - the name of the source router
        dst (str) - the name of the destination router
        dv  (distance vector) - the distance vector (presumably, of src)
        """
        # TODO: implement me
        pass

    def __str__(self):
        """ Produces a string representation of a Message, suitable for debugging. """
        # TODO: implement me
        pass

class Router:

    def __init__(self, name, all_routers, neighbors, network, poison, debug=False):
        """ Creates and initializes this router with the given parameters.

        Arguments:
        name (str) - the name of the router
        all_routers (list(str)) - the names of all known routers in the network
        neighbors (map(str, float)) - a mapping from neighbors of this router
            to weights of links connecting this router to its neighbors
        network - the network this router is attached to
        poison (bool) - whether the router should utilize the poisoned reverse strategy
        debug - whether the program is executing in debug mode (for the
            purposes of debug printing)
        """
        # TODO: implement me
        pass

    def receive_update(self, msg):
        """ Receives an updated distance vector from a neighbor on the network.

        Arguments:
        msg (Message) - the message sent by a neighbor to this node containing
            its updated distance vector
        """
        # TODO: implement me
        pass

    def update_distances(self):
        """ Updates this router's distance vector according to the DV algorithm. """
        # TODO: implement me
        pass

    def get_next_hop(self, dst):
        """ Returns the next hop in the best path from this router to the destination. """
        # TODO: implement me
        pass

    def detect_link_change(self, neighbor, weight):
        """ Updates this router when it detects that its link with its specified neighbor has changed to the new, updated weight. """
        # TODO: implement me
        pass

    def __str__(self):
        """ Produces a string representation of a Router, suitable for debugging. """
        # TODO: implement me
        pass
