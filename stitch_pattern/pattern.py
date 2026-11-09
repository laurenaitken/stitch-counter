def expand_pattern(text):
    if ',' not in text:
            split_text = text.split(" ")
    else:
         split_text = text.split(', ')
    

    stitch_tuples = []
    for instruction in split_text:
        if instruction == '*':
            stitch_tuples.append(instruction)
        else:
            stitch_tuples.append((instruction[0], int(instruction[1])))

    final_stitch_list = []
    repeat_started = False

    for stitch in stitch_tuples:
        if stitch == '*':
            if not repeat_started:
                repeat_started = True
                repeated_pattern = []

            else:
                repeat_started = False

        elif stitch[0] == 'x':
            repeated_pattern = repeated_pattern * stitch[1]
            final_stitch_list.extend(repeated_pattern)           
                
        else:    
            count = 0
            while count < stitch[1]:
                if repeat_started:
                    repeated_pattern.append(stitch[0])
                else:
                    final_stitch_list.append(stitch[0])
                count += 1
        
    return final_stitch_list
    