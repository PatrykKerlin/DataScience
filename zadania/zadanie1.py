def generator_kodow():
    start = '79-900'
    stop = '80-155'
    kody = []
    for x in range(999 - int(start[3:])):
        kody.append(start[:2] + '-' + str(int(start[3:]) + (x + 1)))
    for z in range(int(stop[3:])):
        if z < 10:
            kody.append(stop[:2] + '-00' + str(z))
        elif 9 < z < 100:
            kody.append(stop[:2] + '-0' + str(z))
        elif 99 < z:
            kody.append(stop[:2] + '-' + str(z))
    print(kody)

generator_kodow()