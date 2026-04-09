from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from orm.models import Client, UserTrainer
from ..forms import ClientForm

# logged_in_trainer = 1

# These path start from trainer/templates/...
def client_list(request):

    request.session["module"] = 'clients'

    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    # clients = Client.objects.filter(trainer__id=logged_in_trainer)
    clients = Client.objects.filter(trainer=userTrainer)
    
    return render(request, "trainer/client/client_list.html", {"clients": clients})

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

    return render(request, "trainer/client/client_add.html", {"form": form})

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

    return render(request, "trainer/client/client_edit.html", {"form": form})

def client_delete(request, pk):
    
    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    # clients = Client.objects.filter(trainer__id=logged_in_trainer)

    # clients = Client.objects.get(id=pk, trainer=trainer)  <-- Alternate way to only get first item instead of array
    client = Client.objects.filter(id=pk, trainer=userTrainer).first()

    if request.method == "POST":
        client.delete()

        messages.success(request, "Client has been successfully deleted!")
        return redirect("client_list")

    return render(request, "trainer/client/client_delete.html", {"client": client})