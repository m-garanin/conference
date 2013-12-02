# coding: utf-8

from pytils.translit import translify


def upload_to_docs(obj, fname):
    tfn = translify(fname)
    tfn = tfn.replace(' ','')
    tfn = tfn.replace("'",'')
    res = u'docs/%d/%s' % (obj.author.id, tfn)
    return res
