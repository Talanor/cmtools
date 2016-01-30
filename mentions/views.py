from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import tweepy
import datetime

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import ClientForm, Client, Mention, MentionsQueryForm


@login_required
def index(request):
    return render(request, "mentions/index.html")


@login_required
def client_add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClientForm(request.POST, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/mentions/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClientForm(user=request.user)
    return render(
            request,
            "mentions/client_add.html",
            context={
                "form": form,
                "next": "/client/add/"
            }
    )


@login_required
def client_list(request):
    return render(
        request,
        "mentions/client_list.html",
        context={
            "clients": Client.objects.all()
        }
    )


@login_required
def mention_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    form = MentionsQueryForm(initial={"client_id": client_id})
    return render(
        request,
        "mentions/mention_list.html",
        context={
            "client": client,
            "form": form
        }
    )


@login_required
def api_v1_get_n_mentions_between(request):
    client = get_object_or_404(Client, pk=request.POST.get("client_id"))

    start_date = datetime.datetime.strptime(request.POST.get("start_date"), "%d/%m/%Y %H:%M")
    end_date = datetime.datetime.strptime(request.POST.get("end_date"), "%d/%m/%Y %H:%M")

    max_id = None
    since_id = None

    n_after = Mention.objects.filter(created_at__gt=end_date).count()
    n_before = Mention.objects.filter(created_at__lt=start_date).count()

    qset = Mention.objects\
            .filter(created_at__gte=start_date, created_at__lte=end_date)\
            .order_by("created_at")

    if n_after > 0:
        last_tweet = qset\
            .latest()

        max_id = last_tweet.id

    if n_before > 0:
        first_tweet = qset\
            .first()

        since_id = first_tweet.id

    tweets = []
    if max_id is not None or since_id is not None:
        tweets = qset.all()

    auth = tweepy.OAuthHandler(client.consumer_key, client.consumer_secret)
    auth.secure = True
    auth.set_access_token(client.access_token, client.access_token_secret)

    api = tweepy.API(auth)

    while True:
        mentions = api.mentions_timeline(max_id=max_id, since_id=since_id)

        if len(mentions) == 0 or mentions[0].created_at < start_date:
            break

        max_id = mentions[-1].id

        if mentions[-1].created_at > end_date:
            continue

        for mention in mentions:
            if start_date <= mention.created_at <= end_date:
                omention = Mention(
                    text=mention.text,
                    id=mention.id,
                    created_at=mention.created_at,
                    username=mention.user.name,
                    client=client
                )
                omention.save()
                tweets.append(omention)

    return HttpResponse("You have %d mentions " % (len(tweets)))