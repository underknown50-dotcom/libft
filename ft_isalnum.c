/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalnum.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 15:29:46 by mewaysi           #+#    #+#             */
/*   Updated: 2025/11/25 17:23:53 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_isalnum(int alphanumeric)
{
	if (alphanumeric >= 'a' && alphanumeric <= 'z')
		return (1);
	else if (alphanumeric >= 'A' && alphanumeric <= 'Z')
		return (1);
	else if (alphanumeric >= '1' && alphanumeric <= '9')
		return (1);
	else
		return (0);
}
/*
int main()
{
	printf("5 is a %d\n",ft_isalnum('5'));
	printf("b is a %d\n",ft_isalnum('b'));
	printf("B is a %d\n",ft_isalnum('B'));
	printf("= is a %d\n",ft_isalnum('='));
	printf("nothing is a %d\n",ft_isalnum(' '));
}
*/
