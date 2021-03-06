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
ckpt = None

def enhance_mini_process(noisy_dir, enhanced_save_dir):
  global smg
  if smg is None:
    smg = build_SMG(ckpt)
  noisy_wav, sr = audio.read_audio(noisy_dir)
  enhanced_wav = enhance_one_wav(smg, noisy_wav)
  noisy_name = Path(noisy_dir).stem
  audio.write_audio(os.path.join(enhanced_save_dir, noisy_name+'_enhanced.wav'),
                    enhanced_wav, PARAM.sampling_rate)


def enhance_one_testset(testset_dir, enhanced_save_dir):
  testset_path = Path(testset_dir)
  noisy_path_list = list(map(str, testset_path.glob("*.wav")))
  func = partial(enhance_mini_process, enhanced_save_dir=enhanced_save_dir)
  # for path in noisy_path_list:
  #   func(path)
  pool = Pool(test_processor)
  job = pool.imap(func, noisy_path_list)
  list(tqdm(job, "Enhancing", len(noisy_path_list), unit="test wav", ncols=60))
  pool.close()
  pool.join()


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

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--n_process', default=1, type=int, help="n processor")
  parser.add_argument('--ckpt', default=None, type=str, help="ckpt dir")
  # parser.add_argument('--noisy_phase', default=0, type=int, help='if use noisy phase')
  parser.add_argument('--mp', default=1, type=int, help='if measure preformance')
  args = parser.parse_args()

  test_processor = args.n_process
  ckpt = args.ckpt
  # noisy_phase = bool(args.noisy_phase)
  if_measure_preformance = bool(args.mp)

  print('n_process:', args.n_process)
  # print("noisy_phase:", noisy_phase)
  print('ckpt:', args.ckpt)
  print('measure_preformance:', if_measure_preformance)

  main()

  if not if_measure_preformance:
    exit(0)
  # calculate pesq, ssnr, csig, cbak, covl
  from .sepm import compare
  import time

  for testset_name, cleanset_name in zip(PARAM.test_noisy_sets, PARAM.test_clean_sets):
    print("Calculate PM %s:" % testset_name, flush=True)
    ref_dir = str(misc_utils.datasets_dir().joinpath(cleanset_name))
    deg_dir = str(misc_utils.enhanced_testsets_save_dir(testset_name))
    t1 = time.time()
    res = compare(ref_dir, deg_dir)
    t2 = time.time()

    pm = np.array([x[1:] for x in res])
    pm = np.mean(pm,axis=0)
    print('time: %.3f' % (t2-t1))
    print('ref=', ref_dir)
    print('deg=', deg_dir)
    print('csig:%6.4f cbak:%6.4f covl:%6.4f pesq:%6.4f ssnr:%6.4f lsd:%6.4f estoi:%6.4f'% tuple(pm))

  """
  run cmd:
  `OMP_NUM_THREADS=1 python -m xx._3_enhance_testsets --ckpt=xxx --n_process=1`
  [csig,cbak,cvol,pesq,snr,ssnr]=evaluate_all('/home/lhf/worklhf/ulaw-SGAN-for-SE/noisy_datasets_16k/clean_testset_wav','/home/lhf/worklhf/ulaw-SGAN-for-SE/exp/se_reMagMSE_cnn/enhanced_testsets/noisy_testset_wav')
  """
