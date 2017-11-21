from django import template

register = template.Library()


@register.filter
def get_nav_links(profiles):
    letters = list(set([x.last_name[0] for x in profiles]))
    letters.sort()
    links = ['<a class="scrolly" href="#' + x + '"">' + x + '</a> - ' for x in letters]
    ret = '\n'.join(links)[:-3]
    return ret