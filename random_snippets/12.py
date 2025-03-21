import datetime
import json
import os
import asyncio

from pydub import AudioSegment


def make_split_audio(source_audio_file: str, results: list, consultant_id: str, dialog_id: str, base_dir_to_save: str) -> str:
    """
    :param base_dir_to_save:
    :param source_audio_file:
    :param results:
    :param consultant_id:
    :param dialog_id:
    :return: str: path/to/splitted_audios
    """
    sorted_results = sorted(results, key=lambda d: d["begin"])

    continued = 0

    t1 = 0
    t2 = 0
    file_id = 1

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H_%M_%S")

    # make dir to save splitted audio
    os.makedirs(os.path.join(base_dir_to_save, "splitted_audio"))

    for i, result in enumerate(sorted_results):
        # print("speaker_id", result["speaker_id"])
        speaker_id = result["speaker_id"]

        if not continued:
            t1 = result["begin"]  # Works in milliseconds

        t2 = result["end"]  # * 1000
        step = 1
        while True:
            if i != len(sorted_results) - 1:
                try:
                    next_speaker = sorted_results[i + step]["speaker_id"]
                except IndexError:
                    break
            else:
                continued = 0
                break
            if next_speaker == speaker_id:
                continued = 1
                break
            else:
                continued = 0
                break
        if continued:
            continue
        new_audio = AudioSegment.from_wav(source_audio_file)
        new_audio = new_audio[t1:t2]
        print('t2 - t1 = ', t2 - t1)
        # logger.info(msg="Saving as {}.".format("{}".format(new_name)))
        audio_path = os.path.join(base_dir_to_save, "splitted_audio", f"{file_id}_{speaker_id}_{dialog_id}_{t1}_{t2}_{now}.wav")
        new_name = audio_path
        new_audio.export("{}".format(new_name), format="wav")

        if t2 - t1 < 3000:
            asyncio.run(add_mute(audio_path, mute_size=1))
            print(f'[INFO] {now} add 1 sec mute to both side')
        elif t2 - t1 < 2000:
            print(f'[INFO] {now} add 1.5 sec mute to both side')
            asyncio.run(add_mute(audio_path, mute_size=1.5))
        file_id += 1
        continued = 0

    splitted_audios_dir = os.path.join(base_dir_to_save, "splitted_audio")

    return splitted_audios_dir


def get_texts(source_audio_name: str):
    texts = []
    files = [(f, f.split("_")[1]) for f in os.listdir(os.path.join(os.getcwd(), "diariz-jsons2",
                                                                   source_audio_name.split("_")[2])) if f.endswith(".json") and not f.startswith("texts")]
    # print(files)

    files.sort(key=lambda b: int(b[1]))

    for f, n in files:
        if f.startswith("texts"):
            continue
        with open(os.path.join("diariz-jsons2", source_audio_name.split("_")[2], f), encoding="utf-8") as file:
            data = json.load(file)["text"]
            if data in texts:
                continue
            texts.append(data)

    source_audio_name = source_audio_name.split(".wav")[0]
    with open(fr"texts/texts_{source_audio_name.split('_')[2]}.json", "w", encoding="utf-8") as file:
        json.dump({"texts": texts}, file, ensure_ascii=False, indent=4)


async def add_mute(abs_path_to_audio: str, mute_size=1.5, one_side=False):
    print('mute abs_path_to_audio ', abs_path_to_audio)
    """
    :param mute_size
    size of mute audio. it may be 1 or 1.5
    """
    global mute
    if one_side:
        # добавление тишины с одной стороны
        return
    path = f'{os.path.join(os.getcwd())}/Tools/audios'
    if mute_size == 1:
        mute = AudioSegment.from_file(f'{path}/mute_1.wav', format='wav')
    elif mute_size == 1.5:
        mute = AudioSegment.from_file(f'{path}/mute_1_5.wav', format='wav')
    original_sound = AudioSegment.from_file(abs_path_to_audio, format='wav')

    combined = mute + original_sound + mute

    combined.export(abs_path_to_audio, format='wav')

    return 0
