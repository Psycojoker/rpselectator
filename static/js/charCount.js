(function($) {
  $.fn.charCount = function(options){
    var defaults = {
      allowed: 90,
      warning: 10,
      css: 'counter',
      counterElement: 'span',
      cssWarning: 'warning',
      cssExceeded: 'exceeded',
      counterText: ''
    }; 

    var options = $.extend(defaults, options); 

    function calculate(obj){
      var count = $(obj).val().length;
      var available = options.allowed - count;
      if(available <= options.warning && available >= 0){
        $(obj).next().addClass(options.cssWarning);
      } else {
        $(obj).next().removeClass(options.cssWarning);
      }
      if(available < 0){
        $(obj).next().addClass(options.cssExceeded);
      } else {
        $(obj).next().removeClass(options.cssExceeded);
      }
      $(obj).next().html(options.counterText + available);
    };

    this.each(function() {
      $(this).after('<'+ options.counterElement +' class="' + options.css + '">'+ options.counterText +'</'+ options.counterElement +'>');
      calculate(this);
      $(this).keyup(function(){calculate(this)});
      $(this).change(function(){calculate(this)});
    });

  };

})(jQuery);
