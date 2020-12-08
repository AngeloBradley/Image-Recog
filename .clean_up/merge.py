items = set()

with open("requirements.txt", 'r') as r:
    lines = r.readlines()

    for line in lines:
        items.add(line.replace('\n', ''))

    items = sorted(list(items), key=str.casefold)

    with open("global_requirements.txt", 'w') as g:
        for item in items:
            g.write(item + '\n')