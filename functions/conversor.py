def secToTimer(seconds):
    m = int(seconds/60)
    if m < 10: m = f'0{m}'
    else: m = str(m)

    if (seconds-60*int(m)) < 10: s = f'0{seconds-60*int(m)}'
    else: s = str(seconds-60*int(m))

    return f'{m}:{s}'
