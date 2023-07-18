tabstr = "    "

def tabify(tab):
    retstr = ""
    for i in range(tab):
        retstr += tabstr
    return retstr 

def main():
    file = open('test.txt', 'r')
    Lines = file.readlines()
    file.close()

    for line in Lines: 
        line = line.strip()
    
    f = open('out.txt', 'w')
    
    tab = 1    
    cnt = 0
    last = ""
    f.writelines("<div class = \"converted-text\">\n")
    for line in Lines:
        if (line == "\n"):
            if (cnt == 1):
                f.writelines(f"{tabify(tab)}<\\{last}>\n")
            cnt = 0 
        elif (line[0] == '#'):
            subcn = 0
            for l in line:
                if (l == '#'):
                    subcn += 1
                else:
                    break 
            line = line[subcn+1:]
            last = f"h{subcn}"
            f.writelines(f"{tabify(tab)}<{last}>\n")
            f.writelines(f"{tabify(tab+1)}{line}")
            f.writelines(f"{tabify(tab)}<\{last}>\n")
            cnt = 0
        elif (cnt == 0):
            last = "p"
            f.writelines(f"{tabify(tab)}<p>\n")
            f.writelines(f"{tabify(tab+1)}{line}")
            cnt = 1 
        else: 
            f.writelines(f"{tabify(tab+1)}<br>{line}")
            cnt = 1
    f.writelines("<\div>\n")

    print("done!")

if __name__ == "__main__":
    main()