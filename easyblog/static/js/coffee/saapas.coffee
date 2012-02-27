$('.nav-link').click ->
    $(this).addClass 'active'
    

jQuery ($) ->

    $('#myCarousel').carousel
      interval: 8000

    $('.list-items').pajinate
          items_per_page: 15
          nav_label_first: '<<'
          nav_label_last: '>>'
          nav_label_prev: '<'
          nav_label_next: '>'

    $('#wysiwyg').wysiwyg()
    " "
    
