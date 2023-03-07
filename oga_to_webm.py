import soundfile as sf

def convert(oga_file, wave_file):
    data, samplerate = sf.read(oga_file)
    sf.write(wave_file, data, samplerate)