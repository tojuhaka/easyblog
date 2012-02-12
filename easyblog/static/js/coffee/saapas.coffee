jQuery ($) ->
    $('#myCarousel').carousel
      interval: 8000

    $('#items').pajinate ->
          items_per_page: 1
          nav_label_first: '<<'
          nav_label_last: '>>'
          nav_label_prev: '<'
          nav_label_next: '>'
