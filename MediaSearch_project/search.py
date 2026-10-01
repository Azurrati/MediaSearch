from rapidfuzz import fuzz

def search(keyword, text_detected, confidence_val):
    if keyword is not None:
        for word in keyword:
            confidence = fuzz.token_set_ratio(text_detected, word)

            if confidence >= confidence_val:
                return (1, text_detected, confidence)
            else:
                return (0)
    else:
        return (2, text_detected)

def decode(result, verbose):
    code = result[0]

    if code == 1:
        text = result[1]
        return text
    elif code == 2 and verbose:
        text = result[1]
        return text

    return ''