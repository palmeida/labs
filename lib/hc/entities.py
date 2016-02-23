'''
This module contains entities to be represented in the hemicycle
'''


class MP(object):
    '''Representation of a parliament MP'''

    def __init__(self, name=None, party=None):
        '''
        name - name of the MP
        party - Party object of the MP's party
        '''

        self.name = name
        self.party = party


class Party(object):
    '''Representation of a party'''

    def __init__(self, initials, order, head_color=None, body_color=None):
        '''
        name - name of the party
        order - integer with the order of the party in the hemicycle
        '''
        self.initials = initials
        self.order = order
        self.name = None
        self.head_color = head_color
        self.body_color = body_color
        self.result = None

