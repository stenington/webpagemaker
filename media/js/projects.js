$(function(){
  $('#js-list').click(function(){
    console.log('ok');
    $('.projects').toggleClass('show-list', true).toggleClass('show-thumbs', false);
  });
  $('#js-thumbs').click(function(){
    console.log('wut');
    $('.projects').toggleClass('show-list', false).toggleClass('show-thumbs', true);
  });
});
