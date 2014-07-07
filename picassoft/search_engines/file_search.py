# coding=utf-8
import glob
import os


def lines_from_file(file_name):
    with open(file_name) as fp:
        for line in fp:
            line = line.strip()
            if line and line[0] != u'#':
                yield line


def _extract_site_from_file_name(file_name, splitter='__'):
    return file_name.split(splitter)[0]


def _get_file_names(dir_name, pattern):
    """Get text file names in a folder."""
    for file_path in glob.glob(os.path.join(dir_name, pattern)):
        file_name = os.path.split(file_path)[1]
        yield file_path, file_name


def get_site_names(dir_name, pattern):
    for file_path, file_name in _get_file_names(dir_name, pattern):
        site = _extract_site_from_file_name(file_name)
        yield file_path, site


def scan_files(dir_name, engine_list, pattern='*.txt'):
    """Scan each file in a directory and query each search engine with each line as a query.

    File names in a directory must start from site domain names and must have additional symbols after '__'."""
    for file_path, site in get_site_names(dir_name, pattern):
        yield u"{}".format(site)
        yield u"-" * 40
        for i, query in enumerate(lines_from_file(file_path)):
            yield u"{})\t{}:".format(i + 1, query)
            for engine in engine_list:
                pos, result = engine.search(query, site)
                position_name = unicode(pos + 1) if result else 'not found'
                yield u"\t{}\t{}".format(engine.verbose_name, position_name)
        yield u"-" * 40
