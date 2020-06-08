# Import necessary modules/libraries
import unittest
import sys
import os
import wordninja
import xml.etree.ElementTree as ET
import pickle
import datetime


def printAvailableCommands():
    print('--p   Create a pickle file from an xml file.')

"""
def isRegisteredCommand(s):
    command_characters = ['p']
    for com_char in command_characters:
        if s in com_char:
            return True
    return False
"""

# main
def main(argv):
    import getopt

    os.chdir('../.')

    file_name = ""

    # Check if user if supplying something as an agrument
    if len(argv)>1:

        file_name = ' '.join(argv[1:])
        #print(file_name)

        # Checks to see if the user want to use a command
        action = ''
        if '--' in file_name:
            command_characters = ['p']
            #They want to output to something else:
            # Add a try except
            index = file_name.find(' ')

            action = file_name[0:index+1]
            file_name = file_name[index+1:]

            if 'p' in action:
                if '.xml' not in file_name and '.XML' not in file_name:
                    print("Invalid agruments: xml file required as input")
                    return
            else:
                print("Unknown command, try: ")
                printAvailableCommands()
                return

        input_file_name = './input/' + file_name
        file = open(input_file_name, "r", encoding="utf8")

        # Rename new file to parsed_(input file name)
        new_file_args = ('parsed_',file_name)
        new_file_name = ''.join(new_file_args)
        output_file_name = './output/' + new_file_name
        new_file = open(output_file_name, "w")

        # Perform different action based on file type
        if 'txt' in file_name or 'TXT' in file_name:
            print("Fixing spacing on txt file")
            print(output_file_name, '\n')
            cleanTextFile(file, new_file)
        elif 'xml' in file_name or 'XML' in file_name:
            if 'p' in action:
                print("Converting to pkl file")
                # Rename new_file to a pkl extension matching its input file name
                index = file_name.find('.')
                name = file_name[0:index+1]
                ext = 'pkl'
                new_file_args = (name,ext)
                new_file_name = ''.join(new_file_args)
                output_file_name = './pickles/' + new_file_name
                print(output_file_name, '\n')
                pickleXMLFile(file, output_file_name)
            else:
                print("Fixing spacing on xml file")
                print(output_file_name, '\n')
                cleanXMLFile(file, new_file)
            #createLog()
        else:
            print("Invalid argument. Must include file.")
            return

        # After parsing is complete
        createLog()

    else:
        print("Please supply a command or input")
    return

corrections = []
errors = []

def createLog():
    time_created = str(datetime.datetime.now())
    time_created = time_created.replace(':','.')
    file_name = ('logs/' + time_created + '.txt')
    print('\nSaving log data under ' + file_name)
    log_file = open(file_name, "w")
    log_file.write('Corrections:')
    num_logging_exceptions = 0
    for cor in corrections:
        try:
            log_file.write(cor + '\n')
        except:
            num_logging_exceptions += 1
    log_file.write('\nErrors:')
    for error in errors:
        try:
            log_file.write(error + '\n')
        except:
            num_logging_exceptions += 1
    log_file.write('\nNumber of exceptions while loggins: ' + str(num_logging_exceptions))
    log_file.close()


def cleanTextFile(file, new_file):
    for line in file:
        words = line.split()
        for word in words:
            split_words = wordninja.split(word)
            # Check if a word has actually been split
            if(len(split_words)>1):
                output = split_words[0]
                for i in range(1,len(split_words)):
                    output_args = (output, split_words[i])
                    output = ' '.join(output_args)
                # Output both words to new file
                print(word, "->", output)
                corrections.append('Changed ' + word + ' --> '\
                        + output)
                new_file.write(output)
                new_file.write(" ")
            else:
                new_file.write(word)
                new_file.write(" ")

        new_file.write('\n')

    file.close()
    new_file.close()
    return


def pickleXMLFile(file, new_file):
    #print(file, '->', new_file)
    # Get xml (tree) into a list (stack) and find courses (courseID & descriptions)
    tree = ET.parse(file)
    text = tree.getroot()
    courseID = []
    descriptions = []
    stack = []

    #Convert xml text into stack list
    for subLevel in text:
        recursive(subLevel, stack)

    counter = 0
    for xml in stack:
        if xml.text is not None:
            split_words = wordninja.split(xml.text)
            # Check if a word has actually been split
            if(len(split_words)>1):
                output = split_words[0]
                for i in range(1,len(split_words)):
                    output_args = (output, split_words[i])
                    output = ' '.join(output_args)
                print(xml.text, "->", output)
                corrections.append('Changed ' + xml.text + ' --> '\
                        + output)
                xml.text = output
    with open(new_file, 'wb') as f_handle:
        pickle.dump(stack, f_handle)
        f_handle.close()
    return

def recursive(xml, stack):
    #Remove null and blank lines
    if xml.text is not None:
        if not xml.text.isspace():
            stack.append(xml)
    #Loop to bottom of a nested xml tag
    for subLevel in xml:
        recursive(subLevel, stack)


def cleanXMLFile(file, new_file):
    in_tag = False
    line_number = 1
    for line in file:
        opening_tag_indexes = []
        closing_tag_indexes = []
        if '<' in line and '>' in line:
            indexes = []
            for i in range(0, len(line)):
                if line[i] == '<':
                    opening_tag_indexes.append(i)
                elif line[i] == '>':
                    closing_tag_indexes.append(i)
        final_line = []
        for i in range(0, len(opening_tag_indexes)):
            if i == len(opening_tag_indexes)-2:
                temp_word = line[opening_tag_indexes[i]:closing_tag_indexes[i]+1]
                final_line.append(temp_word)
                temp_word = line[closing_tag_indexes[i]+1:opening_tag_indexes[i+1]]
                final_line.append(temp_word)
            else:
                temp_word = line[opening_tag_indexes[i]:closing_tag_indexes[i]+1]
                final_line.append(temp_word)
        temp_word = ' '.join(final_line)
        words = temp_word.split()
        #words = line.split()
        # A bit of preparsing to make sure tag endings are its own separate words
        # Ex:
        # ['<item','name="item1">','Milk,'</item>']
        #   vs.
        # ['<item', 'name="item1">Milkc</item>']
        for word in words:
            #print(word)
            if('<' in word):
                in_tag = True

            if not in_tag:
                try:
                    # Apparently words are being saved as "<p>ABD", but only when
                    #  the if statement if uncommented

                    # Check if word is a course ID
                    """
                    if word.isupper():
                        new_file.write(output)
                        new_file.write(" ")
                    else:
                    """
                    split_words = wordninja.split(word)
                    # Check if a word has actually been split
                    if(len(split_words)>1):
                        output = split_words[0]
                        for i in range(1,len(split_words)):
                            output_args = (output, split_words[i])
                            output = ' '.join(output_args)
                        # Output both words to new file
                        print(word, "->", output)
                        corrections.append('Changed ' + word + ' --> '\
                                + output)
                        new_file.write(output)
                        new_file.write(" ")
                    else:
                        new_file.write(word)
                        new_file.write(" ")
                except:
                    print("Error caused by xml line number ",line_number)
                    errors.append(word + ' in line ' + str(line_number) + ' in '\
                            + file)
            else:
                try:
                    new_file.write(word)
                    if '<' in word and '>' not in word:
                        new_file.write(" ")
                    if '>' in word:
                        in_tag = False
                except:
                    print("Error caused by xml line number ",line_number)
            #if('>' in word):
            #    in_tag = False
        new_file.write('\n')
        line_number+=1
    file.close()
    new_file.close()
    createLog()
    return

if __name__ == '__main__':
    sys.exit(main(sys.argv))
