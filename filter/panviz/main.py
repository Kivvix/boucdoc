#! /usr/bin/env python

import panflute as pf
import io
import subprocess
import uuid

def tmp_file ( filename,elem ) :
	"""
		write elem content in temporary file with filename name
		I use io module because of UTF-8 encoding
	"""
	tmp_f = io.open(filename,'w',encoding='utf8')
	tmp_f.write(pf.stringify(elem))
	tmp_f.close()


def action ( elem,doc ) :
	"""
		action of filter, get all codeblock of class `dot` and replace it with a figure
	"""
	if isinstance(elem,pf.CodeBlock) and u'dot' in elem.classes :

		renderer = u'dot'
		if u'renderer' in elem.attributes :
			renderer = elem.attributes[u'renderer']

		f = u'png'
		if doc.format == 'latex' :
			f = u'pdf'
		elif u'format' in elem.attributes :
			f = elem.attributes[u'format']

		folder = '/tmp'
		if doc.format == 'html' :
			folder = './build/html'

		gv_in  = "/tmp/panviz_"+str(uuid.uuid4())+".gv"
		image  = "panviz_"+str(uuid.uuid4())+"."+f
		gv_out = folder + "/" + image
		tmp_file( gv_in , elem )

		subprocess.check_call(" ".join([renderer,"-T"+f,gv_in,"-o",gv_out]),shell=True)
		raw_title = pf.stringify(elem).split('\n',1)[0][1:]
		title = (pf.convert_text(raw_title))[0].content 
		
		if doc.format == 'html' :
			gv_out = image
		elif doc.format == 'latex' :
			gv_out = gv_out[:-len(f)-1]

		return pf.Para(pf.Image(*title,url=gv_out,title=u'fig:'+raw_title))

def main(doc=None):
	return pf.run_filter(action,doc=doc)

if __name__ == '__main__':
	main()

