# Voice-over: Piper vi_VN-vais1000-medium (offline). Usage: python3 voiceover.py <model.onnx>
import sys, wave, numpy as np
from piper import PiperVoice, SynthesisConfig
# (start time in video, max seconds, text) — numbers & brand names spelled phonetically
LINES = [
 (0.6, 4.3, "Cơ hội vàng cho khách hàng sở hữu Vin hôm, với ưu đãi kép cực hấp dẫn!"),
 (5.3, 5.6, "Vâu chơ ba mươi phần trăm, cộng chiết khấu thanh toán sớm bảy phẩy năm phần trăm. Giảm tới ba mươi bảy phẩy năm phần trăm!"),
 (11.3, 5.0, "Vin hôm Sài Gòn Pác, Hóc Môn. Chính sách chiết khấu kỷ lục!"),
 (16.7, 6.2, "Một căn năm phẩy tám tỷ, tiết kiệm ngay hai phẩy một bảy lăm tỷ. Giá sở hữu chỉ còn ba phẩy sáu hai lăm tỷ!"),
 (23.3, 5.0, "Mức giá quá hời cho siêu đô thị có làng đại học và sân gôn ba mươi sáu lỗ!"),
 (28.8, 4.6, "Liên hệ ngay Em Bến: không tám sáu tám, năm năm sáu, bốn tám sáu."),
]
v = PiperVoice.load(sys.argv[1], config_path=sys.argv[1] + ".json")
sr = v.config.sample_rate
def synth(text, ls):
    cfg = SynthesisConfig(length_scale=ls, noise_scale=0.6, noise_w_scale=0.7)
    a = np.concatenate([np.frombuffer(c.audio_int16_bytes, np.int16) for c in v.synthesize(text, syn_config=cfg)])
    nz = np.where(np.abs(a) > 300)[0]
    return a[nz[0]:nz[-1] + 1] if len(nz) else a
track = np.zeros(int(34 * sr), np.float32)
for start, maxd, text in LINES:
    ls = 0.95
    a = synth(text, ls)
    while len(a) / sr > maxd and ls > 0.72:
        ls -= 0.03; a = synth(text, ls)
    print(f"{start:5.1f}s  {len(a)/sr:4.2f}/{maxd}s  speed={ls:.2f}  {text}")
    s = int(start * sr); track[s:s + len(a)] += a[:len(track) - s] / 32768
with wave.open("voice.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(track, -1, 1) * 32767).astype(np.int16).tobytes())
