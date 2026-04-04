from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from orm.models import Client, Trainer
from ..forms import ClientForm

logged_in_trainer = 1

# These path start from trainer/templates/...
def client_list(request):
    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    # clients = Client.objects.filter(trainer__id=logged_in_trainer)
    clients = Client.objects.filter(trainer=trainer)
    
    return render(request, "trainer/client/client_list.html", {"clients": clients})

def client_add(request):

    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # form.save()
            client = form.save(commit=False)
            client.trainer = trainer
            client.save()
            messages.success(request, "Client Saved!")
    else:
        form = ClientForm()

    return render(request, "trainer/client/client_add.html", {"form": form})

def client_edit(request, pk):
    
    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    client = Client.objects.get(id=pk, trainer=trainer)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            # form.save()
            client = form.save(commit=False)
            client.trainer = trainer
            client.save()
            messages.success(request, "Client Saved!")
    else:
        form = ClientForm(instance=client)

    return render(request, "trainer/client/client_edit.html", {"form": form})

def client_delete(request, pk):
    
    trainer = get_object_or_404(Trainer, pk=logged_in_trainer)
    # clients = Client.objects.filter(trainer__id=logged_in_trainer)

    # clients = Client.objects.get(id=pk, trainer=trainer)  <-- Alternate way to only get first item instead of array
    client = Client.objects.filter(id=pk, trainer=trainer).first()
    print(client)

    if request.method == "POST":
        client.delete()

        messages.success(request, "Client has been successfully deleted!")
        return redirect("client_list")

    return render(request, "trainer/client/client_delete.html", {"client": client})