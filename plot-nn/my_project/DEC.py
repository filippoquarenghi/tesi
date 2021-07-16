import sys
sys.path.append('../')
from pycore.tikzeng import *

DEC = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_input('../examples/CAE/PET92.png'),
    to_Conv(name="input", s_filer=128, n_filer=1, offset="(0,0,0)", to="(0,0,0)", height=40, depth=40, width=1, caption='Input'),
    to_Conv(name="conv1", s_filer=32, n_filer=16, offset="(1,0,0)", to="(input-east)", height=32, depth=32, width=8, caption='Conv1'),
    to_connection( "input", "conv1"),
    to_Conv(name="conv2", n_filer=32, s_filer=8, offset="(1,0,0)", to="(conv1-east)", height=16, depth=16, width=16, caption='Conv2'),
    to_connection( "conv1", "conv2"),
    to_Conv(name="conv3", n_filer=32, s_filer=4, offset="(1,0,0)", to="(conv2-east)", height=8, depth=8, width=16, caption='Conv3'),
    to_connection( "conv2", "conv3"),
    to_Flatten("flatten", 512, 1, offset="(0.5,0,0)", to="(conv3-east)", height=50, depth=2, width=2, caption='Flatten'),
    to_connection( "conv3", "flatten"),
    to_Linear("embedded", 3, 1, offset="(0.5,0,0)", to="(flatten-east)", height=3, depth=2, width=2, caption='Emb.'),
    to_connection( "flatten", "embedded"),
    to_Linear("clustering", 3, 1, offset="(0.25,0,10)", to="(embedded-east)", height=3, depth=2, width=2, caption='Clustering'),
    to_connection( "embedded", "clustering"),
    to_end(),
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(DEC, namefile + '.tex' )


if __name__ == '__main__':
    main()