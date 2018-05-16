import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from utils2 import *

class MEDDataset(Dataset):

    def __init__(self, file_name, train=True):
        inputs, outputs = load_dataset(file_name)
        inputs, outputs, in_vocab, out_vocab = preprocess_data(inputs, outputs, train)
        self.inputs = inputs
        self.outputs = outputs
        self.in_vocab = in_vocab
        self.out_vocab = out_vocab

    def __len__(self):
        return self.inputs.shape[0]

    def __getitem__(self, index):
        src = get_indices(self.inputs[index], self.in_vocab[1])
        trg = get_indices(self.outputs[index], self.out_vocab[1])
        return src, trg

def med_collate_fn(data):

    def _pad_sequences(seqs):
        lens = [len(seq) for seq in seqs]
        padded_seqs = torch.zeros(len(seqs), max(lens)).long()
        for i, seq in enumerate(seqs):
            end = lens[i]
            padded_seqs[i, :end] = torch.LongTensor(seq[:end])
        return padded_seqs, lens

    data.sort(key=lambda x: len(x[0]), reverse=True)
    src_seqs, trg_seqs = zip(*data)
    src_seqs, src_lens = _pad_sequences(src_seqs)
    trg_seqs, trg_lens = _pad_sequences(trg_seqs)

    #(batch, seq_len) => (seq_len, batch)
    src_seqs = src_seqs.transpose(0,1)
    trg_seqs = trg_seqs.transpose(0,1)

    return src_seqs, src_lens, trg_seqs, trg_lens


def main():
    ds = MEDDataset("data/german-task2-train")
    train_iter = DataLoader(dataset=ds,
                            batch_size=3,
                            shuffle=True,
                            num_workers=4,
                            collate_fn=med_collate_fn)

    i = 0
    for src_seqs, src_lens, trg_seqs, trg_lens in train_iter:
        if i == 0:
            print("src seqs ==================================")
            print(src_seqs)
            print("src lens ==================================")
            print(src_lens)
            print("trg seqs ==================================")
            print(trg_seqs)
            print("trg_lens ==================================")
            print(trg_lens)
            print("".join([ds.in_vocab[0][x] for x in src_seqs[:,0]]))
            print("".join([ds.out_vocab[0][x] for x in trg_seqs[:,0]]))
        else: break
        i += 1
    print(len(ds.out_vocab[0]))

if __name__ == "__main__":
    main()
