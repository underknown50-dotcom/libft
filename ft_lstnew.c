typedef struct s_list
{
void *content;
struct s_list *next;
} t_list;

t_list  *ft_lstnew(voidd *content)
{
    t_list  *elem;

    if (!elem)
    {
        return (NULL);
    }
    elem->content = content;
    elem->next = NULL;
    return (elem);
}