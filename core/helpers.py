import numpy as np
import torch
import torchaudio.functional as F_torchaudio
from scipy.signal import resample as scipy_resample
from core.config import SAMPLE_RATE, VAD_RMS_THRESHOLD

def is_speech(audio: np.ndarray, rms_threshold: float = VAD_RMS_THRESHOLD) -> bool:
    if audio.size == 0:
        return False
    return float(np.sqrt(np.mean(audio ** 2))) >= rms_threshold

def resample_audio_if_needed(audio_float: np.ndarray, orig_sr: int, target_sr: int = SAMPLE_RATE) -> np.ndarray:
    if orig_sr == target_sr:
        return audio_float
    tensor = torch.from_numpy(audio_float).float().unsqueeze(0)
    resampled = F_torchaudio.resample(tensor, orig_freq=int(orig_sr), new_freq=int(target_sr))
    return resampled.squeeze(0).numpy()

def trim_silence(audio: np.ndarray, threshold: float = 0.01) -> np.ndarray:
    idx = np.where(np.abs(audio) > threshold)[0]
    return audio[idx[0]: idx[-1] + 1] if idx.size else audio
