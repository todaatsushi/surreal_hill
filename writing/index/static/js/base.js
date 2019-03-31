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
  // Search Chapters
  // Adapted from https://www.codexworld.com/jquery-live-search-filter-on-html-table/

  $(document).ready(function(){
    $('#menu-search').keyup(function(){
      console.log('Search');
      let query = $(this).val().toLowerCase();

      $('.all-chapters a').each(function(){
        let chapter = $(this).text().toLowerCase()

        if (!chapter.includes(query)) {
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

    $('.story').each(function() {
      // Show/Hide relevant chapters
      let story = $(this).attr('id');

      if (story == current) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });

  });


  // Show/hide chapters depending on selected story tab
  $('.panel-tabs a').click(function(){
    let name = $(this).text();

    $('.story').each(function() {
      // Show/Hide relevant chapters
      let story = $(this).attr('id');

      if (story == name || name == 'All') {
        $(this).show();
      } else {
        $(this).hide();
      }
    });

    $('.panel-tabs a').each(function(){
      // Highlight relevant story
      let title = $(this).text();

      if (name == title) {
        $(this).addClass('is-active');
      } else {
        $(this).removeClass('is-active');
      }
    });
  });
});
