$ ->
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
    avatar: 'http://tp3.sinaimg.cn/1650783422/180/5715179049/1'
    text: '我們的目標是星辰大海'
  ,
    avatar: 'http://tp2.sinaimg.cn/1787684317/180/40047241448/1'
    text: '管它做什麼，再不做就沒機會做了'
  ]

  coords = [
    [-20, -290], [180, -250], [290, -140],
    [440, -50], [290, 80], [240, 190],
    [20, 240], [-190, 240], [-360, 90],
    [-350, -10], [-440, -120], [-280, -250],
  ]

  getRandomInt = (min, max) ->
    Math.floor(Math.random() * (max - min)) + min

  randomCoord = ->
    idx = Math.floor Math.random() * coords.length
    coords.splice(idx, 1)[0]

  eleCenter = (ele) ->
    rect = ele.getBoundingClientRect()
    [ (rect.left + rect.right) / 2, (rect.top + rect.bottom) / 2]

  clientCenter = ->
    [document.body.clientWidth / 2, document.body.scrollHeight / 2]

  generateChaser = (avatar, text) ->
    $('<div class="chaser"><div class="avatar"><img src="' + avatar + '" /></div><div class="board">' + text + '</div></div>')

  fixCenter = (ele) ->
    halfHeight = ele.height() / 2
    halfWidth = ele.width() / 2
    ele.css 'margin-left', -halfWidth
    ele.css 'margin-top', -halfHeight

  putPosition = (ele) ->
    [coordX, coordY] = randomCoord()
    [centerX, centerY] = clientCenter()
    ele.css 'left', centerX + coordX + getRandomInt(-10, 10)
    ele.css 'top', centerY + coordY + getRandomInt(-10, 10)

  $('.sign-btn').click ->
    $('.sign-container').fadeToggle()

  showChasers = ->
    chasers = $('#chasers')
    $.each dreams, (idx, data) ->
      ele = generateChaser data.avatar, data.text
      setTimeout ->
        chasers.append ele
        fixCenter ele
        putPosition ele
        ele.addClass 'bounceIn'
        setTimeout ->
          ele.removeClass 'bounceIn'
        , 500
      , idx * (getRandomInt 100, 150)

  showChasers()
