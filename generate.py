from numpy.random import choice as rand
import pickle
import argparse
import sys


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--prefix", type=str)
    parser.add_argument("--length", required=True, help='Количество предложений')

    return parser


class generator:

    def generate_sentence(self, model, prefix):
        sentence = ''

        t0, t1 = '@', '@'
        if prefix:
            sentence += prefix
            prefix = prefix.split()[-1]
            t1 = prefix
        while t1 not in '.!?':
            # while t1 not in '.!?':
            try:
                words, probabilities = zip(*model[t0, t1])
            except KeyError:
                t0, t1 = '@', '@'
                words, probabilities = zip(*model[t0, t1])
            t0, t1 = t1, rand(words, p=probabilities)
            if t1 not in '.!?,;:"':
                sentence += ' '
            if t1 == '@':
                sentence += ''
            else:
                sentence += t1

        return sentence.replace('@', '').lstrip().capitalize()

    def load_model(self, filename):
        model = []
        with open(filename, 'rb') as handle:
            try:
                while True:
                    model.append(pickle.load(handle))
            except EOFError:
                pass
        return model[0]


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])
    model = args.model
    prefix = args.prefix
    length = args.length
    modelfilename = args.model

    generator = generator()
    model = generator.load_model(modelfilename)
    for i in range(int(length)):
        sentence = generator.generate_sentence(model, prefix)
        prefix = None
        print(sentence)
