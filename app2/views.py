import json
# import os
# import pickle as pkl
from django.db.models import Sum, Avg
from django.shortcuts import render
import pandas as pd
# import numpy as np
from .models import socialmediadata



def facebook(request):
    facebook = socialmediadata.objects.filter(Account='Facebook')
    # value boxes here
    value_boxes = {
        'impressions': list(facebook.aggregate(Sum('Impressions')).values())[0],
        'engagements': round(list(facebook.aggregate(Avg('Totalengagement2')).values())[0], 2),
        'ClickThroughrate': round(list(facebook.aggregate(Avg('ClickThroughrate')).values())[0], 2),
        'folows_likes': list(facebook.aggregate(Sum('Follows')).values())[0] +
                        list(facebook.aggregate(Sum('Likes')).values())[0]
    }

    context = {
        'value_boxes': value_boxes,
    }
    return render(request, "app2/facebook.html", context)


def twitter(request):
    tweets = socialmediadata.objects.filter(Account='Twitter')
    value_boxes = {
        'impressions': list(tweets.aggregate(Sum('Impressions')).values())[0],
        'engagements': round(list(tweets.aggregate(Avg('Totalengagement2')).values())[0], 2),
        'ClickThroughrate': round(list(tweets.aggregate(Sum('Userprofileclicks')).values())[0], 2),
        'folows_likes': list(tweets.aggregate(Sum('Detailexpands')).values())[0]
    }

    context = {
        'value_boxes': value_boxes,
    }
    return render(request, "app2/twitter.html", context)


def linkedin(request):
    linkedin_ = socialmediadata.objects.filter(Account='LinkedIn')
    value_boxes = {
        'impressions': list(linkedin_.aggregate(Sum('Follows')).values())[0],
        'engagements': round(list(linkedin_.aggregate(Avg('Totalengagement2')).values())[0], 2),
        'ClickThroughrate': round(list(linkedin_.aggregate(Sum('ClickThroughrate')).values())[0], 2),
        'folows_likes': list(linkedin_.aggregate(Sum('Userprofileclicks')).values())[0]
    }

    context = {
        'value_boxes': value_boxes,
    }
    return render(request, "app2/linkedin.html", context)


def nba(request):
    df = pd.DataFrame(list(socialmediadata.objects.values())).sample(500)
    output = df
    predicted_values = output[output.Totalengagement == max(output.Totalengagement)]

    #
    def detailed_stats(infile):
        fb = infile.query("Account == '{}'".format('Facebook'))
        fb = fb[fb.Totalengagement == max(fb.Totalengagement)]
        tw = infile.query("Account == '{}'".format('Twitter'))
        tw = tw[tw.Totalengagement == max(tw.Totalengagement)]
        ln = infile.query("Account == '{}'".format('LinkedIn'))
        ln = ln[ln.Totalengagement == max(ln.Totalengagement)]

        df = pd.concat([fb, tw, ln], axis=0)[
            ['Account', 'Format', 'PostLength', 'Hashtags', 'Mentions', 'Totalengagement']]

        json_records = df.to_json(orient='records')
        data = []
        data = json.loads(json_records)
        return data

    print(detailed_stats(output))
    context = {
        'bet_params': {
            'platform': predicted_values.Account.values[0].lower,
            'format': predicted_values.Format.values[0],
            'postlength': predicted_values.PostLength.values[0],
            'hashtags': predicted_values.Hashtags.values[0],
            'engagement': round(predicted_values.Totalengagement.values[0]),
            'mentions': predicted_values.Mentions.values[0]},
        'df': detailed_stats(infile=output),

    }
    print(detailed_stats(output))
    return render(request, "app2/nba.html", context)
