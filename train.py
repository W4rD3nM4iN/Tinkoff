import re
import pickle
import argparse
import sys
import os


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir")
    parser.add_argument("--model", required=True, type=str)

    return parser


class train:
    re_compile = re.compile(u'[а-яА-ЯA-Fa-f-]+|[.,:;?!]+')

    def training(self, text, modelfilename):
        if not text:
            text = self.new_text()
        else:
            text = self.get_list_of_files(text)

        lines = self.split_into_lines(text)

        tokens = self.sampling(lines)
        trigrams = self.trigram(tokens)
        model = self.creating_model(trigrams)
        self.save_model(model, modelfilename)

    def new_text(self):
        new_text_file = open('data/newtext.txt', 'w')
        for line in sys.stdin:
            new_text_file.write(line)
        new_text_file.close()
        return ['data/newtext.txt']

    def get_list_of_files(self, directory):
        list = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                list.append(f)
        return list

    def split_into_lines(self, text):
        for file in text:
            data = open(file, encoding='utf-8')
            for line in data:
                yield line.lower()

    def sampling(self, lines):
        for line in lines:
            for token in train.re_compile.findall(line):
                yield token

    def trigram(self, tokens):
        t0, t1 = '@', '@'
        for t2 in tokens:
            yield t0, t1, t2
            if t2 in '!.':
                yield t1, t1, '@'
                yield t2, '@', '@'
                t0, t1 = '@', '@'
            else:
                t0, t1 = t1, t2

    def creating_model(self, trigrams):

        d2 = {}
        d3 = {}

        for t0, t1, t2 in trigrams:
            if (t0, t1) not in d2:
                d2[t0, t1] = 1
            else:
                d2[t0, t1] += 1
            if (t0, t1, t2) not in d3:
                d3[t0, t1, t2] = 1
            else:
                d3[t0, t1, t2] += 1

        model = {}

        for (t0, t1, t2), frequency in d3.items():
            if (t0, t1) in model:
                model[t0, t1].append((t2, frequency / d2[t0, t1]))
            else:
                model[t0, t1] = [(t2, frequency / d2[t0, t1])]

        return model

    def save_model(self, model, modelfilename):
        with open(modelfilename + '.pkl', 'a+b') as file:
            pickle.dump(model, file, protocol=pickle.HIGHEST_PROTOCOL)
        print('Модель успешно сохранена')


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])
    text = args.input_dir
    modelfilename = args.model

    training = train()
    training.training(text, modelfilename)
