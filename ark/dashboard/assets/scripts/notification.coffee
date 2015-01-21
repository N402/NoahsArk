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

$('#receiver').autocomplete
  lookup: ({value: one.label, data: one.value} for one in $('#receivers')[0].options)
  autoSelectFirst: true
  onSelect: (item) ->
    $(this).attr('data', item.data)

$('#receiver').on 'keypress', (event) ->
  if event.keyCode in [13, 32]
    event.preventDefault()
    $("#receivers option[value='#{$('#receiver').attr('data')}']").prop('selected', true)
    $('#receiver').val('')
    $('#receiver').attr('data', '')
    $('#receivers').change()

selectedReceivers = []

$('#receivers').change (event) ->
  selected = $(this).val()
  $.each selected, (idx, each) ->
    return if each in selectedReceivers
    selectedReceivers.push each
    $('#receivers-box').append(
      $("<span class='receiver'>#{$("#receivers option[value='#{each}']").text()}</span>").append
        $("<span class='close-btn'>x</span>").click ->
          $("#receivers option[value='#{each}']").prop('selected', false)
          $(this).parent().remove()
          selectedReceivers.splice selectedReceivers.indexOf(each), 1
    )
