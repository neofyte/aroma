import urllib.request

#input:
#    arXive_identifier: e.g.'arXiv:hep-th/0612073v2'
#output:
#    the xml responsed by the arXiv api
def arxiv_query(arxiv_identifier):
    if arxiv_identifier:
        query_header = 'http://export.arxiv.org/api/query?id_list='
        query_url = ''.join([query_header, arxiv_identifier])
        xml_data = urllib.request.urlopen(query_url).read()
        return xml_data
    else:
    	print  ('no arxiv_identifier passed')
    	return None