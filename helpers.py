"""Custom functions for document processing """

__author__ = "Mati, Nico"
__version__ = "0.1"


def document_wrapper(input_file):
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
