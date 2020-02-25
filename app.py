import re
import urllib.request as request

'''
test url
http://savings.gov.pk/wp-content/uploads/15-01-2019-Rs-750.txt
'''

def txt_cleanup(txt:str):
    txt = txt.replace(r'\t', ' '*4)
    txt = txt.replace(r'\r', '')
    txt = txt.replace(r'\n', '\n')
    return txt


def read_bond_draw_url(url):
    '''
    returns the contents in bytes from the url 
    '''
    try:
        # open url
        URL = request.urlopen(url)
        # read contents
        contents = URL.read()
        # close the url
        URL.close()
        return contents
    except:
        print('\nINCORRECT URL')
        raise
        

def read_bond_txt(url):
    '''
    returns the list of bonds that you own from a .txt file.
    The file should be saved in the following format: Bonds_Rs.{amount}.txt
    '''
    try:
        match = re.search(r'Rs-(\d+)', url)
        rs = match.group(1)
    except AttributeError:
        print('IS THE URL CORRECT? MATCH WAS NOT FOUND.')
        raise
    try:
        with open(f"bonds_Rs.{rs}.txt", "r") as f:
            return f.read().split("\n")
    except FileNotFoundError:
        gap()
        print(f'YOU DO NOT HAVE {rs}- BONDS OR THE FILE DOES NOT EXIST')
        raise


def search_bond_draw(url, show_output=False):
    '''
    searches the draw url for the bonds in the txt file.
    '''
    # convert from bytes to string the data obtained form the url
    draw = str(read_bond_draw_url(url))
    # read the txt file on disk
    bonds = read_bond_txt(url)
    if show_output:
        print(txt_cleanup(draw))
        print('bonds:', bonds)
    # declare a list that will hold all the matches found
    match_list = []
    gap()
    # for each bond in the txt file
    for bond in bonds:
        # strip away the leading and trailing whitespace
        bond = bond.strip()
        # search for that bond in draw
        match = re.search(bond, draw)
        if match:
            print('# match found!', match.group())
            # append it to the match list
            match_list.append(bond)
    return match_list
   

def do_cmd():
    cmd = input('>> ').lower()

    if cmd[:3] == 'url':
        URL = input('url: ')
        if URL == '':
            print('URL IS NULL. TYPE URL AND TRY AGAIN')
            do_cmd()
        print('# found:', search_bond_draw(URL, '-o' in cmd)) 
    elif cmd == 'quit':
        quit()  
    elif cmd == '?' or cmd == 'help':
        gap()
        print('''Bond files should be named in the following format:
            Bonds_Rs.{amount}.txt''')
        gap()
        print('type quit to quit app.')
        print('type url to enter url.')
        main()
    elif cmd == '':
        do_cmd()
    else:
        print('cmd not recognized. Press ? or help to see the available cmd.')
        do_cmd()


def main():
    # gap()
    # print('type help or ? to see avaiable cmd.\n')

    # do_cmd()
    while True:
        try:
            if do_cmd():
                break
        except Exception:
            pass


def gap():
    print('-'* 56+'+')

    
if __name__ == "__main__":
    main()

