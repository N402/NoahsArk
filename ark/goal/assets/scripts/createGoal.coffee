$('#createGoalForm input').tooltipster
  position: 'top'
  trigger: 'custom'

$('#createGoalForm textarea').tooltipster
  position: 'top'
  trigger: 'custom'

$('#createGoalChoosePicBtn').tooltipster
  position: 'top'
  trigger: 'custom'
$('#createGoalChoosePicBtn').tooltipster 'update', '请选择图片'

$('#createGoalForm').ajaxForm
  success: (resp) ->
    if resp.success
      $('#mask').fadeOut()
      $('#createGoal').fadeOut()
      location.reload()
    else
      for field, msg of resp.messages
        if field in ['image_url', 'image_name']
          $('#createGoalChoosePicBtn').tooltipster 'show'
        else
          $('#' + field).tooltipster 'update', msg?.join ','
          $('#' + field).tooltipster 'show'

uploader = Qiniu.uploader
  runtimes: 'html5,flash,html4'
  browse_button: 'createGoalChoosePicBtn'
  uptoken_url: '/uptoken'
  save_key: true
  domain: 'https://dn-ichaser-upload.qbox.me'
  container: 'createGoal'
  max_file_size: '3mb'
  flash_swf_url: 'js/plupload/Moxie.swf'
  max_retries: 3
  dragdrop: false
  drop_element: 'createGoal'
  chunk_size: '4mb'
  auto_start: false
  init:
    'FilesAdded': (up, files) ->
      return unless files
      $('#createGoalPrevewContainer').show()
      $('.pics .pic').removeClass 'pic-selected'
      $('#createGoalChoosePicBtn').addClass('pic-selected')
      $('#createGoalPrevewContainer').addClass 'pic-selected'
      plupload.each files, (file) ->
        document.getElementById('createGoalPriview').src = window.URL.createObjectURL file.getNative()
        document.getElementById('is_external_image').value = 'True'
    'BeforeUpload': (up, file) ->
    'UploadProgress': (up, file) ->
    'FileUploaded': (up, file, info) ->
      infoObj = JSON.parse info
      document.getElementById('image_name').value = infoObj.name
      document.getElementById('image_url').value = infoObj.key
    'Error': (up, err, errTip) ->
    'UploadComplete': () ->
      document.getElementById('is_external_image').value = 'True'
      $('#createGoalForm input').tooltipster 'hide'
      $('#createGoalForm textarea').tooltipster 'hide'
      $('#createGoalChoosePicBtn').tooltipster 'hide'
      $('#createGoalForm').submit()
      $('#createBtn').removeAttr('disabled')
      $('#createBtn').html('创建')
      $('#createGoalChoosePicBtn').removeClass('pic-selected')

createGoal = ->
  if document.getElementById('is_external_image').value == 'True'
    $('#createBtn').attr('disabled', 'disabled')
    $('#createBtn').html('创建中...')
    uploader.start()
  else
    document.getElementById('is_external_image').value = 'False'
    $('#createGoalForm').submit()

$('#createBtn').click ->
  createGoal()

$('#openModalBtn').click ->
  $('#mask').fadeIn()
  $('#createGoal').fadeIn()

$('#createCancelBtn').click ->
  $('#mask').fadeOut()
  $('#createGoal').fadeOut()

$('.pics .pic:not(#createGoalChoosePicBtn)').click ->
  $('.pics .pic').removeClass 'pic-selected'
  $(this).addClass 'pic-selected'
  document.getElementById('image_name').value = "#{$(this).attr('data')}.png"
  document.getElementById('image_url').value = "/static/images/pics/#{$(this).attr('data')}.png"
  document.getElementById('is_external_image').value = 'False'
