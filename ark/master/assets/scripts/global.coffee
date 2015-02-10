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

avatarUpload = Qiniu.uploader
  runtimes: 'html5,flash,html4'
  browse_button: 'avatarUploadBtn'
  uptoken_url: '/uptoken/avatar'
  save_key: true
  domain: 'https://dn-ichaser-upload.qbox.me'
  container: 'profile-setting'
  max_file_size: '3mb'
  flash_swf_url: 'js/plupload/Moxie.swf'
  max_retries: 3
  dragdrop: false
  drop_element: 'profile-setting'
  chunk_size: '4mb'
  auto_start: true
  init:
    'FilesAdded': (up, files) ->
      $('#avatarSaveTip').fadeIn()
    'BeforeUpload': (up, file) ->
    'UploadProgress': (up, file) ->
    'FileUploaded': (up, file, info) ->
      infoObj = JSON.parse info
      image_url = infoObj.key
      token = $('#avatarUploadBtn').attr('data-csrf')
      $.ajax
        url: '/account/avatar'
        type: 'POST'
        data:
          avatar_url: image_url
          csrf_token: token
        success: (resp) ->
          if resp.success
            $('.avatarImage').attr('src', resp.url)
            $('#avatarSaveTip').fadeOut()
    'Error': (up, err, errTip) ->
      $('#avatarSaveTip').fadeOut()
    'UploadComplete': () ->
