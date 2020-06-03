def recursive(xml, stack):
    #Remove null and blank lines
    if xml.text is not None:
        if not xml.text.isspace():
            word_count = xml.text.split(' ')

            split_words = wordninja.split(xml.text)
            if len(word_count) != len(split_words):
            # Check if a word has actually been split
            #if(len(split_words)>1):
                output = split_words[0]
                for i in range(1,len(split_words)):
                    output_args = (output, split_words[i])
                    output = ' '.join(output_args)
                print(xml.text, "->", output)
                xml.text = output
    #Loop to bottom of a nested xml tag
    for subLevel in xml:
        recursive(subLevel, stack)
