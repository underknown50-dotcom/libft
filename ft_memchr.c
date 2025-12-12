/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 12:35:26 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/04 13:21:32 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stddef.h>

void	*ft_memchr(const void *s, int c, size_t n)
{
	const unsigned char	*ptr;
	unsigned char		value;

	ptr = (const unsigned char *)s;
	value = (unsigned char )c;
	while (n--)
	{
		if (*ptr == value)
			return ((void *)ptr);
		ptr++;
	}
	return (0);
}

int	main(void)
{
	int	nums[5];
	int	target;
	int	*found;

	nums[0] = 10;
	nums[1] = 20;
	nums[2] = 30;
	nums[3] = 40;
	nums[4] = 50;
	target = 30;
	found = ft_memchr(nums, target, sizeof(nums));
	if (found != NULL)
		printf("Found: %d\n", *found);
	else
		printf("Not found\n");
	return (0);
}
