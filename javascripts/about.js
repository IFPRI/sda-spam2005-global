jQuery(document).ready(function() {
 jQuery('input.prettyCheckable').each(function(){
  $(this).prettyCheckable();
 });
$("#download_button").click(function() {
  jQuery('input.prettyCheckable').each(function(){
  alert($(this))
  });
});
});