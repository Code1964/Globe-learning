from flask import Flask, flash, redirect, render_template, request, session, url_for
import wikipediaapi
import json
import requests

from helpers import apology

# リダイレクト元：map.html
# 地域名をgetで取得

def country_info():
    region_name = request.args.get('region')

    if not region_name:
        flash("国/地域を選択してください")
        return redirect(url_for('map'))

    wiki = wikipediaapi.Wikipedia("ja")
    page = wiki.page(region_name)
    if not page.exists():
        return apology("Not in countries where data acquisition is possible", 501)

    # print(page.content) # コンテンツ全て
    # print(page.title) # タイトル
    # print(page.summary) # 要約
    # print(page.html()) # html
    # print(page.images) #全写真url
    url="https://pixabay.com/api"

    params={
        "key":"34132799-a99680c2889f5f7f494030834",
        "q":region_name + "国旗",
        "lang":"ja",
        "image_type":"photo"
    }

    result = requests.get(url, params=params)

    data = json.loads(result.text)
    if data["totalHits"] > 0:
        region_image = data["hits"][0]["webformatURL"]
    else:
        region_image = [] # どちらにしろ渡すので空のものをダミーで作成

    # ==================================================

    sections = page.sections
    # print(sections[1])  # section1つ目出力, 基本的に概要

    title = []
    detail = []
    for section in sections:
        if section.title == '歴史':
            for i in range(len(section.sections)):
                text = str(section.sections[i]).split()
                # print(text[1]) # 常に[1]がタイトル、本文の位置も決まってる
                title.append(text[1])
                # print("".join(text[3:len(text)-2]))
                detail.append("".join(text[3:len(text)-2]))
            break

    historys = dict(zip(title, detail))
    wiki_summary = page.summary

    return render_template("country_info.html", wiki_summary=wiki_summary, region_image=region_image, historys=historys)
