from cs50 import get_string


def main():
    letters = 0
    sentences = 0
    words = 0
    LL = 0
    SS = 0
    s = get_string("Text:   ")

    for i in s:
        if i == " ":
            words += 1
    words += 1

    for i in s:
        if i.isalpha():
            letters = letters + 1

    for i in s:
        if i == '.' or i == '!' or i == '?':
            sentences += 1

    LL = 100 * (letters / words)
    SS = 100 * (sentences / words)

    score = round((0.0588 * LL) - (0.296 * SS) - 15.8)

    if score > 16:
        print("Grade 16+")

    if score < 1:
        print("Before Grade 1")

    else:
        print(f"Grade {score}")


main()