# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm          # Register

def index_page(request):
    """
    Una funcion simple que envia a renderizar la pagina
    de inicio.
    """
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    """
    Una funcion simple que se encarga de enviar a renderizar
    las imagenes en forma de tarjetas. Tambien envia informacion
    sobre los favoritos del usuario para renderizar el botón
    correspondiente.
    """
    images = services.getAllImages()
    favourite_list = []

    for img_card in services.getAllFavourites(request):
        favourite_list.append(img_card.name)
    
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    """
    Una funcion simple que recibe como argumento una peticion http con
    informacion del nombre que el usuario esta buscando. Realiza la
    busqueda y envia a renderizar las tarjetas resultantes de la busqueda.
    Tambien envia informacion de los favoritos para que se renderice
    correctamente el boton favoritos.
    """
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = services.filterByCharacter(name)
        favourite_list = []

        for img_card in services.getAllFavourites(request):
            favourite_list.append(img_card.name)                # lista los nombres de pokemon en favoritos
        
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    """
    Una funcion simple que recibe como argumento una peticion http con
    informacion del tipo que el usuario esta buscando. Realiza la
    busqueda y envia a renderizar las tarjetas resultantes de la busqueda.
    Tambien envia informacion de los favoritos para que se renderice
    correctamente el boton favoritos.
    """
    type = request.POST.get('type', '')
    print(type)

    if type != '':
        images = []                                             # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        for img_card in services.getAllFavourites(request):
            favourite_list.append(img_card.name)                # lista los nombres de pokemon en favoritos

        for img_card in services.getAllImages():                # un bucle que filtra las imagenes por tipo
            if type in img_card.types:
                images.append(img_card)
        
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')
    

def register(request):                                          # <Register>
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()                                         # Crea el usuario
            return redirect('login')                            # Redirige a la vista de login
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})     # </Register>


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion del usuario, si es que inició sesion. Y envia a
    renderizar, usando la plantilla favoritos, las imagenes de los 
    pokemon que esten agregados a favoritos.
    """
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion de la tarjeta que el usuario que agregar a 
    favoritos. Se agrega la tajeta a favoritos y se vuelve a cargar la
    pantalla de galeria.
    """
    services.saveFavourite(request)
    return home(request)

@login_required
def deleteFavourite(request):
    """
    Una funcion simple que recibe como argumento una peticion http
    con la informacion de la tarjeta que el usuario quiere quitar de 
    favoritos. Se elimina la tajeta de favoritos y se vuelve a cargar la
    pantalla favoritos.
    """
    services.deleteFavourite(request)
    return getAllFavouritesByUser(request)

@login_required
def exit(request):
    """
    Una funcion simple que permite cerrar la sesion del usuario.
    Luego de cerrar sesion, se redirije al usuario a la pantalla
    de inicio.
    """
    logout(request)
    return redirect('home')