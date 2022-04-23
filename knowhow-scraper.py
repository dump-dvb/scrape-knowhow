#!/usr/bin/env python
import requests
import json
import sys
import time

pdf_base_url =  r'https://knowhow.vdv.de/wp-admin/admin-post.php?action=serve_pdf&token='
token_base_url =  r'https://knowhow.vdv.de/wp-json/kh-tm/v1/document/'
variant = [  r'variant=lang-de_fulltext', r'variant=lang-en_fulltext' ]
outdir = r'./out/'

with open('documents.json', 'r') as f:
    documents = json.load(f)

for e in variant:
    for d in documents:
        token_url = token_base_url + str(d['id']) + r'?' + e
        sys.stderr.write("ID {0}: Trying token at {1}\n".format(d['id'], token_url))
        r = requests.get(token_url)
        if r.ok:
            token = json.loads(r.content)['token']
            sys.stderr.write("ID {0}: got token {1}\n".format(d['id'], token))
            r.close()
        else:
            sys.stderr.write("ID {0}: HTTP {1}\n".format(d['id'], r.status_code))
            r.close()
            pass

        rpdf = requests.get(pdf_base_url + token)
        sys.stderr.write("ID {0}: HTTP {1}\n".format(d['id'], rpdf.status_code))

        try:

            if 'application/octet-stream' in rpdf.headers.get('content-type'):
                sys.stderr.write("ID {0}: Got octet-stream ^_^\n".format(d['id']))
                if rpdf.content[1:4] == b"PDF":
                    filename = d['doc_num'] + '_' + str(d['id']) + '_' +  d['title@de_DE_formal'][0:20] + e +  '.pdf'
                    filename = filename.replace(r'/', '_').replace(r'=', '-')
                    with open(outdir + filename, 'wb') as outpdf:
                        outpdf.write(rpdf.content)
                        sys.stderr.write("ID {0}: wrote {1}\n".format(d['id'], outdir + filename))
                else:
                    sys.stderr.write("ID {0}: got {1} content type but no PDF\n".format(d['id'], rpdf.headers.get('content-type')))
            else:
                sys.stderr.write("ID {0}: got {1} content type\n".format(d['id'], rpdf.headers.get('content-type')))
     
            rpdf.close()
        except FileNotFoundError:
            pass

