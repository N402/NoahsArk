w = h = x = y = 0

updateCoords = (crop) ->
  w = crop.w
  h = crop.h
  x = crop.x
  y = crop.y

$('#uploadBtn').click ->
  uploader.start()

getUploader = () ->
  Qiniu.uploader
    runtimes: 'html5,flash,html4'
    browse_button: 'browerBtn'
    uptoken_url: "/uptoken/avatar"
    save_key: true
    domain: 'https://dn-ichaser-upload.qbox.me'
    container: 'container'
    max_file_size: '3mb'
    flash_swf_url: 'js/plupload/Moxie.swf'
    max_retries: 3
    dragdrop: false
    drop_element: 'container'
    chunk_size: '4mb'
    auto_start: false
    init:
      'FilesAdded': (up, files) ->
        plupload.each files, (file) ->
          document.getElementById('preview').src = window.URL.createObjectURL file.getNative()
          $('#preview').Jcrop
            onChange: updateCoords,
            onSelect: updateCoords,
      'BeforeUpload': (up, file) ->
      'UploadProgress': (up, file) ->
      'FileUploaded': (up, file, info) ->
        infoObj = JSON.parse info
        imgLink = Qiniu.imageMogr2
          thumbnail: "#{$('#preview').width()}x#{$('#preview').height()}"
          crop: "!#{w}x#{h}a#{x}a#{y}",
        , infoObj.key
        document.getElementById('avatar_url').value = imgLink
      'Error': (up, err, errTip) ->
      'UploadComplete': () ->
        document.getElementById('avatarForm').submit()

uploader = getUploader()
