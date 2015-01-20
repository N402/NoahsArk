uploader = Qiniu.uploader
    runtimes: 'html5,flash,html4'
    browse_button: 'upbtn'
    uptoken_url: '/uptoken'
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
      'BeforeUpload': (up, file) ->
      'UploadProgress': (up, file) ->
      'FileUploaded': (up, file, info) ->
        infoObj = JSON.parse info
        document.getElementById('image_name').value = infoObj.name
        document.getElementById('image_url').value = infoObj.key
      'Error': (up, err, errTip) ->
      'UploadComplete': () ->
        document.getElementById('createActivityForm').submit()


upload = ->
  uploader.start()
