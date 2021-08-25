from django.shortcuts import render, redirect
from .models import Pregunta, Respuesta, Partida, Categoria
from datetime import datetime
from django.contrib.auth.decorators import login_required
#from .forms import PreguntaForm
from datetime import datetime
#from .models import PostForm
from django.shortcuts import redirect



# Create your views here.
@login_required(login_url='/login')
def listar_preguntas(request, identificador):
    if request.method == "POST":
        resultado = 0
        for i in range(1,4):
            opcion = Respuesta.objects.get(pk=request.POST[str(i)])
            resultado += opcion.puntaje
        Partida.objects.create(usuario=request.user, fecha=datetime.now, resultado= resultado)
        return redirect("/")
    else:
        data = {}
        preguntas = Pregunta.objects.filter(id_categoria_id=identificador).order_by('?')[:3]
        for item in preguntas:
            respuestas = Respuesta.objects.filter(id_pregunta=item.id)
            categorias = Categoria.objects.get(pk=item.id_categoria.id)
            data[item.pregunta]= {"opciones":respuestas, "categoria":categorias}
        return render(request, 'juego/listar_preguntas.html', {"pregunta":preguntas, "data":data})



def crear_pregunta(request):
    if request.method == "juego":
        form = PreguntaForm(request.JUEGO)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.fecha_creacion = datetime.now()
            registro.save()
    form = PreguntaForm()
    return render(request, 'juego/crear_pregunta.html', {'form': form})

def paginafinal(request):
    return render(request, 'juego/paginafinal.html')

def seleccionarcategorias(request):
    categoria=Categoria.objects.all()
    return render(request, 'juego/seleccionarcategorias.html', {"categoria": categoria})



