class Files:
    def read(name):
        file = open("sentences.txt", "r")
        lines = file.readlines()
        file.close()
        return lines

print(Files.read("bob"))
