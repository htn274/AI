type_animal = {'1':'mamal',
        '2': 'bird',
        '3' : 'reptile',
        '4' : 'fish',
        '5':'amphibian',
        '6' :'insect',
        '7': 'invertebrate'
}
with open('zoo.data.txt', 'r') as f:
    content = f.readlines()
    content = [x.strip() for x in content] 
    out = open('zoo.arff','w')
    for c in content:
        attr = list(c.split(','))
        attr[len(attr) - 1] = type_animal[attr[len(attr) - 1]]
        out.write(",".join(attr))
        out.write("\n")

