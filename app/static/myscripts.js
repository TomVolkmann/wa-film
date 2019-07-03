function activeClass() {
    var fullCurrentURL = window.location.href;
    var CurrentURLparts = fullCurrentURL.split("/");
    var CurrentURLindex = CurrentURLparts.length - 1;
    var CurrentURL = CurrentURLparts[CurrentURLindex];
    console.log(CurrentURL);
  
    $('.navbar-nav > li a').each(function() {
      var fullLinkURL = $(this).attr('href');
      var LinkURLparts = fullLinkURL.split("/");
      var LinkURLindex = LinkURLparts.length - 1;
      var LinkURL = LinkURLparts[LinkURLindex];
      if (LinkURL === CurrentURL) {
        $(this).parents("li").addClass("active");
      }

    });
  }
  activeClass();

/* jQuery(function($) {
    function fixDiv() {
     var $cache = $('#productnav');
     if ($(window).scrollTop() > 0)
         $cache.css({

         'display' : 'block',
         'position': 'fixed',
         'top': '0px'

   });
      else
      $cache.css({
      'position': 'relative',
      'top': 'auto',
      'display' : 'block'
   });
}
$(window).scroll(fixDiv);
 fixDiv();
});*/

$(window).scroll(function () {
  if ($(window).scrollTop() >= 50) {
  $('#productnav').css('background','black');
  } else {
  $('#productnav').css('background','transparent');
  }
  });