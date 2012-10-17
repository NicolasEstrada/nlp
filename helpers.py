"""Custom functions for document processing """

__author__ = "Mati, Nico"
__version__ = "0.2"

import MySQLdb


def document_wrapper(input_file):
    """ This function returns a generator for
    each document on the input file.
    """
    counter = 0
    document = []
    for line in input_file:
        if counter == 4:
            yield document
            document = []
            counter = 1
            document.append(line)
        else:
            counter += 1
            document.append(line)

# Example document description (4 lines)
"""
1 Connectivity Versus Entropy
2 Yaser S. Abu-Mostafa
3 1
4
"""


def get_abstract(input_file):
    """This functions returns the abstract from a document file."""

    abstracts = ["ABSTRACT", "Abstract"]
    intros = ["INTRODUCTION", "Introduction"]
    tmp_str = None

    for a in abstracts:
        if a in input_file:
            tmp_str = input_file.split(a)[1]
            for i in intros:
                if i in tmp_str:
                    tmp_str = tmp_str.split(i)[0]
                    return tmp_str

    # print "[Abstract]: No intro/abs tags found."
    return None


def remove_punctuation(text):
    """This function removes the punctuation in the text"""
    from string import punctuation
    exclude = set(punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)
    return text


def remove_stopwords(tokens, lang="english"):
    """This function removes the stopwords."""
    from nltk.corpus import stopwords
    important_words = filter(lambda x: x not in stopwords.words(lang), tokens)
    return important_words


def decode_text(text):
    """This function decode the text."""
    return text


def tokenize(text):
    """This function tokenize the text."""
    from nltk import word_tokenize
    return word_tokenize(text)


def year_to_str(year):
    """This function returns a string with the last two digits of a year"""
    return str(year)[-2:]


def get_str_id(id):
    """This function return the id with corresponding leading zeros."""
    return str(id).zfill(4)


def get_collocations(tokens, n_collocations=None):
    """This functions returns the collocations for a given set of tokens"""
    from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    colls = sorted(bigram for bigram, score in scored)[:100]

    return colls


# Database class
class mysql_db(object):
    def __init__(self, host, port, dbname, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.db_connection = None
        self.cursor = None
        self.connecting = False

    def __del__(self):
        self.disconnect()

    def connect(self):
        """Call this function to connect to MySQL.
        Output: Returns True when connected"""

        self.connecting = True

        try:
            self.db_connection = MySQLdb.connect(
                passwd=self.password,
                db=self.dbname,
                host=self.host,
                port=self.port,
                user=self.username,
                charset="utf8",
                use_unicode="True")
            # Setting autocommit True for InnoDB transactions
            self.db_connection.autocommit(True)
            self.cursor = self.db_connection.cursor()
            self.connecting = False

        except MySQLdb.Error, e:
            print ("DB Error {0}: {1}"
                               .format(e.args[0], e.args[1]))
            return False

        except Exception, e:
            print ("Error: {0}".format(str(e)))
            return False
        return True

    def disconnect(self):
        """Disconnect from MySQL"""
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None

    def insert_into_mysql(self, table, cols, rows):
        """This function insert into mysql the required rows."""

        self.connect()

        try:
            # Check if the connection has been stablished.
            if self.db_connection:

                query = "INSERT INTO " + table + " ( " + ', '.join(cols) + ") VALUES ("
                query += ", ".join(["%s" for i in range(0, len(cols))])
                query += ")"

                if len(rows) > 1:
                    self.cursor.executemany(query, rows)
                elif len(rows) == 1:
                    self.cursor.execute(query, rows[0])

                # print self.cursor._last_executed

                self.db_connection.commit()
            else:
                print "Connection problem"

        except MySQLdb.Error, e:
            print "[MySql] Error ", e

        finally:
            if self.db_connection:
                self.disconnect()

    def query(self, query):
        """This function insert into mysql the required rows."""

        self.connect()

        try:
            # Check if the connection has been stablished.
            if self.db_connection:
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result

            else:
                print "Connection problem"

        except MySQLdb.Error, e:
            print "[MySql] Error ", e

        finally:
            if self.db_connection:
                self.disconnect()
