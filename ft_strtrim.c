/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 22:39:46 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/12 22:41:09 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

static int	to_trim(const char *set, char c)
{
	int	i;

	i = 0;
	while (set[i])
	{
		if (c == set[i])
			return (1);
		i++;
	}
	return (0);
}

static int	get_start(const char *s1, const char *set)
{
	int	start;

	start = 0;
	while (s1[start] && to_trim(set, s1[start]))
		start++;
	return (start);
}

static int	get_end(const char *s1, const char *set, int len)
{
	int	end;

	end = len - 1;
	while (end >= 0 && to_trim(set, s1[end]))
		end--;
	return (end);
}

static char	*empty_string(void)
{
	char	*str;

	str = (char *)malloc(1);
	if (!str)
		return (NULL);
	str[0] = '\0';
	return (str);
}

char	*ft_strtrim(const char *s1, const char *set)
{
	int		start;
	int		end;
	int		i;
	int		len;
	char	*trimmed;

	if (!s1 || !set)
		return (NULL);
	len = 0;
	while (s1[len])
		len++;
	start = get_start(s1, set);
	if (start >= len)
		return (empty_string());
	end = get_end(s1, set, len);
	trimmed = (char *)malloc(end - start + 2);
	if (!trimmed)
		return (NULL);
	i = 0;
	while (start <= end)
		trimmed[i++] = s1[start++];
	trimmed[i] = '\0';
	return (trimmed);
}
