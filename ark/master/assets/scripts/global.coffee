$('#header .container').css('width', document.body.clientWidth)
$('#header .profile #msgContainer').mouseover ->
  $('#header .profile ul').hide()
$('#header .profile #msgContainer').mouseout ->
  $('#header .profile ul').show()

$('#passwordForm input').tooltipster
  trigger: 'custom'
  position: 'top'

$('#profileForm input').tooltipster
  trigger: 'custom'
  position: 'top'

$('#profileForm textarea').tooltipster
  trigger: 'custom'
  position: 'top'

$('#msgContainer .closeBtn').click ->
  $('#msgContainer').fadeOut()

$('#openSettingBtn').click ->
  $('.msg-tips').hide()
  $('.mask').fadeIn()
  $('#profile-setting').fadeIn()

$('.cancelBtn').click ->
  $('.mask').fadeOut()
  $('#profile-setting').fadeOut()

$('.mask').click ->
  $('.mask').fadeOut()
  $('.mask-fadeOut').fadeOut()

$('.tabBtn').click ->
  tab = $(this).attr('data-tab')
  $('.tabBtn').removeClass('selected')
  $(this).addClass('selected')
  $('.tab-container').hide()
  $("##{tab}-tab").show()

$('#passwordForm').ajaxForm
  type: 'PUT'
  success: (resp) ->
    if (resp.success)
      document.getElementById('passwordForm').reset()
      $('#passwordForm input').tooltipster 'hide'
      $('#passwordForm .msg-tips').fadeIn()
    else
      for field, msg of resp.messages
        $("##{field}").tooltipster 'update', msg?.join ','
        $("##{field}").tooltipster 'show'

$('#profileForm').ajaxForm
  type: 'PUT'
  success: (resp) ->
    if (resp.success)
      $('#profileForm input').tooltipster 'hide'
      $('#profileForm textarea').tooltipster 'hide'
      $('#profileForm .msg-tips').fadeIn()
    else
      for field, msg of resp.messages
        $("##{field}").tooltipster 'update', msg?.join ','
        $("##{field}").tooltipster 'show'
