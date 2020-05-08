from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from accounts.models import Account
from inventory.models import Apparatus, Facility, Laboratory
from inventory.views import get_occupied_facilities
from .forms import FacilityApplicationForm, ResearchApplicationForm
from .models import FacilityApplication, ResearchApplication


@login_required(login_url=reverse_lazy('login'))
def my_list(request):
    fal = FacilityApplication.objects.filter(applicant=request.user)
    ral = ResearchApplication.objects.filter(applicant=request.user)
    apparatus_ids = [apparatus.id for apparatus in Apparatus.objects.all()]

    context = {}
    for fa in fal:
        context[fa] = {'apparatus_list': [], 'lab_list': []}
        for f in fa.items.all():
            if f.id in apparatus_ids:
                context[fa]['apparatus_list'].append(Apparatus.objects.get(id=f.id))
            else:
                context[fa]['lab_list'].append(Laboratory.objects.get(id=f.id))

    return render(request, 'applications/my-list.html', {
        'facility_application_list': fal,
        'research_application_list': ral,
        'context'                  : context,
        'user_quota'               : get_user_quota(request.user),
    })


@login_required(login_url=reverse_lazy('login'))
def ajax_application_switcher(request):
    action = request.GET.get('action')

    if action == 'CREATE':
        return create(request)
    elif action == 'APPLY':
        return apply(request)
    elif action == 'UPDATE':
        return update(request)
    elif action == 'WITHDRAW':
        return withdraw(request)
    elif action == 'DELETE':
        return delete(request)


def create(request):
    replies = {
        'message'   : 'PLEASE CHECK YOUR INPUTS',
        'is_success': False,
    }

    if request.GET.get('type') == 'FACILITY':
        form = FacilityApplicationForm(request.GET)
    else:
        form = ResearchApplicationForm(request.GET)

    if form.is_valid():
        app = form.save(commit=False)
        app.applicant = request.user
        app.save()
        replies['message'] = 'APPLICATION CREATED'
        replies['is_success'] = True

    return JsonResponse(replies)


def apply(request):
    # there is no extra condition for applying a research
    if request.GET.get('type') == 'RESEARCH':
        ra = ResearchApplication.objects.get(id=request.GET.get('id'))
        ra.applied_at = datetime.today()
        ra.status = 'APP'
        ra.save()
        return JsonResponse({'is_success': True})

    # it's much complex for the logic of borrowing facility
    replies = {
        'message'   : '',
        'is_success': False,
        'id'        : request.GET.get('id'),
    }
    fa = FacilityApplication.objects.get(id=request.GET.get('id'))
    item_count = fa.items.count()
    quota = get_user_quota(request.user)
    occupied_facilities = get_occupied_facilities()
    apparatus_ids = set([a.id for a in Apparatus.objects.all()])

    if item_count < 1:
        replies['message'] = 'Apply for WHAT exactly?'

    elif item_count > quota:
        replies['message'] = 'You can only apply additional ' + str(quota) + ' facilities!'

    elif item_count == 1:
        if fa.items.first() in occupied_facilities:
            replies['message'] = 'This facility is unavailable right now'
        else:
            replies['is_success'] = True

    else:
        # Facilities that are managed by different
        # staffs can't be applied together
        management, unavailable = {}, []
        for f in fa.items.all():
            if f in occupied_facilities:
                unavailable.append(f)

            if f.staff in management.keys():
                management[f.staff].append(f)
            else:
                management[f.staff] = [f]

        for f in unavailable:
            if f.id in apparatus_ids:
                replies['message'] += str(Apparatus.objects.get(id=f.id))
            else:
                replies['message'] += str(Laboratory.objects.get(id=f.id))
            replies['message'] += ' is unavailable! //'

        if len(management) > 1:
            for lst in management.values():
                replies['message'] += '['
                for f in lst:
                    if f.id in apparatus_ids:
                        replies['message'] += str(Apparatus.objects.get(id=f.id)) + ', '
                    else:
                        replies['message'] += str(Laboratory.objects.get(id=f.id)) + ', '
                replies['message'] += '] // '
            replies['message'] += ' need to be applied separately!'

        if len(unavailable) == 0 and len(management) == 1:
            replies['is_success'] = True

    if replies['is_success']:
        fa.applied_at = datetime.today()
        fa.status = 'APP'
        fa.save()
    return JsonResponse(replies)


def update(request):
    data = request.GET
    app = get_application_by_id(data.get('type'), data.get('id'))

    if data.get('type') == 'FACILITY':
        if len(data.get('alias')) > 0:
            app.alias = data.get('alias')
    else:
        if len(data.get('title')) > 0:
            app.title = data.get('title')

    if app.status == 'PEN':
        start, end, reason = data.get('start'), data.get('end'), data.get('reason')

        if len(start) > 0 and start > str(datetime.today().date()):
            app.start = start
        if len(end) > 0 and end > str(datetime.today().date()) and end > str(app.start):
            app.end = end
        if reason != app.reason:
            app.reason = reason

    app.save()
    return JsonResponse({'id': app.id, 'is_success': True})


def withdraw(request):
    app = get_application_by_id(request.GET.get('type'),
                                request.GET.get('id'))
    app.applied_at = None
    app.status = 'PEN'
    app.save()

    return JsonResponse({'is_success': True})


def delete(request):
    get_application_by_id(request.GET.get('type'),
                          request.GET.get('id')).delete()

    return JsonResponse({'is_success': True})


def get_user_quota(user):
    fal = FacilityApplication.objects.filter(applicant=user).filter(
        status__in=['APP', 'WAI', 'BOR', 'OVE'])
    borrow_limit = Account.objects.get(id=user.id).limit
    current_count = sum([fa.items.count() for fa in fal])

    return borrow_limit - current_count


def get_application_by_id(app_type, app_id):
    if app_type == 'FACILITY':
        return FacilityApplication.objects.get(id=app_id)
    else:
        return ResearchApplication.objects.get(id=app_id)


# Remove a facility from 'items' field of an facility
# application list whose status is PENDING
@login_required(login_url=reverse_lazy('login'))
def remove_facility_from_list(request):
    f = Facility.objects.get(id=request.GET.get('facility_id'))
    fa = FacilityApplication.objects.get(id=request.GET.get('facility_app_id'))

    if f and fa:
        if fa.status == 'PEN' and (f in fa.items.all()):
            fa.items.remove(f)
            fa.save()
            return JsonResponse({'is_success': True})

    return JsonResponse({'is_success': False})


@login_required(login_url=reverse_lazy('login'))
def ajax_account_switcher(request):
    action = request.GET.get('action')

    if action == 'SEARCH':
        return search_account(request)
    elif action == 'ADD':
        return add_account(request)
    elif action == 'REMOVE':
        return remove_account(request)


# Search account based on name/email/campus_id field
def search_account(request):
    text = request.GET.get('text')
    researchAppID = request.GET.get('id')
    matchedQS, matchedAccounts = set(), set()

    existed_user_ids = [user.id for user in ResearchApplication.objects \
        .get(id=researchAppID).members.all()]
    accounts = Account.objects.filter(
        is_verified=True
    ).filter(
        role__in=['TEA', 'STU']
    ).exclude(
        id__in=existed_user_ids
    )

    matchedQS.add(accounts.filter(name__contains=text))
    matchedQS.add(accounts.filter(email__contains=text))
    matchedQS.add(accounts.filter(campus_id__contains=text))

    for qs in matchedQS:
        for account in qs:
            matchedAccounts.add(account)

    data = serializers.serialize('json', matchedAccounts)
    return HttpResponse(data, content_type='application/json')


# Add a user to 'members' field of an research
# application list whose status is PENDING
def add_account(request):
    a = Account.objects.get(id=request.GET.get('account_id'))
    ra = ResearchApplication.objects.get(id=request.GET.get('id'))

    if a and ra:
        if ra.status == 'PEN' and (a not in ra.members.all()):
            ra.members.add(a)
            ra.save()
            return JsonResponse({'is_success': True})

    return JsonResponse({'is_success': False})


# Remove a user from 'members' field of an research
# application list whose status is PENDING
def remove_account(request):
    a = Account.objects.get(id=request.GET.get('account_id'))
    ra = ResearchApplication.objects.get(id=request.GET.get('id'))

    if a and ra:
        if ra.status == 'PEN' and (a in ra.members.all()):
            ra.members.remove(a)
            ra.save()
            return JsonResponse({'is_success': True})

    return JsonResponse({'is_success': False})
