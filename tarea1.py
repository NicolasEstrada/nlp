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

# Stablish database connection
db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')


def fetch_docs():
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
        fobj = open(base_path + "nips" + year_to_str(y)
            + "/" + get_str_id(did) + ".txt", "r")

        with fobj as fo:
            abstract = get_abstract(fo.read())

        if abstract:
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


if __name__ == "__main__":
    # Step 1
    print "[Step 1] Fetching documents headers..."
    fetch_docs()
    # Step 2
    print "[Step 2] Fetching and processing abstracts..."
    fetch_abstracts()
    # Step 3
    print "[Step 3] Calculating the collocations..."
    fetch_collocations()
