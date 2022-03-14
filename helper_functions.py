import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager


def print_section_info(input_array):
    print(f"Section contains {len(input_array)} runes.")


def calculate_ioc(input_array):
    _, counts = np.unique(input_array, return_counts=True)
    ioc = 0

    for counted in counts:
        ioc += counted * (counted - 1)
    ioc = ioc / (len(input_array) * (len(input_array) - 1) / 29)

    print(ioc)


def count_doublets(input_array):
    number_of_doublets = np.sum(input_array[0:-1] == input_array[1::])
    print(f"Number of doublets: {number_of_doublets}")
    print(f"Doublets rate: {number_of_doublets / (len(input_array) - 1) * 100}%")


def plot_bigrams(input_array, axis_option=None, fullscreen=None):
    matplotlib.rcParams['font.family'] = "Segoe UI Historic"

    bigram_table = np.zeros((29, 29), dtype=np.int32)
    for index in range(len(input_array) - 1):
        bigram_table[input_array[index], input_array[index + 1]] += 1

    fig, ax = plt.subplots()
    ax.matshow(bigram_table, cmap=plt.cm.jet)

    sx = ax.secondary_xaxis('bottom')
    sy = ax.secondary_yaxis('right')

    ax.set_xticks(np.arange(29))
    ax.set_yticks(np.arange(29))
    sx.set_xticks(np.arange(29))
    sy.set_yticks(np.arange(29))

    ax.set_xticklabels(latin_ticks())
    ax.set_yticklabels(latin_ticks())

    if axis_option == 'runes':
        sx.set_xticklabels(rune_ticks())
        sy.set_yticklabels(rune_ticks())

    for i in range(29):
        for j in range(29):
            c = bigram_table[j, i]
            ax.text(i, j, str(c), va='center', ha='center')

    if fullscreen:
        plot_fullscreen()

    plt.show()


def plot_letter_frequency(input_array, axis_option=None):
    matplotlib.rcParams['font.family'] = "Segoe UI Historic"

    _, counts = np.unique(input_array, return_counts=True)
    if len(counts) != 29:
        counts = np.zeros(29)
        for number in range(29):
            counts[number] = np.sum(input_array == number)
    fig, ax = plt.subplots()
    plt.plot(np.arange(29), counts)
    ax.set_xticks(np.arange(29))
    ax.set_xlim(left=0, right=28)

    if axis_option == 'runes':
        ax.set_xticklabels(rune_ticks())
    if axis_option == 'latin':
        ax.set_xticklabels(latin_ticks())

    plt.tight_layout()
    plt.show()


def latin_ticks():
    return ['F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'ING', 'OE',
            'D', 'A', 'AE', 'Y', 'IA', 'EA']


def rune_ticks():
    return ['ᚠ', 'ᚢ', 'ᚦ', 'ᚩ', 'ᚱ', 'v', 'ᚷ', 'ᚹ', 'ᚻ', 'ᚾ', 'ᛁ', 'ᛄ', 'ᛇ', 'ᛈ', 'ᛉ', 'ᛋ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛝ', 'ᛟ', 'ᛞ',
            'ᚪ', 'ᚫ', 'ᚣ', 'ᛡ', 'ᛠ ']


def plot_fullscreen():
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()


def convert_text_to_index(input_text):
    latin_fragments = ['F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'ING',
                       'OE',
                       'D', 'A', 'AE', 'Y', 'IA', 'EA']

    e2p = {}
    for i in range(0, 29):
        e2p[latin_fragments[i]] = i
    e2p["IO"] = e2p["IA"]
    e2p["K"] = e2p["C"]
    e2p["NG"] = e2p["ING"]
    e2p["Z"] = e2p["S"]
    e2p["Q"] = e2p["C"]
    e2p["V"] = e2p["U"]

    input_text = input_text.upper().replace("QU", "KW")
    input_text = input_text.replace("Q", "K")

    text_as_index = []
    skip = 0
    for index, value in enumerate(input_text):
        if skip:
            skip -= 1
            continue
        if input_text[index:index + 3] in e2p:
            text_as_index.append(e2p[input_text[index:index + 3]])
            skip = 2
            continue
        elif input_text[index:index + 2] in e2p:
            text_as_index.append(e2p[input_text[index:index + 2]])
            skip = 1
        else:
            text_as_index.append(e2p[input_text[index]])
    return np.asarray(text_as_index)
