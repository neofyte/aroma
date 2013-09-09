import re

from django.core.exceptions import ValidationError

def validate_identifier(arxiv_id):
    #arxiv_id = 'arXiv:1308.291'
    pattern = 'arXiv:\d{4}\.\d{4}(v\d{1})?|arXiv:[a-zA-Z]+\-[a-zA-Z]+/\d{7}(v\d{1})?'
    if re.match(pattern, arxiv_id):
        return arxiv_id
    else:
    	raise ValidationError('Improper arXiv Id')
