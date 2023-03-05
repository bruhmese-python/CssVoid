import sys
import re

REGEX = R'<\s*(?P<styledTag>\w+)[^<>]*\s*(style=\"(?P<style>[^\"]*)\")[^<>]*>'
STYLE_GRP = 2


def new_class(class_name: str, styles: str):
    return '.{}'.format(class_name) + '\n{\n' + '{}'.format(styles) + "\n}\n"


def class_attribute(class_name: str, string: str):
    search_obj = re.search(R'class\s*=\s*\"', string)
    if search_obj is not None:
        i = search_obj.end()
        return string[:i] + class_name + " " + string[i:]
    else:
        i = string.find(" ")
        return string[:i + 1] + "class=\'{}\' ".format(class_name) + string[i + 1:]


if __name__ == '__main__':
    print('''CssVoid (2023)
bruhmese-python. Free to modify and use.
    ''')
    # get file name
    fname = sys.argv[1] if len(sys.argv) > 1 else input("argv[1]:")
    try:
        f = open(fname, 'r')
    except:
        print('Could not open file')

    new_html_file = 'new_{}'.format(fname)
    css_file = '{}_styles.css'.format(fname)

    html = f.read()
    matchobjects = re.finditer(REGEX, html, re.MULTILINE)

    cssOut = str()
    htmlOut = str()

    lastpos = 0

    for index, x in enumerate(matchobjects):

        htmlOut += html[lastpos:x.start()]
        f = x.groupdict()
        if(f['styledTag'] is not None):
            # index is just used to create a random number
            new_class_name = f['styledTag'] + str(index)
            cssOut += new_class(new_class_name, f['style'])
            htmlOut += class_attribute(new_class_name,
                                       html[x.start(): x.span(STYLE_GRP)[0]] + html[x.span(STYLE_GRP)[1]:x.end()])

        lastpos = x.end()

    htmlOut += html[lastpos:]

    # embed link tag in head
    fhead = htmlOut.find('<head>')
    if fhead != -1:
        r = fhead + len('<head>')
        htmlOut = htmlOut[:r] + \
            '<link rel="stylesheet" href="{}">'.format(css_file) + htmlOut[r:]
    f = open(new_html_file, 'w')
    f.write(htmlOut)

    f = open(css_file, 'w')
    f.write(cssOut)

    print('new_html_file : {}'.format(new_html_file))
    print('css_file : {}'.format(css_file))
