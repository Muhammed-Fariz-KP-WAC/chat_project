from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Room, Message
from django.utils.text import slugify

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        
        if not name or not password:
            messages.error(request, 'Both room name and password are required.')
            return redirect('create_room')
            
        slug = slugify(name)
        
        if Room.objects.filter(slug=slug).exists():
            messages.error(request, 'A room with this name already exists.')
            return redirect('create_room')
        
        room = Room.objects.create(
            name=name,
            slug=slug,
            password=password,
            creator=request.user.profile
        )
        room.participants.add(request.user.profile)
        return redirect('room', slug=slug)
        
    return render(request, 'room/create_room.html')

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == room.password:
            room.participants.add(request.user.profile)
            messages.success(request, 'Successfully joined the room!')
            return redirect('room', slug=slug)
        else:
            messages.error(request, 'Incorrect password')
            return redirect('rooms')

    if not room.participants.filter(id=request.user.profile.id).exists():
        return render(request, 'room/join_room.html', {'room': room})

    # Rename the variable to avoid conflict with Django's messages framework
    chat_messages = Message.objects.filter(room=room).order_by('date_added')

    return render(request, 'room/room.html', {'room': room, 'chat_messages': chat_messages})