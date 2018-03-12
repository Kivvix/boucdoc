#! /usr/bin/env python
# coding: utf8

import panflute as pf

def action ( elem,doc ) :
  if isinstance( elem , pf.CodeBlock ) and u'include' in elem.attributes :
    fromLine = toLine = 0
    data = open(elem.attributes[u'include'],'r').readlines()
    
    if u'from' in elem.attributes :
      fromLine = int(elem.attributes[u'from'])-1
    if u'to' in elem.attributes :
      toLine   = int(elem.attributes[u'to'])
    if u'length' in elem.attributes :
      toLine   = fromLine + int(elem.attributes[u'length'])

    attr = elem.attributes
    attr[u'startFrom'] = str(fromLine+1)

    if toLine == 0 :
      rawCode = ''.join(data[fromLine:])
    else:
      rawCode = ''.join(data[fromLine:toLine])

    code = pf.CodeBlock(rawCode,identifier=elem.identifier,classes=elem.classes[:],attributes=elem.attributes)
    return code

def main(doc=None):
  return pf.run_filter(action,doc=doc)

if __name__ == '__main__':
  main()


