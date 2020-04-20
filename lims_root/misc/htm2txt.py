IN_FILE = 'hardware.htm'
OUT_FILE = 'hardware.txt'


def process_line(line):
    return line.strip().lower()


def main():
    infile = open(IN_FILE, "r")
    outfile = open(OUT_FILE, "w")

    s = infile.read()
    s1 = s[s.rfind("<table"):s.rfind("</table")]

    for line in s1.splitlines():
        nline = process_line(line)
        if "</a></b></td>" in nline or \
            "</b></a></td>" in nline:

            left = nline.rfind("\">")
            if "</a></b></td>" in nline:
                right = nline.rfind("</a")
            else:
                right = nline.rfind("</b")

            outfile.write(nline[left+2:right]
                          .replace("<b>", "")
                          .upper() + "\n")

    infile.close()
    outfile.close()


main()
