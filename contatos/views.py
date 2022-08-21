from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

def index(request):
    contatos = Contato.objects.order_by('nome').filter(
        mostrar = True
    )
    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'index.html', {
        'contatos': contatos
    })

def ver_contato(request, contato_id):
        contato = get_object_or_404(Contato, id=contato_id)

        if not contato.mostrar:
            raise Http404()

        return render(request, 'ver_contato.html', {
            'contato': contato
    })

def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        request, messages.ERROR, 'Campo não pode ficar vazio.'
        return redirect('index')
    
    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.order_by('-id').filter(
        Q(nome__icontains = termo) | Q(sobrenome__icontains = termo),
        mostrar = True
    )
    print(contatos.query)
    paginator = Paginator(contatos, 2)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'busca.html',{
        'contatos': contatos
    })