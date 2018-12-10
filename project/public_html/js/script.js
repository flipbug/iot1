$(document).ready(function($) {
  var $img = $('#image');
  var $imgTitle = $('#image-title');
  var $imgLink = $('#image-link');

  $imgLink.magnificPopup({ type: 'image' });

  $('#snapshot-link, #capture-link').click(function(event) {
    event.preventDefault();
    var id = $(this).attr('id');
    var newSrc = '';
    var newLink = '';

    if (id === 'snapshot-link') {
      $imgTitle.text('Snapshot image');
      newSrc = $img.attr('src').replace('capture.jpg', 'snapshot.png');
      newLink = $imgLink.attr('href').replace('capture.jpg', 'snapshot.png');
    } else {
      $imgTitle.text('Capture image');
      newSrc = $img.attr('src').replace('snapshot.png', 'capture.jpg');
      newLink = $imgLink.attr('href').replace('snapshot.png', 'capture.jpg');
    }

    $img.attr('src', newSrc);
    $imgLink.attr('href', newLink);

    return false;
  })
});
