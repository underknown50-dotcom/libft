/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 13:51:47 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/04 14:02:36 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stddef.h>

size_t	ft_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

size_t	ft_strlcat(char *dst. const char *src, size_t dstsize)
{
	size_t	dstlen;
	size_t	src_len;
	size_t	i;

	i = 0;
	while (dst_len < dstsize && dst[dst_len])
		dst_len++;
	if (dst_len == dstsize)
		return (dstsize + src_len);
	while (dst_len + i + 1 < dstsize && src[i])
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[dst_len + i] = '\0';
	return (dst_len + src_len);
}

int	main(void)
{
	char	dst[12];
	size_t	ret;

	dst[0] = 'H';
	dst[1] = 'i';
	dst[2] = ' ';
	dst[3] = '\0';
	ret = ft_strlcat(dst, "there!", 12);
	printf("dst = %s\n", dst);
	printf("return = %zu\n", ret);
	return (0);
}
