$('#ban-btn').click ->
  $.ajax
    url: $(this).attr('href-url')
    type: 'POST'
    dataType: 'json'
    success: (resp) ->
      if resp.success
        $('#ban-btn').hide()
        $('#unban-btn').show()


$('#unban-btn').click ->
  $.ajax
    url: $(this).attr('href-url')
    type: 'DELETE'
    dataType: 'json'
    success: (resp) ->
      if resp.success
        $('#ban-btn').show()
        $('#unban-btn').hide()
