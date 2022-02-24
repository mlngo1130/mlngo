# -*- coding: utf-8 -*- 


import asyncio
import os	
import datetime
from boto3 import client
from pyssml.PySSML import PySSML

basicSetting = []
bossData = []

bossNum = 0

#client = texttospeech.TextToSpeechClient()

def MakeSound(saveSTR, filename, speed):
	global access_key
	global access_secret_key
	
	polly = client('polly', aws_access_key_id = access_key, aws_secret_access_key = access_secret_key, region_name = 'eu-west-1')

	s = '<speak><prosody rate="' + speed + '%">' +  saveSTR + '</prosody></speak>'

	response = polly.synthesize_speech(
		TextType = 'ssml',
		Text=s,
		OutputFormat='mp3',
		VoiceId='Seoyeon')

	stream = response.get('AudioStream')

	with open('./sound/ori/' + filename + '_ori.mp3', 'wb') as mp3file:
		data = stream.read()
		mp3file.write(data)

	os.system("echo Y| ffmpeg -i \"./sound/ori/" + filename + "_ori.mp3\"  -acodec copy \"./sound/" + filename + ".mp3\"")

def init():
	global basicSetting
	global bossData

	global bossNum

	global access_key
	global access_secret_key

	print ('MakeSound Start!')
	tmp_bossData = []
	tmp_fixed_bossData = []
	bossData = []
	fixed_bossData = []
	ment_Data = []
	f = []
	fb = []

	keyinidata = open('MS_setting.ini', 'r', encoding = 'utf-8')
	mentinidata = open('record_Data.ini', 'r', encoding = 'utf-8')
	inidata = open('test_setting.ini', 'r', encoding = 'utf-8')
	boss_inidata = open('boss.ini', 'r', encoding = 'utf-8')
	fixed_initdata = open('fixed_boss.ini', 'r', encoding = 'utf-8')

	tmp_keyData = keyinidata.readlines()
	tmp_ment_inputData = mentinidata.readlines()
	tmp_inputData = inidata.readlines()
	tmp_boss_inputData = boss_inidata.readlines()
	tmp_fixed_inputData = fixed_initdata.readlines()
	
	key_inputData = tmp_keyData
	ment_inputData = tmp_ment_inputData
	inputData = tmp_inputData
	boss_inputData = tmp_boss_inputData
	fixed_inputData = tmp_fixed_inputData
	
	del(boss_inputData[0])
	del(fixed_inputData[0])

	for i in range(key_inputData.count('\n')):
		key_inputData.remove('\n')

	for i in range(ment_inputData.count('\n')):
		ment_inputData.remove('\n')
	
	for i in range(inputData.count('\n')):
		inputData.remove('\n')
	
	for i in range(boss_inputData.count('\n')):
		boss_inputData.remove('\n')
		
	for i in range(fixed_inputData.count('\n')):
		fixed_inputData.remove('\n')

	verChk = 0
	fixed_verChk = 0

	for i in range(len(boss_inputData)) :
		if boss_inputData[i].find('kakaoOnOff') != -1 :
			verChk = 1
			
	for i in range(len(fixed_inputData)) :
		if fixed_inputData[i].find('kakaoOnOff') != -1 :
			fixed_verChk = 1

	if verChk == 1 :
		bossNum = int(len(boss_inputData)/7) 
		for i in range(bossNum):
			tmp_bossData.append(boss_inputData[i*7:i*7+7])
	else :
		bossNum = int(len(boss_inputData)/6)
		for i in range(bossNum):
			tmp_bossData.append(boss_inputData[i*6:i*6+6])

	if fixed_verChk == 1 :
		fixed_bossNum = int(len(fixed_inputData)/7) 
		for i in range(fixed_bossNum):
			tmp_fixed_bossData.append(fixed_inputData[i*7:i*7+7]) 
	else :
		fixed_bossNum = int(len(fixed_inputData)/6)
		for i in range(fixed_bossNum):
			tmp_fixed_bossData.append(fixed_inputData[i*6:i*6+6])  
	
	#print (tmp_bossData)
	#print (tmp_fixed_bossData)
	for j in range(len(key_inputData)):
		key_inputData[j] = key_inputData[j].strip()
	
	for j in range(len(ment_inputData)):
		ment_inputData[j] = ment_inputData[j].strip()	

	access_key = key_inputData[1][20:len(key_inputData[1])]
	access_secret_key = key_inputData[2][24:len(key_inputData[2])]
	speed = key_inputData[3][8:len(key_inputData[3])]
	mode = key_inputData[4][7:len(key_inputData[4])]

	############## 보탐봇 초기 설정 리스트 #####################
	basicSetting.append(inputData[0][12:])     #basicSetting[0] : bot_token
	basicSetting.append(inputData[7][15:])     #basicSetting[1] : before_alert
	basicSetting.append(inputData[9][10:])     #basicSetting[2] : mungChk
	basicSetting.append(inputData[8][16:])     #basicSetting[3] : before_alert1
	basicSetting.append(inputData[11][14:16])  #basicSetting[4] : restarttime 시
	basicSetting.append(inputData[11][17:])    #basicSetting[5] : restarttime 분
	basicSetting.append(inputData[3][15:])     #basicSetting[6] : voice채널 ID
	basicSetting.append(inputData[4][14:])     #basicSetting[7] : text채널 ID
	basicSetting.append(inputData[1][16:])     #basicSetting[8] : 카톡챗방명
	basicSetting.append(inputData[2][13:])     #basicSetting[9] : 카톡챗On/Off
	basicSetting.append(inputData[5][16:])     #basicSetting[10] : 사다리 채널 ID
	basicSetting.append(inputData[10][14:])    #basicSetting[11] : !q 표시 보스 수
	basicSetting.append(inputData[12][16:])    #basicSetting[12] : restart 주기
	basicSetting.append(inputData[6][17:])     #basicSetting[13] : 정산 채널 ID
	basicSetting.append(inputData[13][12:])    #basicSetting[14] : 스프레드시트 파일 이름
	basicSetting.append(inputData[14][11:])    #basicSetting[15] : json 파일명
	basicSetting.append(inputData[15][12:])    #basicSetting[16] : 시트 이름
	basicSetting.append(inputData[16][12:])    #basicSetting[17] : 입력 셀
	basicSetting.append(inputData[17][13:])    #basicSetting[18] : 출력 셀

	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()
	
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])		  #bossData[0] : 보스명
		f.append(tmp_bossData[j][1][10:tmp_len])  #bossData[1] : 시
		f.append(tmp_bossData[j][2][13:])		  #bossData[2] : 멍/미입력
		f.append(tmp_bossData[j][3][20:])		  #bossData[3] : 분전 알림멘트
		f.append(tmp_bossData[j][4][13:])		  #bossData[4] : 젠 알림멘트
		f.append(tmp_bossData[j][1][tmp_len+1:])  #bossData[5] : 분
		#f.append(tmp_bossData[j][5][13:])		  #bossData[6] : 카톡On/Off		
		#f.append('')							  #bossData[7] : 메세지
		bossData.append(f)
		f = []
		
	for j in range(fixed_bossNum):
		tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
		tmp_fixedGen_len = tmp_fixed_bossData[j][2].find(':')
		fb.append(tmp_fixed_bossData[j][0][11:])			      #fixed_bossData[0] : 보스명
		fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])     #fixed_bossData[1] : 시
		fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])     #fixed_bossData[2] : 분
		fb.append(tmp_fixed_bossData[j][4][20:])			      #fixed_bossData[3] : 분전 알림멘트
		fb.append(tmp_fixed_bossData[j][5][13:])			      #fixed_bossData[4] : 젠 알림멘트
		#fb.append(tmp_fixed_bossData[j][6][13:])			      #fixed_bossData[5] : 카톡On/Off		
		#fb.append(tmp_fixed_bossData[j][2][12:tmp_fixedGen_len])  #fixed_bossData[6] : 젠주기-시
		#fb.append(tmp_fixed_bossData[j][2][tmp_fixedGen_len+1:])  #fixed_bossData[7] : 젠주기-분
		##fb.append(tmp_fixed_bossData[j][3][12:16])                #fixed_bossData[8] : 시작일-년	
		f#b.append(tmp_fixed_bossData[j][3][17:19])                #fixed_bossData[9] : 시작일-월
		f#b.append(tmp_fixed_bossData[j][3][20:22])                #fixed_bossData[10] : 시작일-일	
		fixed_bossData.append(fb)
		fb = []

	for j in range(len(ment_inputData)):
		tmp_len = ment_inputData[j].find(',')
		f.append(ment_inputData[j][:tmp_len])  #ment_Data[#][0] : 파일명
		f.append(ment_inputData[j][tmp_len+2:])  #ment_Data[#][1] : 멘트
		f.append('')							
		ment_Data.append(f)
		f = []

	#MakeSound('안녕하세요', 'hello', speed)
	if mode == '1':
		for i in range(fixed_bossNum):
			MakeSound(fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3], fixed_bossData[i][0] + '알림', speed)
			MakeSound(fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3], fixed_bossData[i][0] + '알림1', speed)
			MakeSound(fixed_bossData[i][0] + ' ' + fixed_bossData[i][4], fixed_bossData[i][0] + '젠', speed)

		for i in range(bossNum):
			MakeSound(bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3], bossData[i][0] + '알림', speed)
			MakeSound(bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3], bossData[i][0] + '알림1', speed)
			MakeSound(bossData[i][0] + ' ' + bossData[i][4], bossData[i][0] + '젠', speed)
			MakeSound(bossData[i][0] + ' 미입력 됐습니다.', bossData[i][0] + '미입력', speed)
			MakeSound(bossData[i][0] + ' 멍 입니다.', bossData[i][0] + '멍', speed)	

	else :
		for i in range(len(ment_Data)):
			MakeSound(ment_Data[i][1], ment_Data[i][0], speed)
	
	print ('Finish!')

init()

'''
< VoiceId >
Arabic(arb) : Zeina
Chinese, Mandarin (cmn-CN) : Zhiyu
Danish (da-DK) : Naja / Mads
Dutch (nl-NL) : Lotte / Ruben
English, Australian (en-AU) : Nicole / Russell
English, British (en-GB) : Amy, Emma / Brian
English, Indian (en-IN) : Aditi (bilingual with Hindi), Raveena
English, US (en-US) : Ivy, Joanna, Kendra, Kimberly, Salli / Joey, Justin, Matthew
English, Welsh (en-GB-WLS) : Geraint
French (fr-FR) : Céline/Celine, Léa / Mathieu
French, Canadian (fr-CA) : Chantal
German (de-DE) : Marlene, Vicki / Hans
Hindi (hi-IN) : Aditi (bilingual with Indian English)
Icelandic (is-IS) : Dóra/Dora / Karl
Italian (it-IT) : Carla, Bianca / Giorgio
Japanese (ja-JP) : Mizuki / Takumi
Korean (ko-KR) : Seoyeon
Norwegian (nb-NO) : Liv
Polish (pl-PL) : Ewa, Maja / Jacek, Jan
Portuguese, Brazilian (pt-BR) : Vitória/Vitoria / Ricardo
Portuguese, European (pt-PT) : Inês/Ines / Cristiano
Romanian (ro-RO) : Carmen
Russian (ru-RU) : Tatyana / Maxim
Spanish, European (es-ES) : Conchita, Lucia / Enrique
Spanish, Mexican (es-MX) : Mia
Spanish, US (es-US) : Penélope/Penelope / Miguel
Swedish (sv-SE) : Astrid
Turkish (tr-TR) : Filiz
Welsh (cy-GB) : Gwyneth
'''