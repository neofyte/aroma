import re

#input:
#    file_source:file path
#    file_name:file name
#output:
#    the identifier of the pdf
#
#if a non-arXiv-pdf file is input
#it will raise a 'NonArxivPdf' error
def arxiv_id_parser(arxiv_id):
    #two patterns used before and after 2004 respectively
    #    1:(before 2004) 'arXiv:hep-th/0612073v2'
    #    2:(after 2004) 'arXiv:1305.5767'
    pattern = 'arXiv:\d{4}\.\d{4}(v\d{1})?|arXiv:[a-zA-Z]+\-[a-zA-Z]+/\d{7}(v\d{1})?'
    identifier = re.search(pattern, arxiv_id).group().split(':')[1]
    #identifier looks like 'hep-th/0612073v2' (unicode)
    if identifier:
        return identifier
    else:
        return None
