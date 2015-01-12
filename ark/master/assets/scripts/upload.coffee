get_uploader = (upload_btn) -> Qiniu.uploader
    runtimes: 'html5,flash,html4'
    browse_button: upload_btn
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
    auto_start: true
    init:
      'FilesAdded': (up, files) ->
        plupload.each files, (file) ->
          #
      'BeforeUpload': (up, file) ->
        #
      'UploadProgress': (up, file) ->
        #
      'FileUploaded': (up, file, info) ->
        #
      'Error': (up, err, errTip) ->
        #
      'UploadComplete': () ->
        #
