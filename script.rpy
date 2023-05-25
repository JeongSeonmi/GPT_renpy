﻿init python:
    renpy.music.register_channel("music", mixer="music",loop = True)
    see_point = 0 #추리점수
    see_point_room1 = 0 
    see_point_room2 = 0
    see_point_living = 0 

# 게임에서 사용할 이미지(배경, 캐릭터 등)
image bg_villa = "BG/villa1.jpg"   
image bg_villa_living = "BG/villa_living.png"
image bg_villa_room1 = "BG/villa_room1.jpg"
image bg_villa_room2 = "BG/villa_room2.jpg"
image bg_room = "BG/room.jpg"
image item_hint1 : #거실에서 메모누르면 이미지 뜸
        im.FactorScale("Item/pngegg.png", 0.5)
        xpos 720
        ypos 245
image item_hint2 : #거실에서 그림 누르면 이미지 뜸
        "Item/monariza.png" 
        xpos 720
        ypos 245
image cr_tam = im.FactorScale("CR/pngegg.png", 1.5)
##image side tam = ""


#------chatGPT API사용 예시------##연구 필요
#init python:
#    import openai  ##api키 보안 유의##
#    openai.api_key = "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"

# 게임에서 사용할 캐릭터
define ch_tam = Character('탐정', color="#00531d")
define ch_request = Character('의뢰인', color= "#C986BE")
define ch_men1 = Character("시민1", color = "#9d03fc")
define narrator = Character(None, kind = nvl,color = "#000000")
define ch_narrator = Character(None)

define persistent.see_point = 0 
##
screen test :
    imagemap :
        ground "BG/villa_living.png"

        hotspot(288, 591, 45, 44) action Return("post")
        hotspot(764, 319, 204, 152) action Return("painting")
        hotspot(1838, 685, 80, 180) action Show("test3")
            
screen test3 :  ##이미지 버튼 기능, 이미지 자체가 버튼 기능을 하는데 아직은 사용X
    imagebutton idle "Item/pngegg.png" :
        action Hide("test3")


# 여기에서부터 게임이 시작합니다.~return : 리턴은 메인메뉴로 돌아감
label start:
    scene bg_room with fade
    "\n\n추리 실력이 뛰어난 김탐정 탐정,\n개신동에서 탐정사무소를 오픈하게 되었다."
    nvl clear
    show cr_tam at right
    ch_tam "의뢰가 들어왔네"
    
    ch_tam "사건 장소로 가볼까?"
    play music "audio/music/music_main.mp3" fadein 2 #음악 재생#
    scene bg_villa with fade
    jump villa

label villa :
    scene bg_villa with dissolve
    show cr_tam at right
    ch_tam "어디부터 살펴볼까"
    menu : 
        "방1" :
            ch_tam "그래 방1부터 살펴보자"
            jump room1
        "방2" :
            ch_tam "그래 방2부터 살펴보자"
            jump room2
        "거실" :
            ch_tam "그래 거실부터 살펴보자"
            jump living_room
        "그만 살펴본다" :
            ch_tam "그래 이정도면 됐어."
            $killer_name = renpy.input('범인은 ...')
            if (killer_name == '의뢰인') and (see_point < 5):
                jump bad_ending1
            elif (killer_name == '의뢰인') and (see_point > 4):
                jump good_ending
            else :
                jump bad_ending2

label room1 :
    scene bg_villa_room1 with dissolve
    if (see_point_room1 < 1) :
        $see_point_room1 = 2
        "\n\n방은 먼지가 많이 쌓인 상태이다."
        nvl clear
        show cr_tam at right
        ch_tam "깨끗해보이는데 먼지가 많네.. 뭘 살펴볼까?"

    show cr_tam at right
    menu : 
        "침대" :
            ch_tam "(침대는 가지런히 정리되어 있다.) \n어? 머리끈이 있네?"
            $see_point +=1
            jump room1
        "선반" :
            ch_tam "(여러 장식품들이 놓여있다.) \n유난히 고양이 장식품들이 많네.."
            $see_point +=1
            jump room1
            
        "그림" :
            ch_tam "여긴 어떤 장소일까.."
            $see_point +=1
            jump room1
        "다른 곳을 살펴본다." :
            jump villa


            
    
label room2 :
    scene bg_villa_room2 with dissolve
    if(see_point_room2 < 1) :
        $see_point_room2 = 2
        "\n\n어젯밤에 이 방에서 살인사건이 일어났어."
        nvl clear
        show cr_tam at right
        ch_tam "여긴 피해자가 머무던 방이야."

    show cr_tam at right
    menu : 
        "침대" :
            ch_tam "피해자는 이 침대에서 자고 있었어"
            $see_point +=1
            jump room2
        "옷장" :
            ch_tam "큰 사이즈의 옷이 있다"
            $see_point +=1
            jump room2
        "침대 밑" :
            ch_tam "깨진 유리 조각이 있다"
            $see_point +=5  #see point 조건 달성을 위해 5로 조정#
            jump room2
        "다른 곳을 살펴본다." :
            jump villa

label living_room :
    scene bg_villa_living with dissolve
    if(see_point_living < 1) :
        $see_point_living = 2
        "\n\n넓은 거실에 가구가 몇 개 없어서 쓸쓸한 느낌이 든다."
        nvl clear
        show cr_tam at right
        ch_tam "거실에는 사람이 많이 다녔을거야."
    show cr_tam at right

    call screen test ## 이미지맵(클릭으로 힌트찾는 부분)
    if _return is "post":
        show item_hint1 with dissolve :
        ch_tam "이 쪽지의 내용은 추리하는데 도움되겠어"
        ch_tam "자세히 보니 용의자들끼리 역할 분담한 내용을 적어놓은 것 같아."    
        #사이드 이미지 사용할 예정

    if _return is "painting" :
        show item_hint2 with dissolve :
        ch_tam "이 그림은 고가의 그림인 것 같은데 "


    jump villa
    


label good_ending :
    #(killer_name == '의뢰인') and (see_point > 4)#
    ch_tam "범인은 의뢰인이야!"with vpunch
    stop music fadeout 2
    scene bg_room with fade
    ch_tam "이번에도 무사히 사건을 해결했군"
    return

label bad_ending1 :
    #(killer_name == '의뢰인') and (see_point < 5)#
    ch_tam "어째서 범인 그 사람일까?"
    ch_tam "다시 한번 살펴보자..."
    jump villa

label bad_ending2 :
    #(!(killer_name == '의뢰인'))#
    ch_tam "범인이 아닌것 같은데?"
    ch_tam "다시 한번 살펴보자..."
    jump villa