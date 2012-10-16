# -*- coding: latin-1 -*-
""" Tarea 1 INF335 - Tecnologías de Bíusqueda en la Web
Universidad Técnica Federico Santa Maria"""

__author__ = "Mati, Nico"
__version__ = "0.1"


from helpers import (document_wrapper, mysql_db, year_to_str, get_abstract,
    get_str_id, remove_stopwords, tokenize, remove_punctuation,
    get_collocations)

years = ["01", "02", "03", "04", "05", "06",
"07", "08", "09", "10", "11", "12"]

# Fill the Document table using the cx files
# that contains the document description (year,
# title and autors)

# idx folder relative path
base_path = "nipstxt/"
idx_path = base_path + "idx/"
doc_columns = ["ID", "title", "year", "authors"]
abs_columns = ["ID", "year", "abstract"]
coll_columns = ["ID", "year", "collocation"]


def fetch_docs():
    db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')

    for year in years:
        rows = []
        with open(idx_path + "c" + year + ".txt", "r") as fo:
            for doc in document_wrapper(fo.read().split('\n')):
                rows.append((int(doc[2]), doc[0], 2000 + int(year), doc[1]))
                # print "Title: ", doc[0]
                # print "Authors: ", doc[1]
                # print "Year: 20" + year
                # print "ID: " + doc[2]

        db.insert_into_mysql(
                    'Document',
                    doc_columns,
                    rows)


def fetch_abstracts():
    # First we need the Id and year of each document.
    db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')
    results = db.query("SELECT ID, year FROM Document ORDER BY year;")

    rows = []
    for result in results:
        did = result[0]  # Document ID.
        y = result[1]  # Document Year.
        fobj = open(base_path + "nips" + year_to_str(y)
            + "/" + get_str_id(did) + ".txt", "r")

        with fobj as fo:
            # print "[Abstract]: ", did, y
            abstract = get_abstract(fo.read())

        if abstract:
            text = remove_punctuation(abstract.lower())
            tokens = tokenize(text)
            cls_abs = remove_stopwords(tokens)
            # decoded_abs = []
            # for w in cls_abs:
            #     try:
            #         decoded_abs.append(w.decode('utf8'))
            #     except UnicodeDecodeError:
            #         print "[Abstract] Can't decode ", did, y
            #         decoded_abs.append(w)
            rows.append((did, y, " ".join(cls_abs)))

    db.insert_into_mysql(
                'Abstract',
                abs_columns,
                rows)


def fetch_collocations():
    # First we need fectch all the abstracts for each year.
    db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')

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


if __name__ == "__main__":
    # Step 1
    # fetch_docs()
    # Step 2
    # fetch_abstracts()
    # Step 3
    fetch_collocations()
