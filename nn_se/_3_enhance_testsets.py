import os
import tensorflow as tf
import collections
from pathlib import Path
import numpy as np
from tqdm import tqdm
from functools import partial
from multiprocessing import Pool
import sys

from .utils import misc_utils
from .utils import audio
from .inference import build_SMG
from .inference import enhance_one_wav
from .inference import SMG

from .FLAGS import PARAM

test_processor = 1
smg = None

def enhance_mini_process(noisy_dir, enhanced_save_dir):
  global smg
  if smg is None:
    smg = build_SMG()
  noisy_wav, sr = audio.read_audio(noisy_dir)
  enhanced_wav = enhance_one_wav(smg, noisy_wav)
  noisy_name = Path(noisy_dir).stem
  audio.write_audio(os.path.join(enhanced_save_dir, noisy_name+'_enhanced.wav'),
                    enhanced_wav, PARAM.sampling_rate)


def enhance_one_testset(testset_dir, enhanced_save_dir):
  testset_path = Path(testset_dir)
  noisy_path_list = list(map(str, testset_path.glob("*.wav")))
  func = partial(enhance_mini_process, enhanced_save_dir=enhanced_save_dir)
  job = Pool(test_processor).imap(func, noisy_path_list)
  list(tqdm(job, "Enhancing", len(noisy_path_list), unit="test wav", ncols=60))


def main():
  for testset_name in PARAM.test_noisy_sets:
    print("Enhancing %s:" % testset_name, flush=True)
    _dir = misc_utils.enhanced_testsets_save_dir(testset_name)
    if _dir.exists():
      import shutil
      shutil.rmtree(str(_dir))
    _dir.mkdir(parents=True)
    testset_dir = str(misc_utils.datasets_dir().joinpath(testset_name))
    enhanced_save_dir = str(_dir)
    enhance_one_testset(testset_dir, enhanced_save_dir)

if __name__ == "__main__":
  misc_utils.initial_run(sys.argv[0].split("/")[-2])

  if len(sys.argv) > 1:
    test_processor = int(sys.argv[1])
  main()

  """
  run cmd:
  `OMP_NUM_THREADS=1 python -m xx._3_enhance_testsets 3`
  """
