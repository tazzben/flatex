#!/usr/bin/env python

#  This "flattens" a LaTeX document by replacing all 
#  \input{X} lines w/ the text actually contained in X. See 
#  associated README.md for details. 

import os 
import re 
import sys

def is_input(line):
    """
    Determines whether or not a read in line contains an 
uncommented out \input{} statement. Allows only spaces between 
start of line and '\input{}'. 
    """
    tex_input_re = r"""^\s*\\input{[^}]*}"""
    return re.search(tex_input_re, line) 

def get_input(line):
    """
    Gets the file name from a line containing an input statement. 
    """
    tex_input_filename_re = r"""{[^}]*"""
    m = re.search(tex_input_filename_re, line)
    return m.group()[1:]

def combine_path(base_path, relative_ref):
    """ 
    Combines the base path of the tex document being worked on 
with the the relate reference found in that document.  
    """
    os.chdir(base_path)
    #return os.path.join(base_path, relative_ref)
    return os.path.abspath(relative_ref)

def expand_file(base_file):
    """
    Recursively-defined function that takes as input a file and 
returns it with all the inputs replaced with the contents of the 
referenced file.  
    """
	
	output_lines = []
	extensions = ['.tex','.TEX', '.Tex']
	if os.path.isfile(os.path.expanduser(base_file.strip())):
		base_file = os.path.expanduser(base_file.strip())
	elif:
		for item in extensions:
			if os.path.isfile(os.path.expanduser(base_file.strip() + item)):
				base_file = os.path.expanduser(base_file.strip() + item)
				break
	
	if os.path.isfile(base_file):
		print "Combined " + os.path.expanduser(base_file.strip()) + " into main file"
	else:
		return output_lines
    
    f = open(base_file, "r")
    for line in f:
        if is_input(line):
            current_path = os.path.dirname(os.path.abspath(base_file))
            new_base_file = combine_path(current_path, get_input(line))
            output_lines.extend(expand_file(new_base_file))
        else:
            output_lines.append(line)
    f.close() 
    return output_lines 

def main(base_file, output_file):
    g = open(os.path.expanduser(output_file), "w")
    g.writelines(expand_file(base_file))
    g.close()
    return None

if __name__ == '__main__': 
    base_file, output_file = sys.argv[1:]
    main(base_file, output_file)
