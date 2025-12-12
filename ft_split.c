#include <stdlib.h>
#include <stdio.h>

int is_sep(char c,char *charset)
{
    int i;

    i = 0;
    while (charset[i])
    {
        if (c == charset[i])
        {
            return (1);
        }
        i++;
    }
    return (0);
}
int count_words(char *str, char *charset)
{
    int i;
    int count;

    i = 0;
    count = 0;
    while (str[i])
    {
        while (str[i] && is_sep(str[i], charset))
        {
            i++;
        }
        if (str[i])
        {
            count++;
        }
        while (str[i] && !is_sep(str[i], charset))
        {
            i++;
        }
    }
    return (count);
}
char    *malloc_word(char *str,char charset)
{
    char    *word;
    int len;
    int i;

    i = 0;
    len = 0;
    while (str[len] && !is_sep(str[len], charset))
    {
        len++;
    }
    word = malloc(sizeof(char) * (len + 1));
    if (!word)
    {
        return NULL;
    }
    while (i < len)
    {
        word[i] = str[i];
        i++;
    }
    word[i] = '\0';
    return (word);
}
void    free_split(char **split,int count)
{
    int i;

    i = 0;
    while (i < count)
    {
        free(split[i])
        i++;
    }
    free(split);
}
char    **ft_split(char *str, char *charset)
{
    char    **split;
    int i;
    int j;
    int word;

    i = 0;
    j = 0;
    word = count_words(str.charset);
    split = malloc(sizeof(char *) * (word + 1));
    if (!split)
    {
        return NULL;
    }
    while (str[i] && j < word)
    {
        while (str[i] && is_sep(str[i], charset))
        {
            i++;
        }
        if (str[i])
        {
            split[j] = malloc_word(!str[i],charset)
            if (!split[j])
            {
                free_split(split, j);
                return (NULL);
            }
            j++;
        }
        while (str[i] && !is_sep(str[i], charset))
        {
            i++;
        }
    }
    split[j] = NULL;
    return (split);
}