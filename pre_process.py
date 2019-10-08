import os
import pickle

from tqdm import tqdm

from config import data_file, tran_file


def get_blizzard_2013():
    print('loading samples...')

    with open(tran_file, 'r') as file:
        lines = file.readlines()

    num_lines = len(lines)
    for i in range(0, num_lines, 3):
        filename = lines[i]
        filename = ''.format(filename)
        text = lines[i+1]


    # data_dir = os.path.join(thchs30_folder, 'data')
    # wave_dir = os.path.join(thchs30_folder, split)
    #
    # samples = []
    #
    # for file in tqdm(os.listdir(wave_dir)):
    #     file_path = os.path.join(wave_dir, file)
    #     if file_path.endswith('.wav'):
    #         text_path = os.path.join(data_dir, file + '.trn')
    #         with open(text_path, 'r', encoding='utf-8') as f:
    #             text = f.readlines()[1].strip()
    #         samples.append({'audiopath': file_path, 'text': text})
    #
    # return samples


def main():
    samples = get_blizzard_2013()

    # data = dict()
    # data['train'] = get_blizzard_2013('train')
    # data['dev'] = get_blizzard_2013('dev')
    # data['test'] = get_blizzard_2013('test')
    #
    # with open(data_file, 'wb') as file:
    #     pickle.dump(data, file)
    #
    # print('num_train: ' + str(len(data['train'])))
    # print('num_dev: ' + str(len(data['dev'])))
    # print('num_test: ' + str(len(data['test'])))


if __name__ == "__main__":
    main()
