lines = []

def upisi(kod):
  global lines 

  kod = kod.split('\n')

  lines.extend(kod)

def zavrsi():
  with open('a.frisc', 'w') as file:

    global lines

    finalni_kod = '\n'.join(lines)
    file.writelines(finalni_kod)

if __name__ == '__main__':
  upisi('\thello')
  upisi('world\n!')
  zavrsi()