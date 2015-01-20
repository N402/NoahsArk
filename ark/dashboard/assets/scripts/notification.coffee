$('#notificationSendForm input').tooltipster
  updateAnimation: false
  onlyOne: false
  position: 'right'

$('#notificationSendForm').ajaxForm
  type: 'POST'
  success: (resp) ->
    if resp.success
      $('#info-container').html 'Success'
      $('#info-container').addClass 'success'
      $('#info-container').show()
      document.getElementById('notificationSendForm').reset()
      window.scrollTo 0, 0
    else
      for field, msg of resp.messages
        $("##{field}").tooltipster 'update', msg?.join ','
        $("##{field}").tooltipster 'show'

$('#notificationSendForm').validate
  rules:
    username:
      required: true
    password:
      minlength: 6
      maxlength: 30
  messages:
    username:
      required: '请输入用户名'
    password:
      minlength: '密码不能少于 6 位字符'
      maxlength: '密码不能多于 30 位字符'
  errorPlacement: (error, element) ->
    if $(error).text()
      $(element).tooltipster 'update', $(error).text()
      $(element).tooltipster 'show'
    else
      $(element).tooltipster 'hide'
  success: (label, element) ->
    $(element).tooltipster 'hide'
  submitHandler: (form) ->
    $(form).ajaxSubmit()
