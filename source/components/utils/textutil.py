from itertools import chain

def truncline(text, font, maxwidth):
    words = text.split()  # Split the text into words
    stext = ''
    done = 1
    
    for word in words:
        if font.size(stext + word)[0] <= maxwidth:
            stext += word + ' '
        else:
            done = 0
            break

    stext = stext.rstrip()  # Remove the trailing space
    return len(stext), done, stext


def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped

def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)