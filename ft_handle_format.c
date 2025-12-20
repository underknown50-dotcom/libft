/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_handle_format.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/16 06:29:49 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/16 06:29:50 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	handle_format_numbers(char c, va_list args)
{
	if (c == 'd' || c == 'i')
		return (ft_putnbr(va_arg(args, int)));
	if (c == 'u')
		return (ft_putnbr_unsigned(va_arg(args, unsigned int)));
	if (c == 'x')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789abcdef"));
	if (c == 'X')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789ABCDEF"));
	return (0);
}

static int	handle_format_others(char c, va_list args)
{
	if (c == 'c')
		return (ft_putchar(va_arg(args, int)));
	if (c == 's')
		return (ft_putstr(va_arg(args, char *)));
	if (c == '%')
		return (ft_putchar('%'));
	return (0);
}

int	ft_handle_format(char c, va_list args)
{
	int	count;

	count = 0;
	if (c == 'p')
	{
		count += write(1, "0x", 2);
		count += ft_puthex((unsigned long)va_arg(args, void *),
				"0123456789abcdef");
		return (count);
	}
	count += handle_format_numbers(c, args);
	count += handle_format_others(c, args);
	return (count);
}
