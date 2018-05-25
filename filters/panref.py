#! /usr/bin/env python

"""
  panref a module to do some reference to equation
  TODO : same thing for figure and table (flemme)
"""

import panflute as pf
import io
import subprocess
import uuid
import re

class eqLabel:
  def __init__ (self,h=[0,0,0,0,0,0],n=0,i="eq",level=1):
    self.h = h
    self.n = n
    self.i = i
    self.level = level

  def __str__(self):
    return ".".join([ str(x) for x in self.h[:self.level] ])+"."+str(self.n)

  def id (self):
    return "#"+self.i

  def elemToId (self,elem):
    self.i = pf.stringify(elem).split()[-1][2:-1]

  def itself(self):
    return eqLabel(self.h[:],self.n,self.i,self.level)

  def incHeader(self,level):
    self.h[level-1] += 1
    self.h[level:] = [0]*(len(self.h)-level)
    if self.level >= level:
      self.n  = 0

  def label(self):
    return ".".join([str(x) for x in self.h[:self.level]])+"."+str(self.n)

  def url(self):
    return "#"+self.label()

  def toLink(self):
    return pf.Link(pf.Str(self.label()),url=self.url())


def has_eq (elem) :
    fchild = elem.content[0]
    return isinstance(fchild,pf.Math) and fchild.format == u'DisplayMath'


def prepare (doc):
  """
    prepare doc object to panref (with heq variable and list of each equation)
  """
  doc.backmatter = []
  doc.heq=eqLabel()
  if u'eq' in doc.metadata :
    doc.heq.level = int(doc.metadata[u'eq'].text)

def action ( elem,doc ) :
  """
    action of filter, get all equations with class and ref them 
  """
  if isinstance(elem,pf.Header):
    doc.heq.incHeader(elem.level)
  if isinstance(elem,pf.Para) and has_eq(elem) and len(elem.content) > 1  :
    doc.heq.n += 1
    doc.heq.elemToId(elem)
    doc.backmatter.append( doc.heq.itself() )

    eq = elem.content[0]
    anchor = pf.Link(identifier=doc.heq.label(),url=doc.heq.url(),classes=["eq"])

    return pf.Para(eq,anchor)

def action2(elem,doc) :
  pattern = re.compile("\[\!(.*?)\]")
  if isinstance(elem,pf.Str) :
    for m in pattern.finditer(elem.text) :
      span = m.span()
      i = m.group(1)
      heq = [ x for x in doc.backmatter if x.i == i ]
      if len(heq) != 0 :
          return [pf.Str(elem.text[0:span[0]]), heq[0].toLink(), pf.Str(elem.text[span[1]:]) ]
    

def finalize(doc):
  """
    finalize filter with a remplacement of each reference with Link
  """
  # loop over doc.backmatter to replace all ref by a link
  """
  for heq in doc.backmatter:
    pf.debug(heq.i)
    ref  = '[!'+heq.i+']'
    link = heq.toLink()
    doc.replace_keyword(ref,link,0)
    doc.replace_keyword(ref+')',link,0)
    doc.replace_keyword('('+ref+')',link,0)
  """

def main(doc=None):
  return pf.run_filters([action,action2],doc=doc,prepare=prepare,finalize=finalize)
  
if __name__ == '__main__':
  main()

