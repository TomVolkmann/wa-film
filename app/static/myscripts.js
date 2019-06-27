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