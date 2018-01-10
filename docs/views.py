from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from docs.models import *
import pyperclip
import json


__all__ = [
    'index', 'ngs', 'ajax_test_docs', 'training', 'ajax_copy', 'general'
]


def index(request):
    return render(
        request,
        'docs/index.html'
    )


def ngs(request):
    """Create dictionary from NGS tests and parse into json for tree display in template."""

    test_dict = {
        "name": "NGS",
        "parent": "null",
        "children": []
    }

    tests = Test.objects.filter(
        chemistry_id__category_id__name='NGS'
    ).order_by(
        'chemistry_id__name',
        'name'
    )

    for t in tests:

        chemistries = [dictionary["name"] for dictionary in test_dict["children"]]

        if str(t.chemistry_id.name) in chemistries:
            for dictionary in test_dict["children"]:
                if dictionary["name"] == t.chemistry_id.name:
                    dictionary["children"].append(
                        {"name": str(t.name), "parent": str(t.chemistry_id.name)}
                    )

        else:

            test_dict["children"].append(
                {"name": str(t.chemistry_id.name), "parent": "NGS", "children": [
                    {"name": str(t.name), "parent": str(t.chemistry_id.name)}
                ]}
            )

    return render(
        request,
        'docs/ngs.html',
        {
            'test_data': json.dumps(test_dict)
        }
    )


def general(request):
    docs = Document.objects.filter(
        category_id__name='General'
    ).order_by(
        'type_id__type'
    )

    return render(
        request,
        'docs/general.html',
        {
            'docs': docs
        }
    )


def training(request):
    """Organise by employee then competency title. Create dictionary so employees which have not completed competencies
    completed by others can be filled in as None and highlighted in the template."""

    competencies = CompetencyDocument.objects.all().order_by(
        'competency_id__title',
        'employee_id__name'
    )

    return render(
        request,
        'docs/training.html',
        {
            'comps': competencies
        }
    )


def ajax_test_docs(request):
    """Ajax function: NGS documentation listed after user selects circle in tree diagram."""

    if request.is_ajax():

        selection = request.GET.get('name')

        docs = Document.objects.filter(
            (
                Q(category_id__name=selection) |
                Q(test_id__chemistry_id__name=selection) |
                Q(test_id__name=selection)
            ),
            Q(category_id__name='NGS')
        ).order_by(
            'test_id__chemistry_id__category_id__name',
            'test_id__chemistry_id__name',
            'test_id__name'
        )

        html = render_to_string(
            'docs/ajax_test_docs.html',
            {
                'docs': docs
            }
        )

        return HttpResponse(html)


def ajax_copy(request):
    """Ajax function: copy iPassPort code to clipboard."""

    if request.is_ajax():

        doc = request.GET.get('doc')

        if doc:
            pyperclip.copy(str(doc))
            msg = 'success'
        else:
            msg = 'fail'

        html = render_to_string(
            'docs/ajax_copy.html',
            {
                'msg': msg
            }
        )

        return HttpResponse(html)




