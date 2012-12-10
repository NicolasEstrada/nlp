# -*- coding: latin-1 -*-
""" Tarea 3 INF335 - Tecnologías de Búsqueda en la Web
Universidad Técnica Federico Santa Maria"""

__author__ = "Mati, Nico"
__version__ = "0.1"

from helpers import cluster_wrapper, mysql_db

years = ["00", "01", "02", "03", "04", "05", "06",
"07", "08", "09", "10", "11", "12"]

# idx folder relative path
nips_log_path = "nips/logs/"
result_path = "nips/results/"

cluster_columns = ["year", "k", "cluster_ID",  "des_keywords", "dis_keywords"]

# Stablish database connection
db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')


def fetch_cluster():
    """Fill the Document table using the cx files that contains the document
    description (year, title and autors)"""
    rows = []
    for year in years:
        with open(result_path + "nips" + year + "_5.log", "r") as fo:
            for cluster in cluster_wrapper(fo.read().split('\n')):
                print "inserting"

                row = [2000 + int(year), 5] + cluster
                row = tuple(row)
                rows.append(row)

            db.insert_into_mysql(
            'Cluster',
            cluster_columns,
            rows)

if __name__ == "__main__":
    # # Step 1
    print "[Step 1] Fetching clusters results..."
    fetch_cluster()
