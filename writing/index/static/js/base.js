jQuery(function($) {
  // Show/hide modal

  // On menu button click
  $('.menu-toggle').click(function(){
    $('.modal').toggleClass('is-active');
  });

  // Listen for esc to quit
  $(document).keyup(function(e){
    if (e.keyCode === 27){
      $('.modal').toggleClass('is-active');
    };
  })
});


jQuery(function($) {
  // Search children
  // Adapted from https://www.codexworld.com/jquery-live-search-filter-on-html-table/

  $(document).ready(function(){
    $('#menu-search').keyup(function(){
      let query = $(this).val().toLowerCase();

      $('.all-children a').each(function(){
        let kid = $(this).text().toLowerCase()

        if (!kid.includes(query)) {
          $(this).hide();
        } else {
          $(this).show();
        }
      });
    });
  });
});


jQuery(function($){
  // Start by showing relevant chapters only
  $(document).ready(function(){
    let current = $('.panel-tabs .is-active').text();

    $('.sib').each(function() {
      // Show/Hide relevant chapters
      let sib = $(this).attr('id');

      if (sib == current) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });

  });


  // Show/hide chapters depending on selected sib tab
  $('.panel-tabs a').click(function(){
    let name = $(this).text();

    $('.sib').each(function() {
      // Show/Hide relevant chapters
      let sib = $(this).attr('id');

      if (sib == name || name == 'All') {
        $(this).show();
      } else {
        $(this).hide();
      }
    });

    $('.panel-tabs a').each(function(){
      // Highlight relevant sib
      let title = $(this).text();

      if (name == title) {
        $(this).addClass('is-active');
      } else {
        $(this).removeClass('is-active');
      }
    });
  });
});
