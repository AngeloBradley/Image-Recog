packages = set()

with open('global_requirements copy.txt', 'r') as f:
    lines = f.readlines()

    for line in lines:
        package = line[:line.find('=')]
        packages.add(package)

    

    with open('install.txt', 'w') as i:
        for package in packages:
            i.write(package + '\n')