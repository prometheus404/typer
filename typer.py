import time
import curses
import sys
import getopt
import random

def main(stdscr, argv):

    opts, args = getopt.getopt(argv, "hf:w:", ["file=", "words="])
    
    stdscr.clear()
    stdscr.refresh()
   
    if len(opts) == 0:
        stdscr.addstr("typer.py -f <file>")
        stdscr.getkey()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            stdscr.addstr("typer.py -f <file> -w <words>")
            stdscr.getkey()
            sys.exit()
        elif opt in ("-f", "--file"):
            dic_file = arg
        elif opt in ("-w", "--words"):
            try:
                n_words = int(arg) 
            except ValueError:
                stdscr.addstr("argument -w should be an integer")
                stdscr.getkey()
                sys.exit(2)


    
    #windows
    top = curses.newwin(1, curses.COLS, 0, 0)
    height = int((curses.LINES*2)/3)
    length = int((curses.COLS*2)/3)
    height_pad = int((curses.LINES - height)/2)
    length_pad = int((curses.COLS - length)/2)
    text_area = curses.newwin(height, length, height_pad, length_pad)
    top.addstr(0,0,'wpm: ', curses.A_REVERSE)
    wpm_pad = 4

    #text setup
    text = text_setup(dic_file, n_words)

    #first print
    #TODO: evitare che le parole vengano interrotte a meta
    for t in text:
        text_area.addstr(t['txt']+' ', t['color'])
    text_area.move(0,0)
    top.refresh()
    text_area.refresh()
    
    #cursor position
    cursor_pad = 0
    
    #variables
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    acc = stdscr.getkey()
    start_time = int(time.time())
    word = 0
    wpm = 0
    seconds = 0

    while True:
        seconds = round(time.time() - start_time)
        if seconds != 0:
            wpm = round(60*len([x for x in text if x['color'] == curses.color_pair(2)])/seconds)
        if word >= len(text):
            stdscr.getkey()
            break
        key = stdscr.getkey()
        if key == ' ': 
            cursor_pad += len(text[word]['txt'])+1
            if text[word]['txt'] == acc:
                text[word]['color'] = curses.color_pair(2)
            else:
                text[word]['color'] = curses.color_pair(1)
            
            acc = ''
            word = word + 1
        elif key == 'KEY_BACKSPACE':
            acc = acc[0:-1]
        else:
            acc = acc+key
        text_area.move(0,0)
        for t in text:
            text_area.addstr(t['txt']+' ', t['color'])
        top.addstr(0, wpm_pad, str(wpm)+'     sec: '+str(seconds)+'    ', curses.A_REVERSE)
        text_area.move(int(cursor_pad/length), cursor_pad%length)
        
        if text[word]['txt'][0:len(acc)] == acc:
            text_area.addstr(acc, curses.color_pair(3))
        else:
            text_area.addstr(acc, curses.color_pair(1))
            
        text_area.move(int((cursor_pad+len(acc))/length), (cursor_pad+len(acc))%length)
        
        top.refresh()
        text_area.refresh()

def text_setup(dictionary, num):
    with open(dictionary) as dic:
        r = ""
        for w in dic.readlines():
            r = r + w
        words = r.split()
        text = []
        for n in range(num):
            text.append({'txt': words[random.randrange(len(words))], 'color': 0})
        return text

if __name__ == "__main__":
    curses.wrapper(main, sys.argv[1:])
