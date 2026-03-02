def get_num_input_from_list(target, object_list):
    while True:
        try:
            num = int(input(f'Type in the number of the {target} that you want to view: '))
            if num > len(object_list):
                raise ValueError
            break
        except ValueError:
            print(f"Answer must be a whole number equal to or less than {len(object_list)}.")
    return num
