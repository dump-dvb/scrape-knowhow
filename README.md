# Surprise backup of knowhow.vdv.de PDFs

## Interesting bits

Baseurl for documents: https://knowhow.vdv.de/documents/${INT}/

example cURL to get the pdf (copied from Firefox dev tools):

```sh
curl 'https://knowhow.vdv.de/wp-admin/admin-post.php?action=serve_pdf&token=62637013c4106' \
  -H 'User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.5' \
  -H 'Accept-Encoding: gzip, deflate, br' \
  -H 'Referer: https://knowhow.vdv.de/wp-content/themes/kh/pdf.js/web/viewer.html?file=https%3A%2F%2Fknowhow.vdv.de%2Fwp-admin%2Fadmin-post.php%3Faction%3Dserve_pdf%26token%3D62637013c4106' \
  -H 'DNT: 1' \
  -H 'Connection: keep-alive' \
  -H 'Cookie: PHPSESSID=cttcgu6nb06ou7f5mb00oqs1d9' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
```

In practice can be cut down to:

```sh
curl 'https://knowhow.vdv.de/wp-admin/admin-post.php?action=serve_pdf&token=62637013c4106'
```

Which still works on a different machine and from a different IP

## Crawling

```
curl 'https://knowhow.vdv.de/wp-json/wp/v2/documents?reduced=true&frontend&per_page=1000&page=1&filter%5Bnopaging%5D=true'
```

Returns all the documents metadata. You can find it in [documents.json](./documents.json)

## Token generation

```
curl https://knowhow.vdv.de/wp-json/kh-tm/v1/document/${DOC_ID}?variant=lang-${LANG}_fulltext
```

Returns JSON with status code and if 200, a token.

## Import into Zotero

This relies a lot on the code of [this github gist](https://gist.github.com/danbe/6547077).
It uses the [debug-bridge plugin](https://github.com/retorquere/zotero-better-bibtex/tree/master/test/fixtures/debug-bridge) to import all the files with metadata into zotero.
Execute `./zotero-import.py` after adjusting the password variable.
