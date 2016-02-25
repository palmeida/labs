# -*- coding: utf-8 -*-

'''
This module produces SVG files with hemicycles representations.
'''

##
# Imports
##

from pysvg.structure import svg, g, defs, use, title
from pysvg.builders import TransformBuilder, ShapeBuilder
from pysvg.linking import a
from pysvg.shape import path

from math import sin, cos, pi, floor
from operator import attrgetter
import os.path

from chairs import Hemicycle
from entities import MP, Party

##
#  Config
##

SVGBASE = '/home/helder/prg/hc/hc/share/hc'
TRANSX = 0
TRANSY = -50

##
# Exceptions
##


class SVGError(Exception):
    pass

##
#  Utils
##


def degrees(angle):
    '''Converts radians to degrees'''
    return angle * 180 / pi

##
#  SVG
##


class HemicycleSVG(object):
    '''
    This class creates svg representations of hemicycles.
    '''
    def __init__(self, hc, mps=None):
        '''
        hc - hemicycle object
        mps - list of MP objects, which must have these attributes:
                * name (string)
                * party (Party object)

        The Party object must have the following attributes:
                * initials
                * order (seating order in parliament, left to right)
                * head_color (color for the MP heads in the SVG)
                * body_color (color for the MP bodies in the SVG)
        '''
        self.hc = hc
        self.mps = mps
        self.chairs = []
        self.parties = self.get_parties()

        # Check if the number of chairs in the results matches the
        # calculated hemicycle number of chairs.
        nchairs = sum([party.result for party in self.parties])
        if nchairs != hc.nchairs:
            raise SVGError(
                'Results chair number don\'t match the hemicycle size.')

    def get_parties(self):
        parties = list(set([mp.party for mp in self.mps]))
        return sorted(parties, key=attrgetter('order'))

    def get_mp_generators(self):
        '''Create generators for all party MPs'''

        mp_generators = {}

        for party in self.parties:
            mps = filter(
                lambda x: x.party.initials == party.initials,
                self.mps
                )
            mp_generators[party.order] = iter(mps)
        return mp_generators

    def chair_dist(self):
        '''Chair distribution on the hemicycle'''

        mp_generators = self.get_mp_generators()

        def smallest(parties, first_row):
            '''Returns the number of chairs for the smalest party in parties'''
            result = 0
            seats = 0

            for party in parties:
                result += party.result
                seats += sum(party.seats)
            remaining = result - seats

            smallest_party = parties[0]

            dist_seats = sum(smallest_party.seats)
            remaining_seats = smallest_party.result - dist_seats

            percent = float(remaining_seats) / remaining
            nc = int(floor(percent * first_row))

            if sum(smallest_party.seats) == smallest_party.result:
                return 0

            return 1 if not nc else nc

        def fill_row(parties, seats):
            parties.sort(key=lambda party: party.result)

            # Find how many seats we have for each party on this row
            for i in range(len(parties)):
                party = parties[i]

                party_row_seats = smallest(parties[i:], seats)
                party.seats.append(party_row_seats)
                seats -= party_row_seats

        parties = self.parties
        for party in parties:
            party.seats = []

        hc = [row['nchairs'] for row in self.hc.rows()]
        for row in hc:
            fill_row(parties, row)
            parties.sort(key=lambda party: party.order)

        # Create an hemicicle matrix, each row is empty, we'll fill the
        # rows afterwards
        chairs = []
        for i in range(self.hc.nrows):
            row = []
            for j in range(len(parties)):
                party = parties[j]
                for seat in range(party.seats[i]):
                    row.append(next(mp_generators[j]))

            chairs.append(row)

        self.chairs = chairs

    def svg_dimention(self):
        # The SVG coord system origin is on the lower left:
        height = self.hc.outer_radius()
        width = self.hc.outer_radius() * 2
        return width, height

    def chair_svg(self, row, column, mp):
        angle, x, y = self.hc.chair_location(row, column)

        width, height = self.svg_dimention()

        # NOTE: Original comment stated '30' is half the size of the svg chair
        # NOTE: 30 was replaced with 25 to make the hemicycle roughly balanced
        x = x + width / 2 - 25 * cos(pi/2 - angle) + TRANSX
        y = height - y - 25 * sin(pi/2 - angle) + TRANSY

        # Chair translation and rotation parametrization
        th = TransformBuilder()
        th.setRotation('%f' % (90 - degrees(angle)))
        th.setTranslation('%f,%f' % (x, y))

        u = use()
        u._attributes['xlink:href'] = '#%s' % mp.party.initials
        u.set_transform(th.getTransform())

        return u

    def chair(self, party):
        style = 'stroke:black;stroke-width:4.0;fill:%s;'
        head = ShapeBuilder().createCircle(30, 25, 16)
        head.set_class('head')
        head.set_style(style % party.head_color)
        body = ShapeBuilder().createPolygon('12,50,47,50,30,15')
        body.set_class('body')
        body.set_style(style % party.body_color)

        group = g()
        group.set_id(party.initials)
        group.addElement(body)
        group.addElement(head)

        return group

    def defs(self):
        d = defs()
        for party in self.parties:
            d.addElement(self.chair(party))
        return d

    def svg(self):
        if not self.chairs:
            raise SVGError('You need to calculate the chair distribution.')

        width, height = self.svg_dimention()

        # SVG doc
        s = svg(height="100%", width="100%")
        s.set_viewBox("0 0 %d %d" % (width, height))
        t = title()
        t.appendTextContent('Parlamento')
        s.addElement(t)

        # Create the party groups
        groups = {}
        for i, party in enumerate(self.parties):
            groups[i] = g()
            groups[i].set_id('%s_group' % party.initials)
            t = title()
            t.appendTextContent('Grupo Parlamentar %s' % party.initials)
            groups[i].addElement(t)

        # Add the chair shape definition
        s.addElement(self.defs())

        # Distribute the chairs
        for i, row in enumerate(self.chairs):
            for j, mp in enumerate(row):
                angle, x, y = self.hc.chair_location(i, j)
                x = x + width / 2
                y = height - y

                t = title()
                t.appendTextContent(mp.name)
                mp_link = a()
                # TODO This link is a placeholder, it will be more sensible
                mp_link._attributes['xlink:href'] = 'http://parlamento.pt'
                mp_link.addElement(t)
                mp_link.addElement(self.chair_svg(i, j, mp))
                groups[mp.party.order].addElement(mp_link)

        # Insert the party groups into the svg
        for i, party in enumerate(self.parties):
            s.addElement(groups[i])

        return s.getXML()


if __name__ == '__main__':
    # Parties
    be = Party(initials='BE', order=0, head_color='black', body_color='red')
    cdu = Party(initials='CDU', order=1, head_color='red', body_color='red')
    ps = Party(initials='PS', order=2, head_color='pink', body_color='pink')
    psd = Party(initials='PSD', order=3, head_color='orange', body_color='orange')
    pp = Party(initials='PP', order=4, head_color='blue', body_color='blue')

    # MPs
    mps = []
    for i in range(1, 8):
        mps.append(MP(name='Deputado_BE_%d' % i, party=be))
    for i in range(8, 24):
        mps.append(MP(name='Deputado_CDU_%d' % i, party=cdu))
    for i in range(24, 98):
        mps.append(MP(name='Deputado_PS_%d' % i, party=ps))
    for i in range(98, 207):
        mps.append(MP(name='Deputado_PSD_%d' % i, party=psd))
    for i in range(207, 231):
        mps.append(MP(name='Deputado_PP_%d' % i, party=pp))

    # Results
    for party in (be, cdu, ps, psd, pp):
        result = len(filter(lambda x: x.party.initials == party.initials, mps))
        party.result = result

    # Create the hemicycle
    hc = Hemicycle(
        chair_width=60,
        chair_height=60,
        nchairs=230,
        nrows=8,
        hangle=(4/3)*pi
        )

    # Graphical representation of the hemicycle
    hc_svg = HemicycleSVG(hc, mps)

    hc_svg.chair_dist()

    print hc_svg.svg()
