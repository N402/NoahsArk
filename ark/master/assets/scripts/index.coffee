dreams = [
  avatar: '/static/images/avatars/1.png'
  text: '去每一栋女生宿舍'
,
  avatar: '/static/images/avatars/2.png'
  text: '拍拖!'
,
  avatar: '/static/images/avatars/3.png'
  text: '出国旅游!'
,
  avatar: '/static/images/avatars/4.png'
  text: '从科技楼跳下去'
,
  avatar: '/static/images/avatars/5.png'
  text: '夜游校园'
,
  avatar: '/static/images/avatars/6.png'
  text: '脱团..'
,
  avatar: '/static/images/avatars/7.png'
  text: '旁听各种选修课'
,
  avatar: '/static/images/avatars/8.png'
  text: '入党成功'
,
  avatar: '/static/images/avatars/8.png'
  text: '然后拒交党费'
,
  avatar: '/static/images/avatars/9.png'
  text: '做一件不敢做的事'
,
  avatar: 'http://tp2.sinaimg.cn/1787684317/180/40047241448/1'
  text: '管它做什麼，再不做就沒機會做了'
]

isOver = (lhp, rhp) ->
  lhpRect = lhp.getBoundingClientRect()
  rhpRect = rhp.getBoundingClientRect()
  console.log lhpRect, rhpRect
  ((lhpRect.top > rhpRect.top and lhpRect.bottom < rhpRect.bottom) or
   (lhpRect.left > rhpRect.left and lhpRect.right < rhpRect.right))

generateChaser = (avatar, text) ->
  $('<div class="chaser"><div class="avatar"><img src="' + avatar + '" /></div><div class="board">' + text + '</div></div>')

getRandomInt = (min, max) ->
  Math.floor(Math.random() * (max - min)) + min

randomPosition = (ele) ->
  x = getRandomInt(0, document.body.clientWidth / 3)
  y = getRandomInt(0, document.body.scrollHeight / 3)
  if getRandomInt(0, 2) > 0
    ele.css 'margin-left', x
  else
    ele.css 'margin-left', -x
  if getRandomInt(0, 2) > 0
    ele.css 'margin-top', y
  else
    ele.css 'margin-top', -y

rePotision = (ele) ->
  ele.removeClass 'popOut'
  randomPosition ele
  ele.addClass 'popOut'

start = ->
  chasers = $('#chasers')
  $.each dreams, (idx, data) ->
    ele = generateChaser data.avatar, data.text
    randomPosition ele
    setTimeout ->
      chasers.append ele
      ele.addClass 'popOut'
    , idx * getRandomInt 300, 500

check = ->
  interval = setInterval ->
    flag = true
    $.each $('.chaser'), (idx, ele) ->
      if isOver ele, $('#logo')[0]
        rePotision $(ele)
        flag = false
    if flag
      cleanInterval interval
  , 1

start()
check()
