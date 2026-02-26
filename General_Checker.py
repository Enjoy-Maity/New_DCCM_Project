def int_checker(value):
    try:
        floated_value = float(value)
        int_value = int(floated_value)
        return True

    except ValueError:
        return False

def result_dict_sorter(result_dict):
    if len(result_dict) > 0:
        reasons = list(result_dict.keys())
        if len(reasons) > 0:
            i = 0
            while i < len(reasons):
                selected_reason = reasons[i]
                if all(
                    list(
                        map(int_checker, result_dict[selected_reason])
                        )
                    ):
                    
                    result_dict[selected_reason] = list(
                        map(
                            str, 
                            sorted(
                                list(
                                    set(
                                        map(
                                            int, 
                                            result_dict[selected_reason]
                                            )
                                        )
                                    )
                                )
                            )
                        )
                i += 1
    return result_dict

