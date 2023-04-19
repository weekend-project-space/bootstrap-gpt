# import re
from jinja2 import Template

# def render(template, context):
#     template_vars = re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", template)
#     temp = template
#     for var in template_vars:
#         if var in context:
#             temp = temp.replace("{{" + var + "}}", str(context[var]))
#         else:
#             temp = temp.replace("{{" + var + "}}", "")
#     return temp


def render(template, context):
    v = Template(template).render(context)
    # print(v)
    return v
