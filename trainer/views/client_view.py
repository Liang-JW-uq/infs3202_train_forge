from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from orm.models import Client, UserTrainer
from ..forms import ClientForm

# logged_in_trainer = 1

# These path start from trainer/templates/...
def client_list(request):

    request.session["module"] = 'clients'

    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)

    search = request.GET.get('search', '')
    # We MUST order by something, otherwise will screw up paginator ordering when swapping pages
    if search:
        # icontains to ignore char case
        clients = Client.objects.filter(trainer=userTrainer, name__icontains=search).order_by('name')
    else:     
        clients = Client.objects.filter(trainer=userTrainer).order_by('name')

    # tags = Tag.objects.filter(trainer=userTrainer)
    clients =  clients.annotate(workout_count = Count('workouts'))


    # page controls - paginators with model data - 4 rows per page
    paginator = Paginator(clients, 6)
    page_number = request.GET.get('page')
    try:
        pager = paginator.get_page(page_number)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        pager = paginator.page(paginator.num_pages)

    return render(request, 'trainer/clients/client_list.html', {'clients': pager, 'search': search, 'page_obj': pager})


def client_add(request):

    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                # form.save()
                client = form.save(commit=False)
                client.trainer = userTrainer
                client.save()
                messages.success(request, "Client Saved!")
                return redirect("client_list")
            except ValidationError as e:
                form.add_error(None, str(e))
            except Exception as e:
                messages.error(request, f"Exceptions: {str(e)}")
    else:
        form = ClientForm()

    return render(request, "trainer/clients/client_add.html", {"form": form})

def client_edit(request, pk):
    
    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    client = Client.objects.get(id=pk, trainer=userTrainer)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            # form.save()
            client = form.save(commit=False)
            client.trainer = userTrainer
            client.save()
            messages.success(request, "Client Saved!")
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)

    return render(request, "trainer/clients/client_edit.html", {"form": form})

def client_delete(request, pk):
    
    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    # clients = Client.objects.filter(trainer__id=logged_in_trainer)

    # clients = Client.objects.get(id=pk, trainer=trainer)  <-- Alternate way to only get first item instead of array
    client = Client.objects.filter(id=pk, trainer=userTrainer).first()

    if request.method == "POST":
        client.delete()

        messages.success(request, "Client has been successfully deleted!")
        return redirect("client_list")

    return render(request, "trainer/clients/client_delete.html", {"client": client})


# def get_client_info(request, pk):
def get_client_info(request):
    trainer = get_object_or_404(UserTrainer, id=request.user.id)
    client_id = request.GET.get('client')
    client = Client.objects.get(id=client_id, trainer=trainer)
    client_info = {"id": client.id, "goals": client.goals, 'age': client.age, 'weight': client.weight, 'height': client.height}

    # id = client_info['id']
    # id = client_info.get('id')

    # return JsonResponse(client_info, safe=False)    
    return render(request, 'trainer/partials/_client_partial.html', {'client': client_info})