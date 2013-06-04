$(function() {
  $('#released_on').datepicker({
    changeYear: true,
    yearRange: '1940:2000'
  });
  return $('#like input').click(function(event) {
    event.preventDefault();
    return $.post($('#like form').attr('action'), function(data) {
      return $('#like p').html(data).effect('highlight', {
        color: '#fcd'
      });
    });
  });
});