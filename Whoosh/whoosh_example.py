#coding=utf-8
# 아래와 같은 모듈을 import 합니다


# content 에 태깅들 두개로 쪼개서 넣고
# titles 에 원문넣고
# 총 10개 뽑아서 0.5점씩 추가를 한다.
# 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5  ( 이거 반대로 스코어링 ))
# 기본은 BM25F 알고리즘 - 이게 뭔지 알아봐야함
import os
from whoosh.index import create_in
from whoosh.fields import *

# indexdir을 색인 폴더로 이용해 봅니다
indexdir = './whoosh_ndx'

if not os.path.exists(indexdir):
    os.makedirs(indexdir)

# SQL의 DDL을 이용하듯이 특정 문서의 Schema 설정을 우선 합니다.
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT,
				tags=NGRAMWORDS(stored=True))

# 스키마 정보로 색인용 폴더를 생성합니다.
ix = create_in(indexdir, schema)

# Inverted색인을 위한 writer를 정의합니다.
writer = ix.writer()

# 다음과 같이 문서를 추가합니다.
writer.add_document(title=u"First document", path=u"/a",
                    content=u"This is the first document we've added!",
                    tags=u"우리는 민족중흥의 역사적 사명을 띄고")

writer.add_document(title=u"third document", path=u"/a",
                    content=u"The 3 one is even more interesting!",
                    tags=u"나도 태어는났어. 저기도")

writer.add_document(title=u"Second document", path=u"/b",
                    content=u"The second one is even more interesting!",
                    tags=u"이땅에 태어났다. 이에 우리는")

writer.add_document(title=u"My document", content=u"This is my document!",
                    path=u"/a", tags=u"first short")

writer.add_document(title=u"Second try", content=u"This is the second example.",
                    path=u"/b", tags=u"second short")

writer.add_document(title=u"Third time's the charm", content=u"Examples are many.",
                    path=u"/c", tags=u"short")
writer.commit()


# 문서 추가를 마친 후 commit을 합니다. with 컨텍스트 사용도 가능합니다.
# Query를 위한 Parser 모듈을 가져옵니다.
from whoosh.qparser import QueryParser

# 색인이 searcher 컨텍스를 이용합니다.
with ix.searcher() as searcher:
	# N-Gram 단어라 "사명을..." 에서 "명을"을 입력해도 찾아옵니다.
	query = QueryParser("tags", ix.schema).parse(u'땅에 태어')
	results = searcher.search(query,limit=10)
	for r in results:
		print (r,r.score,r.rank,r.docnum)