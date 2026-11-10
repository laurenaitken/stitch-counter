def parse_pattern(text):
    text = text.replace("*", " * ")
    if ',' not in text:
        split_text = text.split()
    else:
        split_text = text.split(',')

    stitch_tuples = []
    for instruction in split_text:
        instruction = instruction.strip()
        if instruction in ['*', 'k2tog']:
            stitch_tuples.append(instruction)
        else:
            stitch_tuples.append((instruction[0].lower(), int(instruction[1])))

    return stitch_tuples


def expand_pattern(text):
    stitch_tuples = parse_pattern(text)
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

        elif stitch == 'k2tog':
            if repeat_started:
                repeated_pattern.append(stitch)
            else:
                final_stitch_list.append(stitch)
        else:
            count = 0
            while count < stitch[1]:
                if repeat_started:
                    repeated_pattern.append(stitch[0])
                else:
                    final_stitch_list.append(stitch[0])
                count += 1
        
    return final_stitch_list
    