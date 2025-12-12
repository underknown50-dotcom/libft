/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isdigit.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 14:53:02 by mewaysi           #+#    #+#             */
/*   Updated: 2025/11/25 17:14:34 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_isdigit(int Digit)
{
	if (Digit >= '0' && Digit <= '9')
		return (1);
	else
		return (0);
}

/*int main()
{
	printf("8 is a %d\n",ft_isdigit('8'));
	printf("g is a %d\n",ft_isdigit('g'));
	printf("= is a %d\n",ft_isdigit('='));
	printf("nothing is a %d\n",ft_isdigit(' '));
}
*/
