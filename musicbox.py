# musicbox.py
# 2019-13674
# 양현서
import sys
import wave
import struct
import math

# 점찍힌 음표의 길이
def dotsec(sec):
    return sec * 1.5

# div분음표의 길이
def sec(div):
    return secpone / div

# 콜론 뒤에 있는 음표길이 처리
def str2sec(st):
    hasdot = False
    if '.' in st:
        hasdot = True
        # st = st.replace('.','')     #not necessary?
    basesec = sec(float(st))
    if hasdot:
        return dotsec(basesec)
    return basesec

# sif == ras 같은 것 처리 가능한 음이름 -> midi base 번호 테이블
str2seqndic = {
    'do' : 0,
    're' : 2,
    'mi' : 4,
    'fa' : 5,
    'sol': 7,
    'ra' : 9,
    'si' : 11
}

# 'fas'에서 6 리턴
def str2seqn(st):
    if(st[0] == 'n'):
        return None
    delta = 0
    if st[-1] == 's':
        delta = 1
        st = st[:-1]
    elif st[-1] == 'f':
        delta = -1
        st = st[:-1]
    return str2seqndic[st] + delta

# 'fas5'에서 739.98..리턴
def str2freq(st):
    # https://stackoverflow.com/a/430665/8614565 - split num and text
    pitch = st.rstrip('0123456789')
    octave = int(st[len(pitch):])
    seqn = str2seqn(pitch)
    if seqn == None:
        return None
    midinum = seqn + (octave+1) * 12
    return 440 * 2**((midinum - 69)/12)


def tone(frequency, amplitude, duration):
    packed = bytearray(b'')
    n = int(duration * sampleRate)   # number of frames
    for i in range(n) :
        t = i / sampleRate
        y = int(volume * math.sin(2*math.pi * frequency * t))
        packed.extend(struct.pack('<h', int(y)))
    return packed

def Load(file):
    tempoline = file.readline()
    tempos = tempoline.split()
    #secpone = 60 * 4 / 120
    Result = []
    if tempos[0].lower() != "tempo":
        print("warning: no tempo specified")
    else:
        tlhs = float(tempos[1])
        trhs = float(tempos[3])
        secpone = 60 * tlhs/ trhs  # 4분음표를 1분에 120개 연주해라 -> 온음표를 1분에 120 /4개 연주해라 온음표하나의 초수이다.
    for line in file:
        notes = line.split()
        for note in notes:
            note = note.strip()
            note = note.lower()
            pit, div = note.split(':')
            freq = str2freq(pit) #: Number or None
            duration = str2sec(div)
            Result.append((freq,duration))
            #dat = tone(freq,10,duration)
            #outfile.writeframesraw(dat)
    file.close()
    return Result

# main

# amplitude = 0.5   # 0 to 1
# sampwidth = 2
# maxVolume = 2**(sampwidth*8 - 1) - 1
# volume = int(amplitude * maxVolume)

# infile = open(sys.argv[1], "r")
# outfile = wave.open(sys.argv[2], 'w')

# sampleRate = 8000
# outfile.setframerate(sampleRate)
# outfile.setnchannels(1)
# outfile.setsampwidth(sampwidth)

# tempoline = infile.readline()

# tempos = tempoline.split()
secpone = 60 * 4 / 120
# if tempos[0].lower() != "tempo":
#     print("warning: no tempo specified")
# else:
#     tlhs = float(tempos[1])
#     trhs = float(tempos[3])
#     secpone = 60 * tlhs/ trhs  # 4분음표를 1분에 120개 연주해라 -> 온음표를 1분에 120 /4개 연주해라 온음표하나의 초수이다.
# for line in infile:
#     notes = line.split()
#     for note in notes:
#         note = note.strip()
#         note = note.lower()
#         pit, div = note.split(':')
#         freq = str2freq(pit)
#         duration = str2sec(div)
#         dat = tone(freq,10,duration)
#         outfile.writeframesraw(dat)

# outfile.close()
# infile.close()