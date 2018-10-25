import numpy 
output_file = "test01.in"

size = 15
random_matrix = numpy.random.randint(0,2,(size, size))
with open(output_file, 'w') as fout:
    fout.write(str(size) + '\n')
    for rows in random_matrix:
        for x in rows:
            fout.write(str(x) + ' ')
        fout.write('\n')
    
