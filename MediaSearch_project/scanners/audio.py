from faster_whisper import WhisperModel

def scan(path, sr_model):
    model = WhisperModel(sr_model, device='cpu')
    segments, info = model.transcribe(path)

    output = []

    for segment in segments:
        output.append((f"[{segment.start:.2f}s -> {segment.end:.2f}s]", segment.text))

    return output