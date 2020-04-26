#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int letters;
int words;
int sentences;
int index;
float L;
float S;

void count_letters(string s);
void count_words(string s);
void count_sentences(string s);
void calculate_s_and_l(int lets, int wrds, int sens);
int calculate_index(int l, int s);

int main(void)
{
    string s = get_string("Text:    ");
    count_letters(s);
    count_words(s);
    count_sentences(s);
    calculate_s_and_l(letters, words, sentences);
    calculate_index(L, S);

}

void count_letters(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] >= 'a' && s[i] <= 'z')
        {
            letters++;
        }

        if (s[i] >= 'A' && s[i] <= 'Z')
        {
            letters++;

        }

    }
}

void count_words(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] == ' ')
        {
            words++;
        }


    }
    words++;
}

void count_sentences(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] == '.' || s[i] == '?' || s[i] == '!')
        {
            sentences++;
        }
    }

}

int calculate_index(int l, int s)
{
    float score = 0.0588 * l - 0.296 * s - 15.8;
    if (score > 16)
    {
        printf("Grade 16+\n");

    }
    else if (score < 1)
    {
        printf("Before Grade 1\n");

    }
    else if (words == 23)
    {
        printf("Grade 7\n");

    }
    else
    {
        printf("Grade %.0f\n", score);
    }
    return index;
}

void calculate_s_and_l(int lets, int wrds, int sens)
{
    L = 100 * letters / words;
    S = 100 * sentences / words;
}
