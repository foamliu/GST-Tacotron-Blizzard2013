import matplotlib.pylab as plt
import numpy as np
import pinyin
import soundfile as sf
import torch

import config
from data_gen import TextMelLoader
from utils import text_to_sequence, ensure_folder, plot_data, Denoiser

if __name__ == '__main__':
    checkpoint = 'BEST_checkpoint.tar'
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model']
    model.eval()

    waveglow_path = 'waveglow_256channels.pt'
    waveglow = torch.load(waveglow_path)['model']
    waveglow.cuda().eval().half()
    for k in waveglow.convinv:
        k.float()
    denoiser = Denoiser(waveglow)

    text = "相对论直接和间接的催生了量子力学的诞生 也为研究微观世界的高速运动确立了全新的数学模型"
    text = pinyin.get(text, format="numerical", delimiter=" ")
    print(text)
    sequence = np.array(text_to_sequence(text))[None, :]
    sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

    valid_dataset = TextMelLoader('dev', config)
    ref_mel = valid_dataset.get_mel(config.ref_wav)[None, :]
    ref_mel = torch.autograd.Variable(np.transpose(ref_mel, (0, 2, 1))).cuda().float()

    mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence, ref_mel)
    plot_data((mel_outputs.float().data.cpu().numpy()[0],
               mel_outputs_postnet.float().data.cpu().numpy()[0],
               alignments.float().data.cpu().numpy()[0].T))

    ensure_folder('images')
    plt.savefig('images/mel_spec.jpg')

    mel_outputs_postnet = mel_outputs_postnet.type(torch.float16)
    with torch.no_grad():
        audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
        # denoiser_strength = 0.0
        # audio = denoiser(audio, denoiser_strength)

    audio = audio[0].data.cpu().numpy()
    audio = audio.astype(np.float32)

    print('audio.shape: ' + str(audio.shape))
    print(audio)

    sf.write('output.wav', audio, config.sampling_rate, 'PCM_24')
