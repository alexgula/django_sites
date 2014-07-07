# coding=utf-8
import sys
from picassoft.search_engines import GoogleEngine, YandexXMLEngine
from picassoft.search_engines.file_search import scan_files


def main():
    scan_dir = u'.'
    log_dir = scan_dir
    debug = False
    engine_list = [
        GoogleEngine(debug=debug, log_dir=log_dir),
        YandexXMLEngine(u'seo-lyamin',
            u'03.133090775:96d22c1d0123309d56f57ecccbf7c06e'),
    ] # Пока Лямин не освободил IP, будем использовать его ключ, потому как наш ключ нельзя активировать на тот же IP
    if len(sys.argv) > 1:
        for pattern in sys.argv[1:]:
            scan_files(scan_dir, engine_list, pattern)
    else:
        scan_files(scan_dir, engine_list)

if __name__ == "__main__":
    main()
