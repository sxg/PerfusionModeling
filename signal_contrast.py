"""Interconverts signal to contrast."""

import numpy as np

def signal_to_contrast(signal, acquisition_data):
    """Convert signal intensity to contrast concentration."""
    alpha = np.asscalar(np.asscalar(acquisition_data["flipAngle"])) * np.pi / 180
    t10liver = np.asscalar(np.asscalar(acquisition_data["T10l"])) * 1000
    r10liver = 1 / t10liver
    rep_time = np.asscalar(np.asscalar(acquisition_data["TR"]))
    relaxivity = np.asscalar(np.asscalar(acquisition_data["relaxivity"]))
    start_frame = np.asscalar(np.asscalar(acquisition_data["startFrame"])) - 1
    add_frames = np.asscalar(np.asscalar(acquisition_data["addFrames"]))
    stop_frame = start_frame + add_frames + 1
    scale_factor = np.asscalar(np.asscalar(acquisition_data["scaleFactor"]))

    s0liver = np.mean(signal[start_frame:stop_frame]) \
        * (1 - np.exp(-r10liver * rep_time) * np.cos(alpha)) \
        / (1 - np.exp(-r10liver * rep_time)) / np.sin(alpha)
    r1liver = np.absolute(np.log(np.divide((s0liver * np.sin(alpha) \
        - np.multiply(signal, np.cos(alpha))) \
        , (s0liver * np.sin(alpha) - signal))) / rep_time)
    contrast = (r1liver - r10liver) * 1000 / relaxivity
    contrast *= scale_factor
    return contrast

def art_signal_to_contrast(acquisition_data):
    """Convert arterial signal intensity to contrast concentration."""
    allts = np.asscalar(acquisition_data["allts"])
    art_signal = np.abs(allts[:, 1])
    pv_signal = np.abs(allts[:, 2])
    alpha = np.asscalar(np.asscalar(acquisition_data["flipAngle"])) * np.pi / 180
    t10a = np.asscalar(np.asscalar(acquisition_data["T10b"])) * 1000
    r10a = 1 / t10a
    rep_time = np.asscalar(np.asscalar(acquisition_data["TR"]))
    relaxivity = np.asscalar(np.asscalar(acquisition_data["relaxivity"]))
    start_frame = np.asscalar(np.asscalar(acquisition_data["startFrame"])) - 1
    add_frames = np.asscalar(np.asscalar(acquisition_data["addFrames"]))
    stop_frame = start_frame + add_frames + 1
    hematocrit = 0.4

    s0a = np.mean(pv_signal[start_frame:stop_frame]) \
        * (1 - np.exp(-r10a * rep_time) * np.cos(alpha)) \
        / (1 - np.exp(-r10a * rep_time)) / np.sin(alpha)
    r1a = np.log(np.divide((s0a * np.sin(alpha) \
        - np.multiply(art_signal, np.cos(alpha))) \
        , (s0a * np.sin(alpha) - art_signal))) / rep_time
    art_contrast = (r1a - r10a) * 1000 / relaxivity
    art_contrast = art_contrast / (1 - hematocrit)
    return art_contrast

def pv_signal_to_contrast(acquisition_data):
    """Convert portal venous signal intensity to contrast concentration."""
    allts = np.asscalar(acquisition_data["allts"])
    pv_signal = np.abs(allts[:, 2])
    alpha = np.asscalar(np.asscalar(acquisition_data["flipAngle"])) * np.pi / 180
    t10pv = np.asscalar(np.asscalar(acquisition_data["T10p"])) * 1000
    r10pv = 1 / t10pv
    rep_time = np.asscalar(np.asscalar(acquisition_data["TR"]))
    relaxivity = np.asscalar(np.asscalar(acquisition_data["relaxivity"]))
    start_frame = np.asscalar(np.asscalar(acquisition_data["startFrame"])) - 1
    add_frames = np.asscalar(np.asscalar(acquisition_data["addFrames"]))
    stop_frame = start_frame + add_frames + 1
    hematocrit = 0.4

    s0pv = np.mean(pv_signal[start_frame:stop_frame]) \
        * (1 - np.exp(-r10pv * rep_time) * np.cos(alpha)) \
        / (1 - np.exp(-r10pv * rep_time)) / np.sin(alpha)
    r1pv = np.log(np.divide((s0pv * np.sin(alpha) \
        - np.multiply(pv_signal, np.cos(alpha))) \
        , (s0pv * np.sin(alpha) - pv_signal))) / rep_time
    art_contrast = (r1pv - r10pv) * 1000 / relaxivity
    art_contrast = art_contrast / (1 - hematocrit)
    return art_contrast
   