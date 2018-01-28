from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RoomModel

# Create your views here.


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """

    # Get a list of rooms, ordered alphabetically
    rooms_qs = RoomModel.objects.order_by("title")
    print(rooms_qs)

    # query set from RoomModel
    context = {"rooms": rooms_qs}

    # Render that in the index template
    return render(request, "index.html", context)
