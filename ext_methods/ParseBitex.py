"""
@inproceedings{dong2023dfvsr,
  title={DFVSR: directional frequency video super-resolution via asymmetric and enhancement alignment network},
  author={Dong, Shuting and Lu, Feng and Wu, Zhe and Yuan, Chun},
  booktitle={Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence},
  pages={681--689},
  year={2023}
}

Dong S, Lu F, Wu Z, et al. "DFVSR: directional frequency video super-resolution via asymmetric and enhancement alignment network,"
in Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, 2023, pp. 681–689.

/author, "title," in booktitle, year, pp. (pages)./

@article{guo2016lime,
  title={LIME: Low-light image enhancement via illumination map estimation},
  author={Guo, Xiaojie and Li, Yu and Ling, Haibin},
  journal={IEEE Transactions on image processing},
  volume={26},
  number={2},
  pages={982--993},
  year={2016},
  publisher={IEEE}
}

Guo X, Li Y, Ling H. "LIME: Low-light image enhancement via illumination map estimation,"
in IEEE Transactions on image processing, vol. 26, no. 2, pp. 982–993, 2016.

/author, "title," in journal, vol. (volume), no. (number), pp. (pages), year./

address,author,booktitle,chapter,crossref,edition,editor,howpublished,
institution,journal*,key,month,note,number,organization,
pages,publisher,school,series,title,type,volume,year
"""

import re


def is_match(content, target):
    match = re.search(target, content)
    if match is not None:
        return match.group(1)
    return None


def parse_conference(content):
    # parse title
    title = is_match(content, r'title={([^}]+)}')
    if title is None:
        raise Exception("No title found.")

    # parse authors
    authors = is_match(content, r'author={([^}]+)}')
    if authors is None:
        raise Exception("No authors found.")
    authors = authors.split(' and ')
    new_authors = ""
    for i, author in enumerate(authors):
        if i > 2:
            new_authors += 'et al.'
            break
        author = author.split(' ')
        author = author[0] + ' ' + author[1][0]
        new_authors += author
        if len(authors) == i + 1:
            new_authors += '.'
        else:
            new_authors += ', '

    # parse journal
    booktitle = is_match(content, r'booktitle={([^}]+)}')
    if booktitle is None:
        raise Exception("No book title.")

    # parse pages
    year = is_match(content, r'year={([^}]+)}')
    if year is None:
        raise Exception("No year found.")

    # parse pages
    pages = is_match(content, r'pages={([^}]+)}')

    # / author, "title," in booktitle, year, pp.(pages). /
    reference = "{} \"{},\" in {}, {}{}.".format(new_authors, title, booktitle, year, f", pp. {pages}" if pages else "")

    return reference, title, new_authors, booktitle + ' ' + year


def parse_journal(content):
    # 使用正则表达式匹配BibTeX中的作者、标题、书名、页码和年份信息
    # parse title
    title = is_match(content, r'title={([^}]+)}')
    if title is None:
        raise Exception("No title found.")

    # parse authors
    authors = is_match(content, r'author={([^}]+)}')
    if authors is None:
        raise Exception("No authors found.")
    authors = authors.split(' and ')
    new_authors = ""
    for i, author in enumerate(authors):
        if i > 2:
            new_authors += 'et al.'
            break
        author = author.split(' ')
        author = author[0] + ' ' + author[1][0]
        new_authors += author
        if len(authors) == i + 1:
            new_authors += '.'
        else:
            new_authors += ', '

    # parse journal
    journal = is_match(content, r'journal={([^}]+)}')
    if journal is None:
        raise Exception("No book title.")

    # parse pages
    year = is_match(content, r'year={([^}]+)}')
    if year is None:
        raise Exception("No year found.")

    # parse pages
    pages = is_match(content, r'pages={([^}]+)}')

    # parse volume
    volume = is_match(content, r'volume={([^}]+)}')

    # parse number
    number = is_match(content, r'number={([^}]+)}')

    # /author, "title," in journal, vol. (volume), no. (number), pp. (pages), year./
    reference = "{} \"{},\" in {}{}{}{}, {}.".format(
        new_authors, title, journal, f", vol. {volume}" if volume else "", f", no. {number}" if number else "",
        f", pp. {pages}" if pages else "", year)

    return reference, title, new_authors, journal + ' ' + year


def parse_bitex(content):
    # 使用正则表达式匹配BibTeX中的作者、标题、书名、页码和年份信息
    conference = re.search(r'@inproceedings{', content)
    if conference is not None:
        return parse_conference(content)
    journal = re.search(r'@article{', content)
    if journal is not None:
        return parse_journal(content)

    if conference is None and journal is None:
        raise Exception("Neither conference nor journal, check bitex content.")


str = """
Chan, K, Wang, X, Yu, K, et al. "Basicvsr: The search for essential components in video super-resolution and beyond," in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2021, pp. 4947--4956.}
}
"""
print(len(str))
