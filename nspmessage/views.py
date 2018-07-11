from django.shortcuts import render,redirect
from .models import Message
from django.contrib.auth.models import User
from nspmessage.models import Message
from accounts.models import UserProfile,Follow
from collections import OrderedDict
# Create your views here.

def chatFriend(request,username):
	sender = request.user
	receiver = User.objects.get(username=username)
	current_user_profile = UserProfile.objects.get(user=request.user)
	receiver_user_profile = UserProfile.objects.get(user=receiver)
	followings = Follow.objects.filter(follower=sender)
	current_participants = [sender,receiver]
	participants = [sender]
	for following in followings:
		participants.append(following.following)
	conversations = OrderedDict()
	messages = Message.objects.filter(sender__in=current_participants,receiver__in=current_participants).order_by("id")
	conv_messages = Message.objects.filter(sender__in=participants,receiver__in=participants).order_by("id")
	for conv_message in conv_messages:
		conv_participants = [conv_message.sender,conv_message.receiver]
		last_message = Message.objects.filter(sender__in=conv_participants,receiver__in=conv_participants).order_by("-id")[0].msg_content
		if conv_participants[0] == request.user:
			try:
				if not conversations[conv_participants[1]]:
					contact_profile = UserProfile.objects.get(user=conv_participants[1])
					conversations[conv_participants[1]] = {"profile":contact_profile,"last_message":last_message}
			except KeyError:
				contact_profile = UserProfile.objects.get(user=conv_participants[1])
				conversations[conv_participants[1]] = {"profile":contact_profile,"last_message":last_message}			
		else:
			try:
				if not conversations[conv_participants[0]]:
					contact_profile = UserProfile.objects.get(user=conv_participants[0])
					conversations[conv_participants[0]] = {"profile":contact_profile,"last_message":last_message}
			except KeyError:
				contact_profile = UserProfile.objects.get(user=conv_participants[0])
				conversations[conv_participants[0]] = {"profile":contact_profile,"last_message":last_message}	

	context = {"messages":messages,"receiver":receiver,"sender_user_profile":current_user_profile,
						"receiver_user_profile":receiver_user_profile,"conversations":conversations}
	return render(request,"chat.html",context)

def newMessage(request,username):
	sender = request.user
	receiver = User.objects.get(username=username)
	message = request.POST.get("sender_message")
	Message.objects.create(
					sender=sender,	   
					receiver=receiver,
					msg_content=message)
	return redirect("/chat/{}".format(username))