#! /usr/bin/env python3
# coding: utf8

import panflute as pf
import uuid
import subprocess as sp

def generic_renderer(dot,renderer=u'dot',format=u'png'):
  """

  """
  ofile = u"/tmp/panviz2_{}.{}".format(uuid.uuid4(),format)
  cmd = u"{} -T{} -o {}".format(renderer,format,ofile)
  #p = sp.Popen([renderer,u'-T'+format,u'-o',ofile],stdin=sp.PIPE,stdout=sp.PIPE)
  p = sp.Popen(cmd.split(' '),stdin=sp.PIPE,stdout=sp.PIPE)
  p.communicate(input=dot)
  p.stdout.close()

  return ofile

def png_renderer(dot,renderer=u'dot'):
  """
    png_renderer:
      - dot(str): dot content to compile
      - renderer(str="dot"): renderer command
  """
  return generic_renderer(dot,renderer,u'png')

def pdf_renderer(dot,renderer=u'dot'):
  """
    latex_renderer:
      - dot(str): dot content to compile
      - renderer(str="dot"): renderer command, dot/neato, can't add arguments now (sap)
  """
  return generic_renderer(dot,renderer,u'pdf')

def base64_renderer(dot,renderer=u'dot'):
  """
    html_renderer:
      - dot(str): dot content to compile
      - renderer(str="dot"): renderer command, dot, neato, no particular arguments are possible now
  """
  cmd = u"{} -Tpng".format(renderer)
  #p1 = sp.Popen([renderer,u'-Tpng'],stdin=sp.PIPE,stdout=sp.PIPE)
  p1 = sp.Popen(cmd.split(' '),stdin=sp.PIPE,stdout=sp.PIPE)
  p2 = sp.Popen([u'base64'],stdin=p1.stdout,stdout=sp.PIPE)
  p1.communicate(input=dot)
  p1.stdout.close()

  return u"data:image/png;base64,"+p2.communicate()[0].rstrip()


class gvimg:
  def __init__(self,elem):
    self.input = pf.stringify(elem).encode('utf8')
    self.cmd_renderer = u'dot'
    self.renderer = png_renderer

    if u'renderer' in elem.attributes :
      self.cmd_renderer = elem.attributes[u'renderer']

    if u'html' in elem.doc.format:
      self.renderer = base64_renderer
    if elem.doc.format == u'latex':
      self.renderer = pdf_renderer

    if u'caption' in elem.attributes:
      self.caption = elem.attributes[u'caption']
    else:
      self.caption = pf.stringify(elem).split('\n',1)[0][1:]

  def run(self):
    url = self.renderer(self.input,self.cmd_renderer)
    pfcaption = (pf.convert_text(self.caption))[0].content
    return pf.Para(pf.Image(*pfcaption,url=url,title=u'fig:'+self.caption))


def action(elem,doc):
  if isinstance(elem,pf.CodeBlock) and u'dot' in elem.classes :
    return gvimg(elem).run()

def main(doc=None):
  return pf.run_filter(action,doc=doc)

if __name__ == '__main__':
  main()

