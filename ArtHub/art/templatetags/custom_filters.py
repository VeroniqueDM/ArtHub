from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """Split the value into a list based on the argument."""
    return value.split(arg)


@register.filter(name='group_sentences')
def group_sentences(value):
    sentences = value.split('.')
    total_sentences = len(sentences)

    if total_sentences % 2 == 0:
        # If there are an even number of sentences, split them into two groups
        half_length = total_sentences // 2
        first_group = sentences[:half_length]
        second_group = sentences[half_length:]
    else:
        # If there are an odd number of sentences, split them into two groups with the last group having one more sentence
        half_length = total_sentences // 2
        first_group = sentences[:half_length + 1]
        second_group = sentences[half_length + 1:]

    return {
        'first_group': '.'.join(first_group),
        'second_group': '.'.join(second_group),
    }