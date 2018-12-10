$(document).ready(function($) {
  var $img = $('#image');
  var $imgTitle = $('#image-title');

  $('#snapshot-link, #capture-link').click(function(event) {
    event.preventDefault();
    var id = $(this).attr('id');
    var newSrc = '';

    if (id === 'snapshot-link') {
      $imgTitle.text('Snapshot image');
      newSrc = $img.attr('src').replace('capture.jpg', 'snapshot.png');
    } else {
      $imgTitle.text('Capture image');
      newSrc = $img.attr('src').replace('snapshot.png', 'capture.jpg');
    }

    $img.attr('src', newSrc);

    return false;
  })
});
