// Trigger the typewriter animation when the page is loaded
$(document).ready(function() {
    $(".typewriter").each(function() {
      var $elem = $(this);
      var text = $elem.text();
      $elem.empty();
      var index = 0;
      var timer = setInterval(function() {
        $elem.text(text.substring(0, index));
        if (++index > text.length) {
          clearInterval(timer);
        }
      }, 80); // Adjust the speed of the animation as needed
    });
  });
  