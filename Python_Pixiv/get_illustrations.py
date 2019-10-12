
# coding: utf-8

from pixivpy_async import *
from pixivpy_async.sync import *
from time import sleep
import json
import os
import re

# ログイン処理
# Log in to pixiv
f = open("client.json", "r")
client_info = json.load(f)
f.close()
api = PixivAPI()
api.login(client_info["pixiv_id"], client_info["password"])
aapi = AppPixivAPI()
aapi.login(client_info["pixiv_id"], client_info["password"])

# 入力された絵師IDから絵師情報を取得
# Enter the Illustrator-Id
illustrator_pixiv_id = int(input("Type illustrator pixiv id number:\n>>>"))

# ユーザ情報（作品数、絵師名）を取得
# get illustratir infomation
user_info_json = aapi.user_detail(illustrator_pixiv_id)
total_works = user_info_json.profile.total_illusts + user_info_json.profile.total_manga
illustrator_name = user_info_json.user.name

# イラスト情報を取得
# get illustrations information
works_info = api.users_works(illustrator_pixiv_id, page = 1, per_page = total_works)

# 渡されたディレクトリが存在しない場合に作成するLambda関数
# make directories
mkdirExceptExist = lambda path: "" if os.path.exists(path) else os.mkdir(path)

saving_direcory_path = "./pixiv_images/" + illustrator_name + "/"
saving_direcory_path_R18 = saving_direcory_path + "R-18/"

# 保存用フォルダがない場合は生成
# make directories
mkdirExceptExist("./pixiv_images")
mkdirExceptExist(saving_direcory_path) 
mkdirExceptExist(saving_direcory_path_R18)

# ダウンロード開始
# Display information of illustrator and illustrations & Download 
separator = "============================================================"
print("Artist: %s" % illustrator_name)
print("Works: %d" %  total_works)
print(separator)

for i, work_info in enumerate(works_info.response):

	work_title = work_info.title
	print("Procedure: %d/%d" % (i + 1,total_works))
	print("Title: %s" % work_title)
	print(separator)

	# ファイル名に適した形にリネーム
	# rename the file 
	work_title = re.sub("[: | \? | . | \" | < | > | \ | /]","",work_title)
	
	if "R-18" in work_info.tags: 
		dir = saving_direcory_path_R18
	else:
		dir = saving_direcory_path

	# 漫画の場合
	# illustrations with only one picture
	if work_info.is_manga:
		manga_info = api.works(work_info.id)
		for page_no in range(0, manga_info.response[0].page_count):
			page_info = manga_info.response[0].metadata.pages[page_no]
			num = str(page_no) if len(str(page_no)) > 1 else "0" + str(page_no)
			aapi.download(page_info.image_urls.large, path = dir, name = work_title + num + ".jpg")

	# イラストの場合
	# illustrations with more than one picture
	else:
		aapi.download(work_info.image_urls.large, path = dir, name = work_title + ".jpg")

print("\nThat\"s all.")