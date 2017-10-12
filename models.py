# -*- coding: utf-8 -*-
import itertools

from openerp import fields, models, api


def wdomain(w, key='name'):
    return [(key, 'ilike', w)]


def w2domain(w, f1='name', f2='description'):
    return ['|', (f1, 'ilike', w), (f2, 'ilike', w)]


def gen_domain(list_name, w=None, op='&'):
    list_name = list_name[:]
    w = w or []
    if len(list_name) > 1:
        if w:
            w = [op, op, list_name[-2], list_name[-1]] + w
        else:
            w = [op, list_name[-2], list_name[-1]]
        list_name = list_name[:len(list_name) - 2]
        return gen_domain(list_name, w)
    elif len(list_name) == 1:
        if w:
            w = [op, list_name[0]] + w
        else:
            w = [list_name[0]]
        return gen_domain([], w)
    else:
        # Aplana
        ww = []
        for p in w:
            if type(p) is list:
                ww.extend(p)
            else:
                ww.append(p)
        return ww


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    search_sequence = fields.Integer('Search Sequence', default=0)
    _order = 'search_sequence, name'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        name = False
        pos = False

        for k, arg in enumerate(args):
            if type(arg) in (list, tuple) and len(arg) == 3 and type(arg[0]) in (unicode, str) and arg[0] in ['name', 'display_name']:
                name = arg[2]
                pos = k
                break
        if name:
            list_name = [s for s in name.split(' ') if s]

            # Búsqueda k-1 palabras en las k palabras que contiene name, k=1, 2, ... k -1, # palabras en name(list_name)
            for k in range(0, len(list_name)):
                for list_s in itertools.combinations(list_name, len(list_name) - k + k):
                    wargs = [w2domain(s) for s in list_s]
                    domain = gen_domain(wargs)
                    wargs = args[:pos] + domain + args[pos + 1:]
                    res = super(ProductTemplate, self).search(args=wargs, offset=offset, limit=limit, order=order, count=count)
                    if res:
                        return res

        return super(ProductTemplate, self).search(args=args, offset=offset, limit=limit, order=order, count=count)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    search_sequence = fields.Integer('Search Sequence', default=0)
    _order = 'search_sequence, name'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        name = False
        pos = False
        for k, arg in enumerate(args):
            if type(arg) in (list, tuple) and len(arg) == 3 and type(arg[0]) in (unicode, str) and arg[0] in ['name', 'display_name']:
                name = arg[2]
                pos = k
                break

        if name:
            list_name = [s for s in name.split(' ') if s]
            # Búsqueda k-1 palabras en las k palabras que contiene name, k=1, 2, ... k -1, # palabras en name(list_name)
            for k in range(0, len(list_name)):
                for list_s in itertools.combinations(list_name, len(list_name) - k + k):
                    wargs = [w2domain(s) for s in list_s]
                    domain = gen_domain(wargs)
                    wargs = args[:pos] + domain + args[pos + 1:]
                    res = super(ProductProduct, self).search(args=wargs, offset=offset, limit=limit, order=order, count=count)
                    if res:
                        return res

        return super(ProductProduct, self).search(args=args, offset=offset, limit=limit, order=order, count=count)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    search_sequence = fields.Integer('Search Sequence', default=0)
    _order = 'search_sequence, name'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        print '== ' * 40
        print args
        name = False
        pos = False
        for k, arg in enumerate(args):
            if type(arg) in (list, tuple) and len(arg) == 3 and type(arg[0]) in (unicode, str) and arg[0] in ['name', 'display_name']:
                name = arg[2]
                pos = k
                break
        if name:
            list_name = [s for s in name.split(' ') if s]
            # Búsqueda k-1 palabras en las k palabras que contiene name, k=1, 2, ... k -1, # palabras en name(list_name)
            for k in range(0, len(list_name)):
                for list_s in itertools.combinations(list_name, len(list_name) - k + k):
                    wargs = [w2domain(s, f2='comment') for s in list_s]
                    domain = gen_domain(wargs)
                    print 'domain'
                    print domain
                    wargs = args[:pos] + domain + args[pos + 1:]
                    print 'wargs'
                    print wargs
                    res = super(ResPartner, self).search(args=wargs, offset=offset, limit=limit, order=order, count=count)
                    if res:
                        return res

        return super(ResPartner, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
