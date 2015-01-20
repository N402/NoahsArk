$('#activityEditForm').ajaxForm
  type: 'PUT'
  success: (resp) ->
    if resp.success
      $('#info-container').html 'Success'
      $('#info-container').addClass 'success'
      $('#info-container').show()
      window.scrollTo 0, 0
