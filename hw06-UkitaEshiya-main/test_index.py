import pytest
from index import Indexer

# Here's an example test case to make sure your tests are working
# Remember that all test functions must start with "test"
def test_example():
    assert 2 == 1 + 1




def file_as_set(filename):
    """
    Returns all of the non-empty lines in the file, as strings in a set.
    """
    line_set = set()
    with open(filename, "r") as file:
        line = file.readline()
        while line and len(line.strip()) > 0:
            line_set.add(line.strip())
            line = file.readline()
    return line_set

def test_file_contents():
    simple_index = Indexer("wikis/SimpleWiki.xml", "simple_titles.txt",
       "simple_docs.txt", "simple_words.txt")
    simple_index.run() # run the indexer to write to the files
    titles_contents = file_as_set("simple_titles.txt")
    assert len(titles_contents) == 2
    assert "200::Example page" in titles_contents
    assert "30::Page with links" in titles_contents

def test_file_contents(tmp_path):
    # create temporary directory
    tmp_dir = tmp_path / "test_files"
    tmp_dir.mkdir()

    # create indexer and run it to generate output files
    simple_index = Indexer("wikis/SimpleWiki.xml", str(tmp_dir / "simple_titles.txt"),
                           str(tmp_dir / "simple_docs.txt"), str(tmp_dir / "simple_words.txt"))
    simple_index.run()

    # read output files as sets
    titles_contents = file_as_set(str(tmp_dir / "simple_titles.txt"))
    docs_contents = file_as_set(str(tmp_dir / "simple_docs.txt"))
    words_contents = file_as_set(str(tmp_dir / "simple_words.txt"))

    # check contents of titles file
    assert len(titles_contents) == 2
    assert "200::Example page" in titles_contents
    assert "30::Page with links" in titles_contents

    # check contents of docs file
    assert len(docs_contents) == 2
    assert "200 0.5" in docs_contents
    assert "30 0.5" in docs_contents

    # check contents of words file
    assert len(words_contents) == 3
    assert "example 200 1" in words_contents
    assert "page 200 1" in words_contents
    assert "link 30 1" in words_contents
