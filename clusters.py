# -*- coding: latin-1 -*-
""" Tarea 3 INF335 - Tecnologías de Búsqueda en la Web
Universidad Técnica Federico Santa Maria"""

__author__ = "Mati, Nico"
__version__ = "0.1"

import codecs
from helpers import 

years = ["00", "01", "02", "03", "04", "05", "06",
"07", "08", "09", "10", "11", "12"]

# idx folder relative path
base_path = "nipstxt/"
nips_log_path = "nips/logs/"

cluster_columns = ["year", "k", "cluster_ID",  "des_keyword", "dis_keyword"]

# Stablish database connection
db = mysql_db('localhost', 3306, 'inf335', 'mestrada', '123456')


def fetch_cluster():
    """Fill the Document table using the cx files that contains the document
    description (year, title and autors)"""
    


        db.insert_into_mysql(
                    'Cluster',
                    doc_columns,
                    rows)