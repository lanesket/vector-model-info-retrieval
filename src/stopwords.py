def get_stop_words(path: str):
    with open(path, "r") as file:
        words = [w.strip("\n") for w in file.readlines()]

    return words


if __name__ == "__main__":
    print(get_stop_words("../assets/stop-words.txt"))
    print(len(get_stop_words("../assets/stop-words.txt")))
