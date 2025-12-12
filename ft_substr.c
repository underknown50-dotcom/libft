/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 18:21:24 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/12 22:44:34 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

static char	*empty_sub(void)
{
	char	*str;

	str = (char *)malloc(1);
	if (!str)
		return (NULL);
	str[0] = '\0';
	return (str);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	i;
	size_t	s_len;
	char	*sub;

	if (!s)
		return (NULL);
	s_len = 0;
	while (s[s_len])
		s_len++;
	if (start >= s_len)
		return (empty_sub());
	if (len > s_len - start)
		len = s_len - start;
	sub = (char *)malloc(len + 1);
	if (!sub)
		return (NULL);
	i = 0;
	while (i < len)
	{
		sub[i] = s[start + i];
		i++;
	}
	sub[i] = '\0';
	return (sub);
}
/*int main(void)
{
    char *str = "Hello World!";
    char *sub;

    // Test 1
    sub = ft_substr(str, 0, 5);        // "Hello"
    printf("Test 1: %s\n", sub);
    free(sub);

    // Test 2
    sub = ft_substr(str, 6, 5);        // "World"
    printf("Test 2: %s\n", sub);
    free(sub);

    // Test 3
    sub = ft_substr(str, 20, 5);       // start > length => ""
    printf("Test 3: '%s'\n", sub);
    free(sub);

    // Test 4
    sub = ft_substr(str, 3, 50);       // len too big => "lo World!"
    printf("Test 4: %s\n", sub);
    free(sub);

    return 0;
}*/
