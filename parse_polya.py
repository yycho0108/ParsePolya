#!/usr/bin/env python3

import fitz


def main():
    filename = '/home/jamiecho/Documents/Papers/Polya_How-to-solve-it.pdf'
    with fitz.open(filename) as doc:
        text = ''
        for pnum, page in enumerate(doc):
            text += F'PAGE:{pnum:04d}\n'
            text += page.getText()

    with open('/tmp/polya.txt', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    main()
