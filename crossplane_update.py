#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import tarfile

import bs4
import requests


def get_dirindex():
    r = requests.get("http://nginx.org/en/docs/dirindex.html")
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    directives = set(a.text for a in soup.select("#content a"))
    return sorted(directives)


def get_mainline_nginx_version():
    r = requests.get("http://nginx.org/en/download.html")
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    mainline_table = soup.select("#content > table")[0]
    version_column = mainline_table.select("tr > td")[1]
    version_link = version_column.select("a")[0]
    return version_link.text.strip().replace("nginx-", "")


def download_nginx_release(release, path):
    url = "https://github.com/nginx/nginx/archive/release-%s.tar.gz" % release
    r = requests.get(url)
    r.raise_for_status()
    disposition = r.headers["content-disposition"]
    filename = re.search(r"filename=(\S+)", disposition).group(1)
    full_path = os.path.join(os.path.abspath(path), filename)
    with open(full_path, "wb") as fd:
        fd.write(r.content)
    return full_path


def extract_tarfile(path):
    path = path.replace(".tar.gz", "") + ".tar.gz"
    dirname = os.path.dirname(path)
    with tarfile.open(path) as tar:
        tar.extractall(path=dirname)
    return path.replace(".tar.gz", "")


def cleanup_tarfile(path):
    path = path.replace(".tar.gz", "")
    if os.path.exists(path):
        shutil.rmtree(path)
    if os.path.exists(path + ".tar.gz"):
        os.remove(path + ".tar.gz")


def find_files_with_extension(path, ext):
    for root, dirs, files in os.walk(path):
        dirs.sort()
        files.sort()
        for f in files:
            if f.endswith(ext):
                yield os.path.join(root, f)


def search_for_directive(loaded_files, directive):
    for f in sorted(loaded_files.keys()):
        lines = iter(loaded_files[f])
        for line in lines:
            line = line.rstrip()
            if line.endswith('{ ngx_string("%s"),' % directive):
                defline = next(lines).strip()
                while "," not in defline:
                    defline += next(lines).strip()
                yield defline.replace("|", " | ")


def main():
    # get the full list of documented directives from the nginx docs
    dirindex = get_dirindex()

    # find the most recent nginx OSS release
    version = get_mainline_nginx_version()

    # download the tarball for the most recent nginx OSS mainline release
    tarpath = download_nginx_release(version, "/tmp")

    # extract the tarball
    srcpath = extract_tarfile(tarpath)

    try:
        srcpath = os.path.join(srcpath, "src")
        c_files = find_files_with_extension(srcpath, ext=".c")

        # read files into memory so they aren't being opened and closed again and again
        loaded_files = {}
        for f in c_files:
            with open(f) as fd:
                loaded_files[f] = fd.readlines()

        print("{")
        no_defs = []
        for directive in dirindex:
            deflines = search_for_directive(loaded_files, directive)
            deflines = [x.rstrip(",") for x in deflines]
            if deflines:
                # print the bitmask definition for the directive
                print("    '%s': [" % directive)
                print("        " + ",\n        ".join(deflines))
                print("    ],")
            else:
                # if no definition was found in the source code then this directive
                # needs to be investigated manually, so don't print it now and instead
                # print it later at the bottom under the comment
                no_defs.append(directive)

        # print the directives that had no found definitions in the source code so
        # the user of the script knows which ones to look for in the docs manually
        print("")
        print("    # nginx+ directives [definitions inferred from docs]")
        for directive in no_defs:
            print("    '%s': [" % directive)
            print("    ],")
        print("}")
    finally:
        # clean up by removing the downloaded tarball
        cleanup_tarfile(tarpath)


if __name__ == "__main__":
    main()
