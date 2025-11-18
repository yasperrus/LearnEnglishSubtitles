import chardet


class FileReader:
    text: str = ""

    def __init__(self, uri: str):
        self.uri = uri
        self.text = self.get_text()

    # def __iter__(self):
    #     return self.text
    #
    # def __len__(self):
    #     return len(self.text)
    #
    # def __getitem__(self, index):
    #     return self.text[index]

    def get_text(self) -> str:
        with open(self.uri, "r", encoding=self.__detect()["encoding"]) as f:
            return f.read()

    def __detect(self):
        with open(self.uri, "rb") as f:
            return chardet.detect(f.read())


def test_run():
    uri = "/home/chris/Videos/English/The big bang theory/Season 1/Episode 3/TheBigBangTheoryS1E3.vtt"
    text = FileReader(uri).text
    print(text)


if __name__ == "__main__":
    test_run()
