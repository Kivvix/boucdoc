#! /usr/bin/env python

import panflute as pf

def prepare(doc):
    if u'abstract' in doc.metadata :
        text = [ pf.Para(pf.Str(txt)) for txt in doc.get_metadata('abstract').split('\n\n') ]
        abstract = pf.Div(pf.BlockQuote(*text),identifier="abstract")
        doc.content.insert(0,abstract)

def action(elem,doc):
    pass

def main(doc=None):
    return pf.run_filter(action,doc=doc,prepare=prepare)

if __name__ == '__main__':
    main()

