$('#activity').tooltipster
  trigger: 'custom'
  position: 'top'
$('#upImage').tooltipster
  trigger: 'custom'
  position: 'right'
$('#upImage').tooltipster 'update', '请上传图片'

$('#createActivityForm').ajaxForm
  success: (resp) ->
    if resp.success
      activity = $('<div class="activity"></div>').append($('#activity').val())
      if $('#preview').attr('src').length > 0
        activity.append($('<div class="activity-image"></div>').append(
          $("<img src='#{$('#preview').attr('src')}' />")))
      activity.append($('<div class="activity-time">刚刚</div>')).fadeIn("slow")
      $('#activities').prepend(activity)
      $('#createActivityForm')[0].reset()
      document.getElementById('preview').src = ''
    else
      for field, msg of resp.messages
        if field in ['image_url', 'image_name']
          $('#upImage').tooltipster 'show'
        if field == 'activity'
          $('#activity').tooltipster 'update', msg?.join ','
          $('#activity').tooltipster 'show'

uploader = Qiniu.uploader
  runtimes: 'html5,flash,html4'
  browse_button: 'upImage'
  uptoken_url: '/uptoken'
  save_key: true
  domain: 'https://dn-ichaser-upload.qbox.me'
  container: 'create-activity'
  max_file_size: '3mb'
  flash_swf_url: 'js/plupload/Moxie.swf'
  max_retries: 3
  dragdrop: false
  drop_element: 'create-activity'
  chunk_size: '4mb'
  auto_start: false
  init:
    'FilesAdded': (up, files) ->
      plupload.each files, (file) ->
        document.getElementById('preview').src = window.URL.createObjectURL file.getNative()
    'BeforeUpload': (up, file) ->
    'UploadProgress': (up, file) ->
    'FileUploaded': (up, file, info) ->
      infoObj = JSON.parse info
      document.getElementById('image_name').value = infoObj.name
      document.getElementById('image_url').value = infoObj.key
    'Error': (up, err, errTip) ->
    'UploadComplete': () ->
      $('#createActivityForm').submit()
      $('#submitBtn').removeAttr('disabled')
      $('#activity').removeAttr('readonly')

updateAvtivity = ->
  $('#activity').tooltipster 'hide'
  $('#upImage').tooltipster 'hide'
  $('#submitBtn').attr('disabled', 'disabled')
  $('#activity').attr('readonly', 'readonly')
  uploader.start()

$('#giveUpBtn').click ->
  $.ajax $(this).attr('data-url'),
    type: 'DELETE'
    cache: false
    dataType: 'json'
    success: (resp) ->
      if resp.success
        location.reload()

$('#completeBtn').click ->
  $.ajax $(this).attr('data-url'),
    type: 'PUT'
    cache: false
    dataType: 'json'
    success: (resp) ->
      if resp.success
        location.reload()
