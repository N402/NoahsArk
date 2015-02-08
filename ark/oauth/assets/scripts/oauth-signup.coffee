$('#signUpForm input').tooltipster
  trigger: 'custom'
  position: 'top'

$('#signUpForm').ajaxForm
  success: (resp) ->
    if resp.success
      location.href = "/"
    else
      for field, msg of resp.messages
        $("##{field}").tooltipster 'update', msg?.join ','
        $("##{field}").tooltipster 'show'
