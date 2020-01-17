class StaticKey(object):
  MODEL_TRAIN_KEY = 'train'
  MODEL_VALIDATE_KEY = 'val'
  MODEL_INFER_KEY = 'infer'

  # dataset name
  train_name="train"
  validation_name="validation"
  test_name="test"

  def config_name(self): # config_name
    return self.__class__.__name__

class BaseConfig(StaticKey):
  VISIBLE_GPU = "0"
  root_dir = '/home/lhf/worklhf/se-with-FTL/'
  # datasets_name = 'vctk_musan_datasets'
  datasets_name = 'datasets'
  rawdata_type = 'clean_noise' # 'clean_noisy'
  '''
  # dir to store log, model and results files:
  $root_dir/$datasets_name: datasets dir
  $root_dir/exp/$config_name/log: logs(include tensorboard log)
  $root_dir/exp/$config_name/ckpt: ckpt
  $root_dir/exp/$config_name/test_records: test results
  $root_dir/exp/$config_name/hparams
  '''

  min_TF_version = "1.14.0"

  # _1_preprocess param # just for rawdata_type='clean_noise'
  n_train_set_records = 72000
  n_val_set_records = 3600
  n_test_set_records = 3600
  train_val_snr = [-5, 15]

  train_val_wav_seconds = 3.0

  sampling_rate = 8000

  n_processor_gen_tfrecords = 16
  tfrecords_num_pre_set = 160
  batch_size = 64
  n_processor_tfdata = 4

  """
  @param model_name:
  DISCRIMINATOR_AD_MODEL
  """
  model_name = "DISCRIMINATOR_AD_MODEL"

  relative_loss_epsilon = 0.02
  st_frame_length_for_loss = 512
  st_frame_step_for_loss = 128
  sdrv3_bias = None # float, a bias will be added before vector dot multiply.
  stop_criterion_losses = None
  show_losses = None
  use_wav_as_feature = False
  net_out_mask = True
  frame_length = 256
  frame_step = 64
  no_cnn = True
  blstm_layers = 2
  lstm_layers = 0
  rnn_units = 256
  rlstmCell_implementation = 2
  fft_dot = 129
  max_keep_ckpt = 30
  optimizer = "Adam" # "Adam" | "RMSProp"
  learning_rate = 0.001
  max_gradient_norm = 5.0

  GPU_RAM_ALLOW_GROWTH = True
  GPU_PARTION = 0.45

  s_epoch = 1
  max_epoch = 20
  batches_to_logging = 300

  max_model_abandon_time = 3
  no_abandon = True
  use_lr_warmup = True # true: lr warmup; false: lr halving
  warmup_steps = 4000. # for (use_lr_warmup == true)
  start_halving_impr = 0.01 # no use for (use_lr_warmup == true)
  lr_halving_rate = 0.7 # no use for (use_lr_warmup == true)

  # losses optimized in "DISCRIMINATOR_AD_MODEL"
  D_keep_prob = 0.8
  frame_level_D = False # discriminate frame is noisy or clean
  losses_position = ["not_transformed_losses", "transformed_losses", "d_loss"]
  FT_type = ["LogValueT"] # feature transformer type: "LogValueT", "RandomDenseT", "MelDenseT"
  MelDenseT_n_mel = 80
  melDenseT_trainable = True
  # melMat: tf.contrib.signal.linear_to_mel_weight_matrix(129,129,8000,125,3900)
  # plt.pcolormesh
  # import matplotlib.pyplot as plt

  """
  @param not_transformed_losses/transformed_losses[add FT before loss_name]:
  loss_mag_mse, loss_spec_mse, loss_wav_L1, loss_wav_L2,
  loss_reMagMse, loss_reSpecMse, loss_reWavL2,
  loss_sdrV1, loss_sdrV2, loss_stSDRV3, loss_cosSimV1, loss_cosSimV2,
  """
  not_transformed_losses = ["loss_mag_mse"]
  transformed_losses = ["FTloss_mag_mse"] # must based on magnitude spectrum
  NTloss_weight = []
  Tloss_weight = []
  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  # just for "DISCRIMINATOR_AD_MODEL"
  add_noisy_class_in_D = False
  discirminator_grad_coef = 1.0
  D_loss_coef = 1.0

  cnn_shortcut = None # None | "add" | "multiply"

  feature_transformer_grad_coef = 1.0
  weighted_FTL_by_DLoss = False # if D_loss is large (about 0.7) w_FTL tends to 0.0, otherwise tends to 1.0
  D_strict_degree_for_FTL = 300.0 # for weighted_FTL_by_DLoss

  feature_type = "DFT" # DFT | DCT | QCT

  add_FeatureTrans_in_SE_inputs = False
  LogFilter_type = 3
  logFT_type2_btimes = 1.0
  f_log_a = 1.0 # smaller, curve max smaller
  f_log_b = 0.001 # smaller, curve straighter
  log_filter_eps_a_b = 1e-6
  f_log_var_trainable = True

  use_noLabel_noisy_speech = False


class BasicNoisyDataset(BaseConfig):
  rawdata_type = 'clean_noisy'

  # _1_preprocess param # just for rawdata_type='clean_noisy'
  train_noisy_path = './noisy_datasets_8k/noisy_trainset_wav'
  train_clean_path = './noisy_datasets_8k/clean_trainset_wav'
  test_noisy_path = './noisy_datasets_8k/noisy_testset_wav'
  test_clean_path = './noisy_datasets_8k/clean_testset_wav'

  n_train_set_records = 11572
  n_val_set_records = 824
  n_test_set_records = 824

  max_epoch = 120

class p40(BaseConfig):
  n_processor_gen_tfrecords = 56
  n_processor_tfdata = 8
  GPU_PARTION = 0.225
  root_dir = '/home/zhangwenbo5/lihongfeng/se-with-FTL'

class se_reMagMSE_noisyData(BasicNoisyDataset): # done 15123
  '''
  baseline noisy datasets
  '''
  GPU_PARTION = 0.45
  losses_position = ['not_transformed_losses']
  not_transformed_losses = ['loss_reMagMse']
  relative_loss_epsilon = 0.1
  # transformed_losses = ['FTloss_mag_mse']
  # FT_type = ["LogValueT"]
  # weighted_FTL_by_DLoss = False
  # add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

class se_reMagMSE_simulateData(BaseConfig): # done 15123
  '''
  reMagMSE
  '''
  GPU_PARTION = 0.45
  losses_position = ['not_transformed_losses']
  not_transformed_losses = ['loss_reMagMse']
  relative_loss_epsilon = 0.1
  # transformed_losses = ['FTloss_mag_mse']
  # FT_type = ["LogValueT"]
  # weighted_FTL_by_DLoss = False
  # add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

class se_MagMSE(p40): # done p40
  '''
  baseline
  '''
  GPU_PARTION = 0.45
  losses_position = ['not_transformed_losses']
  not_transformed_losses = ['loss_mag_mse']
  # transformed_losses = ['FTloss_mag_mse']
  # FT_type = ["LogValueT"]
  # weighted_FTL_by_DLoss = False
  # add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

class se_MagMSE_RMS_001(p40): # done p40
  '''
  baseline usr RMSProp optimizer
  '''
  GPU_PARTION = 0.45
  losses_position = ['not_transformed_losses']
  not_transformed_losses = ['loss_mag_mse']

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  optimizer = "RMSProp"

class se_FTMagMSE_LogVT001(p40): # done p40
  '''
  LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']
  frame_level_D = True

class se_FTMagMSE_LogVT001_complexD(p40): # done p40
  '''
  LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']
  frame_level_D = True

class se_FTMagMSE_LogVT001_complexNotFrameD(p40): # done p40
  '''
  LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

class se_FTMagMSE_rawB(p40): # done p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  f_log_b = 0.00001

  LogFilter_type = 3 ####

class se_FTMagMSE_ulawBtimes100(p40): # done p40
  '''
  u-low LogVT 100times
  '''
  GPU_PARTION = 0.52
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 2 ####
  f_log_b = 0.0001 ####
  logFT_type2_btimes = 100.0 ####

class se_FTMagMSE_ulawBtimes1000(p40): # running p40
  '''
  u-low LogVT 1000times
  '''
  GPU_PARTION = 0.52
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 2 ####
  f_log_b = 0.00001 ####
  logFT_type2_btimes = 1000.0 ####

class se_FTMagMSE_ulaw(p40): # done p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####

class se_FTMagMSE_ulaw_RMS_001(p40): # done p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1
  optimizer = "RMSProp"

class se_FTMagMSE_100Gulaw(p40): # done p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####
  feature_transformer_grad_coef = 100.0

class se_FTMagMSE_1000Gulaw(p40): # done p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####
  feature_transformer_grad_coef = 1000.0

class se_MagMSE_1000Lulaw_FTin(BaseConfig): # done 15043
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.95
  losses_position = ['not_transformed_losses', 'd_loss'] ####
  not_transformed_losses = ['loss_mag_mse'] ####
  # transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = True ####

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####
  feature_transformer_grad_coef = 1.0
  D_loss_coef = 1000.0

class se_FTMagMSE_1000Lulaw(p40): # done p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####
  feature_transformer_grad_coef = 1.0
  D_loss_coef = 1000.0

class se_FTMagMSE_1000Lulaw_con(p40): # running p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####
  f_log_b = 9.0
  feature_transformer_grad_coef = 1.0
  D_loss_coef = 1000.0

class se_FTMagMSE_1000LfixUlaw(p40): # running p40
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1 ####
  f_log_b = 9.0
  feature_transformer_grad_coef = 0.0
  D_loss_coef = 1000.0

class se_FTMagMSE_1000Lulaw_FTin(BaseConfig): # done 15043
  '''
  u-low LogVT
  '''
  GPU_PARTION = 0.95
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = True ####

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1
  feature_transformer_grad_coef = 1.0
  D_loss_coef = 1000.0

class se_FTMagMSE_100Gulaw_FTin(p40): # done p40
  '''
  u-low-m LogVT
  '''
  GPU_PARTION = 0.45
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = True ####

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

  LogFilter_type = 1
  feature_transformer_grad_coef = 100.0

class se_FTMagRL0_020_100Gulaw_FTin(p40): # done p40
  '''
  u-low-m LogVT
  '''
  GPU_PARTION = 0.3
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_RL'] ####
  FT_type = ["LogValueT"]
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = True

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_RL', 'd_loss']

  LogFilter_type = 1
  relative_loss_epsilon = 0.02 ####
  feature_transformer_grad_coef = 100.0

class se_FTMagMSE_80MelFT(BaseConfig): # done 15043
  '''
  MelDenseT 80
  '''
  GPU_PARTION = 0.95
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["MelDenseT"] ###
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

class se_FTMagMSE_80fixMelFT(p40): # done p40
  '''
  MelDenseT 80 fixed
  '''
  GPU_PARTION = 0.95
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["MelDenseT"] ###
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']
  melDenseT_trainable = False

class se_FTMagMSE_ulaw_80fixMelFT(p40): # done p40
  '''
  ulawFT + MelDenseT_80_fixed
  '''
  GPU_PARTION = 0.46
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["LogValueT", "MelDenseT"] ###
  LogFilter_type = 1
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']
  melDenseT_trainable = False

class se_FTMagMSE_129MelFT(BaseConfig): # done 15043
  '''
  MelDenseT 129
  '''
  GPU_PARTION = 0.95
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["MelDenseT"] ###
  MelDenseT_n_mel = 129
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

class se_FTMagMSE_RDenseFT(p40): # done p40
  '''
  RandomDenseT
  '''
  GPU_PARTION = 0.47
  losses_position = ['transformed_losses', 'd_loss']
  # not_transformed_losses = ['loss_mag_mse']
  transformed_losses = ['FTloss_mag_mse']
  FT_type = ["RandomDenseT"] ###
  weighted_FTL_by_DLoss = False
  add_FeatureTrans_in_SE_inputs = False

  stop_criterion_losses = ['loss_mag_mse']
  show_losses = ['loss_mag_mse', 'FTloss_mag_mse', 'd_loss']

PARAM = se_FTMagMSE_ulawBtimes1000

# CUDA_VISIBLE_DEVICES=2 OMP_NUM_THREADS=4 python -m xxx._2_train
