# -*- coding: latin-1 -*-
""" Tarea 1 (Correcciones) & 2 INF335 - Tecnologías de Búsqueda en la Web
Universidad Técnica Federico Santa Maria"""

__author__ = "Mati, Nico"
__version__ = "0.1"

import codecs
from helpers import (document_wrapper, mysql_db, year_to_str, get_abstract,
    get_str_id, remove_stopwords, tokenize, remove_punctuation,
    get_collocations, keyword_wrapper)

years = ["00", "01", "02", "03", "04", "05", "06",
"07", "08", "09", "10", "11", "12"]

# idx folder relative path
base_path = "nipstxt/"
idx_path = base_path + "idx/"
voc_path = "voctxt/"
doc_columns = ["ID", "title", "year", "authors"]
abs_columns = ["ID", "year", "abstract"]
coll_columns = ["ID", "year", "collocation"]
key_doc_columns = ["ID", "year", "keyword"]
keyword_columns = ["ni", "year", "keyword"]
collo_ni_columns = ["ni", "year", "collocation"]
nouns_columns = ["ni", "year", "tag", "keyword"]
nouns_doc_columns = ["ID", "year", "keyword"]
voc_columns = ["ni", "year", "keyword"]
post_columns = ["ID", "year", "keyword"]

# Stablish database connection
db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')


def fetch_docs():
    """Fill the Document table using the cx files that contains the document
    description (year, title and autors)"""
    # Fetch doc headers for each year
    for year in years:
        rows = []
        with open(idx_path + "c" + year + ".txt", "r") as fo:
            for doc in document_wrapper(fo.read().split('\n')):
                rows.append((int(doc[2]), doc[0], 2000 + int(year), doc[1]))

        db.insert_into_mysql(
                    'Document',
                    doc_columns,
                    rows)


def fetch_abstracts():
    # First we need the Id and year of each document.
    results = db.query("SELECT ID, year FROM Document ORDER BY year;")

    rows = []
    for result in results:
        did = result[0]  # Document ID.
        y = result[1]  # Document Year.
        # fobj = open(base_path + "nips" + year_to_str(y)
        #     + "/" + get_str_id(did) + ".txt", "r")

        fobj = codecs.open(base_path + "nips" + year_to_str(y) +
            "/" + get_str_id(did) + ".txt", "r", "latin1")

        with fobj as fo:
            abstract = get_abstract(fo.read())

        if abstract:
            # Remove the end line  cut words
            abstract = abstract.replace("- \n", '')
            text = remove_punctuation(abstract.lower())
            tokens = tokenize(text)
            cls_abs = remove_stopwords(tokens)

            rows.append((did, y, " ".join(cls_abs)))

    db.insert_into_mysql(
                'Abstract',
                abs_columns,
                rows)


def fetch_collocations():
    # First we need fectch all the abstracts for each year.
    for year in years:
        rows = []
        results = db.query(
            "SELECT ID, abstract FROM Abstract WHERE year = 20" + year)

        year_abstracts = ""
        for abstract in results:
            year_abstracts += " " + abstract[1]

        top_colls = get_collocations(tokenize(year_abstracts), 100)

        for r in results:
            colls_to_insert = [c[0] + " " + c[1] for c in top_colls if c[0] + " " + c[1] in r[1]]
            for col in colls_to_insert:
                rows.append((r[0], 2000 + int(year), col))

        db.insert_into_mysql(
                'Collocation',
                coll_columns,
                rows)


def fetch_keywords():
    # Fetch keywords for each each year
    for year in years:
        rows = []
        rows = {"Keyword_Doc": [],
            "Keyword": [],
            "Collocation_ni": []}
        try:
            with open(idx_path + "s" + year + ".txt", "r") as fo:
                for kword in keyword_wrapper(fo.read().split('\n'),
                    2000 + int(year)):

                    rows[kword[0]].append(kword[1])

            db.insert_into_mysql(
                        'Keyword_Doc',
                        key_doc_columns,
                        rows["Keyword_Doc"])
            db.insert_into_mysql(
                        'Keyword',
                        keyword_columns,
                        rows["Keyword"])
            db.insert_into_mysql(
                        'Collocation_ni',
                        collo_ni_columns,
                        rows["Collocation_ni"])

        except IOError:
            # Missing file i.e s00.txt
            pass


def fetch_collocations_ni():
    # First we need fectch all the abstracts for each year.
    for year in years:
        rows = []
        results = db.query(
            "SELECT COUNT(*), year, collocation FROM Collocation " +
            "WHERE year = 20" + year + " GROUP BY collocation")

        for result in results:
            rows.append((result[0], result[1], result[2]))

        db.insert_into_mysql(
                'Collocation_ni',
                collo_ni_columns,
                rows)


def fetch_nouns():
    # First we need fectch all the abstracts for each year.
    from nltk.tag import pos_tag
    from nltk.tokenize import word_tokenize

    for year in years:

        nouns_doc = []
        nouns = []
        nouns_count = {}

        results = db.query(
            "SELECT ID, abstract FROM Abstract WHERE year = 20" + year)
        keywords = db.query(
            "SELECT keyword FROM Keyword WHERE year = 20" + year)

        for aid, abstract in results:
            tokens = word_tokenize(abstract)
            tags = pos_tag(tokens)
            tags = filter(lambda x: len(x[0]) > 2, tags)
            tags = filter(lambda x: x[1] in ["NN", "NNS", "NNP", "NNPS"], tags)
            tags = filter(lambda x: x[0] not in keywords, tags)

            nouns_columns = ["ni", "year", "tag", "keyword"]
            nouns_doc_columns = ["ID", "year", "keyword"]

            for tag in tags:
                nouns_doc.append((aid, 2000 + int(year), tag[0]))

                if tag[0] not in nouns_count:
                    nouns_count[tag[0]] = {"tag": tag[1], "ni": 1}
                else:
                    nouns_count[tag[0]]["ni"] += 1

        for noun in nouns_count:
            nouns.append((nouns_count[noun]["ni"], 2000 + int(year), nouns_count[noun]["tag"], noun))

        db.insert_into_mysql(
                'Nouns',
                nouns_columns,
                nouns)

        db.insert_into_mysql(
                'Nouns_Doc',
                nouns_doc_columns,
                nouns_doc)


def fetch_vocabulary():

    for year in years:

        nouns = db.query(
            "SELECT ni, Nouns.keyword, Nouns_Doc.ID FROM Nouns JOIN Nouns_Doc ON Nouns.keyword = Nouns_Doc.keyword  WHERE ni > 1 AND Nouns.year = 20" + year)
        keywords = db.query(
            "SELECT ni, Keyword.keyword, Keyword_Doc.ID FROM Keyword JOIN Keyword_Doc ON Keyword.keyword = Keyword_Doc.keyword  WHERE ni > 1 AND Keyword.year = 20" + year)

        voc_rows = []
        post_rows = []

        for noun in nouns:
            voc_rows.append((noun[0], 2000 + int(year), noun[1]))
            post_rows.append((noun[2], 2000 + int(year), noun[1]))
        for key in keywords:
            voc_rows.append((key[0], 2000 + int(year), key[1]))
            post_rows.append((key[2], 2000 + int(year), key[1]))

        db.insert_into_mysql(
                'Vocabulario',
                voc_columns,
                list(set(voc_rows)))

        db.insert_into_mysql(
                'Posteo',
                post_columns,
                list(set(post_rows)))


def generate_matrix():

    for year in years:
        posts = db.query(
            "SELECT keyword, ID FROM Posteo WHERE year = 20" + year)

        vocx = open(voc_path + "voc" + year + ".txt", "w+")
        with vocx:
            for post in posts:
                try:
                    vocx.write(post[0] + " " + str(post[1]) + "\n")
                except UnicodeEncodeError:
                    # Omit weird characters (are few)
                    pass


if __name__ == "__main__":
    # # # Step 1
    # print "[Step 1] Fetching documents headers..."
    # fetch_docs()
    # # # Step 2
    # print "[Step 2] Fetching and processing abstracts..."
    # fetch_abstracts()
    # # # Step 3
    # print "[Step 3] Calculating the collocations..."
    # fetch_collocations()
    # # Step 4
    # print "[Step 4] Fetching the keywords..."
    # fetch_keywords()
    # Step 5
    # print "[Step 5] Fetching collocation ocurrences..."
    # fetch_collocations_ni()
    # Step 6
    # print "[Step 6] Fetching nouns..."
    # fetch_nouns()
    # Step 7
    # print "[Step 7] Generating Vocabulary..."
    # fetch_vocabulary()
    # Step 8
    print "[Step 8] Generating Matrix..."
    generate_matrix()
