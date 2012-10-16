# -*- coding: latin-1 -*-
""" Tarea 1 INF335 - Tecnologías de Bíusqueda en la Web
Universidad Técnica Federico Santa Maria"""

__author__ = "Mati, Nico"
__version__ = "0.1"

#import MySQLdb

from helpers import (document_wrapper, mysql_db, year_to_str, get_abstract,
    get_str_id, remove_stopwords, tokenize, remove_punctuation)

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


def fetch_docs():
    for year in years:
        with open(idx_path + "c" + year + ".txt", "r") as fo:
            for doc in document_wrapper(fo.read().split('\n')):
                db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')
                db.insert_into_mysql(
                    'Document',
                    doc_columns,
                    [(int(doc[2]), doc[0], 2000 + int(year), doc[1])])

                # print "Title: ", doc[0]
                # print "Authors: ", doc[1]
                # print "Year: 20" + year
                # print "ID: " + doc[2]


def fetch_abstracts():
    # Fists we need the Id and year of each document.
    db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')
    results = db.query("SELECT ID, year FROM Document ORDER BY year;")

    for result in results:
        did = result[0]  # Document ID.
        y = result[1]  # Document Year.
        fobj = open(base_path + "nips" + year_to_str(y)
            + "/" + get_str_id(did) + ".txt", "r")

        with fobj as fo:
            print "[Abstract]: ", did, y
            abstract = get_abstract(fo.read())

        if abstract:
            text = remove_punctuation(abstract.lower())
            tokens = tokenize(text)
            cls_abs = remove_stopwords(tokens)
            db.insert_into_mysql(
                'Abstract',
                abs_columns,
                [(did, y, " ".join(cls_abs))])

if __name__ == "__main__":
    # fetch_docs()
    fetch_abstracts()
