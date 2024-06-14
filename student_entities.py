"""
CPSC 5510, Seattle University, Project #3
:Author: Vaishnavi Punati
:Version: s23
"""

# YOU MAY NOT ADD ANY IMPORTS
from entity import Entity
from student_utilities import to_layer_2


def common_init(self):
    """
    You may call a common function like this from your individual __init__
    methods if you want.
    """
    me = self.node
    print('entity {}: initializing'.format(me))
    print(self)

    dt = self.distance_table

    # self.direct and self.routes are only necessary for
    # the extra credit portion
    self.direct = dt[me][:]
    self.route = [i for i in range(len(dt[me]))]

    self.neighbors = [i for i in range(len(dt[me])) if
                      0 < dt[me][i] < float('inf')]
    print('  sending costs to neighbors')
    for i in self.neighbors:
        to_layer_2(me, i, dt[me])


def common_update(self, packet):
    """
    You may call a common function like this from your individual update
    methods if you want.
    """
    me = self.node
    print('node {}: update from {} received'.format(me, packet.src))
    dt = self.distance_table
    dt[packet.src] = packet.mincost[:]  # make a copy just in case
    c = dt[me][packet.src]

    before = dt[me][:]

    # Added for extra credit
    for i in range(len(dt[me])):
        if self.route[i] == packet.src:
            dt[me][i] = self.direct[i]
            self.route[i] = i

    # check if new row changes any of my min costs
    for i in range(len(dt[me])):
        if c + dt[packet.src][i] < dt[me][i]:
            notify = True
            dt[me][i] = c + dt[packet.src][i]
            self.route[i] = packet.src

    # check if we need to propagate any changes
    if dt[me] != before:
        print('  changes based on update')
        print(self)
        print('  sending mincost updates to neighbors')
        for i in self.neighbors:
            to_layer_2(me, i, dt[me])
    else:
        print('  no changes in node {}, so nothing to do'.format(me))
        print(self)


def common_link_cost_change(self, to_entity, new_cost):
    """
    You may call a common function like this from your individual
    link_cost_change methods if you want.
    Note this is only for extra credit and only required for Entity0 and
    Entity1.
    """
    me = self.node
    print('node {}: link cost to {} changed to '
          '{}'.format(me, to_entity, new_cost))
    self.direct[to_entity] = new_cost
    dt = self.distance_table
    dt[me] = self.direct[:]
    print(self)
    print('  sending costs to neighbors')
    for i in self.neighbors:
        to_layer_2(me, i, dt[me])


class Entity0(Entity):
    """Router running a DV algorithm at node 0"""

    def __init__(self):
        super().__init__()
        me = 0
        self.node = me
        dt = self.distance_table
        dt[me][me] = 0
        dt[me][1] = 1
        dt[me][2] = 3
        dt[me][3] = 7
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost)


class Entity1(Entity):
    """Router running a DV algorithm at node 1"""

    def __init__(self):
        super().__init__()
        me = 1
        self.node = me
        dt = self.distance_table
        dt[me][me] = 0
        dt[me][0] = 1
        dt[me][2] = 1
        common_init(self)

    def update(self, packet):
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        common_link_cost_change(self, to_entity, new_cost)


class Entity2(Entity):
    """Router running a DV algorithm at node 2"""

    def __init__(self):
        super().__init__()
        me = 2
        self.node = me
        dt = self.distance_table
        dt[me][me] = 0
        dt[me][0] = 3
        dt[me][1] = 1
        dt[me][3] = 2
        common_init(self)

    def update(self, packet):
        common_update(self, packet)


class Entity3(Entity):
    """Router running a DV algorithm at node 3"""

    def __init__(self):
        super().__init__()
        me = 3
        self.node = me
        dt = self.distance_table
        dt[me][me] = 0
        dt[me][0] = 7
        dt[me][2] = 2
        common_init(self)

    def update(self, packet):
        common_update(self, packet)
