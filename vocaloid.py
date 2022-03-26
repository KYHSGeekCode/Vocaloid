import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import matplotlib.pyplot as plt
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import musicbox
import sys
import io

#algorithm
# input : vocaloid lilypond_with_lytics.txt out.wav
# 1. parse file
# 2. 소리나는대로 옮기기
# 3. 각 음절마다 TTS 변환
# 4. 각 음절을 pitch shift

def get_pitch(snd, frate):
    arr = np.array(snd)
    ffted = np.fft.fft(arr)
    n = len(arr)
    timestep = 1/frate
    freq = np.fft.fftfreq(n, d= timestep)
    amps =[abs(amp) for amp in ffted]
    #plt.plot(freq,amps)
    #plt.show()
    maxa = amps[0]
    maxf = freq[0]
    for f, a in zip(freq,amps):
        if(f >=0):
            if(maxa < a):
                maxa = a
                maxf = f
    return maxf

""" def set_pitch(snd, frate, targetFreq):
    arr = np.array(snd)
    newarr = np.empty_like(arr)
    ffted = np.fft.fft(arr)
    n = len(arr)
    timestep = 1/frate
    freq = np.fft.fftfreq(n, d= timestep)
    amps =[abs(amp) for amp in ffted]
    #plt.plot(freq,amps)
    #plt.show()
    maxa = amps[0]
    maxf = freq[0]
    for f, a in zip(freq,amps):
        if(f >=0):
            if(maxa < a):
                maxa = a
                maxf = f
    deltaf = maxf - targetFreq
    #ffted의 내용: Amplitude 기준: 주파수
    # ffted[i] = ffted[i-deltaf]
    n
    for i, f in enumerate(freq):
        newf = f+ deltaf
        A = ffted[i]
        newarr += A*np.sin()
 """
def CreateOne(ch, freq, dur):
    if dur ==0:
        return None
    if freq == None:
        AudioSegment.silent(duration=dur * 1000)
    tts = gTTS(text=ch, lang='ko')
    #buf =
    tts.save('tmp.mp3')   
    #tts.write_to_fp(buf)
    sound = AudioSegment.from_file('tmp.mp3', format="mp3")
    #print(sound.frame_rate)     
    #print(sound.channels)
    print(ch)
    pitch = get_pitch(sound.get_array_of_samples(), sound.frame_rate)
    print(pitch)
    octaves = freq/pitch
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    newpitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    return newpitch_sound

def CreateTwo(ch, freq, dur):
    if dur ==0:
        return None
    if freq == None:
        AudioSegment.silent(duration=dur * 1000)
    tts = gTTS(text=ch, lang='ko')
    #buf =
    tts.save('tmp.mp3')   
    #tts.write_to_fp(buf)
    sound = AudioSegment.from_file('tmp.mp3', format="mp3")
    #print(sound.frame_rate)     
    #print(sound.channels)
    print(ch)
    pitch = get_pitch(sound.get_array_of_samples(), sound.frame_rate)
    print(pitch)
    octaves = freq/pitch
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    newpitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    return newpitch_sound


if len(sys.argv) <= 3:
    print("usage : melody lyrics output")
    exit(1)
melodyFilename = sys.argv[1]
lyricsfilename = sys.argv[2]
output = sys.argv[3]
notes = musicbox.Load(open(melodyFilename,'r'))
lyricsFile = open(lyricsfilename, 'r')
lyricChs = []
for line in lyricsFile:
    for ch in line.split():
        lyricChs.append(ch)
lyricsFile.close()
lyrit = 0
combined = AudioSegment.empty()
for note in enumerate(notes):
    freq = note[0]
    dur = note[1]
    ch = lyricChs[lyrit]
    if(dur is not 0):
        combined += CreateOne(ch,freq,dur)
    if(freq is not None):
        lyrit = lyrit+1
combined.export(output, format="mp3")

#sound = AudioSegment.from_file("good.mp3", format="mp3")
#play(sound)
#    pitch = get_pitch(sound.get_array_of_samples(), sound.frame_rate)
#https://stackoverflow.com/a/42567511/8614565
#sound.
# shift the pitch down by half an octave (speed will decrease proportionally)
# +1octave = *2
# freq가 440/pitch 배 되야 함
#   octaves = 440/pitch
#   new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
#   lowpitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
#Play pitch changed sound
#play(lowpitch_sound)
#    lowpitch_sound.export("la.mp3", format = "mp3")

